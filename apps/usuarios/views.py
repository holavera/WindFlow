#usuarios/views.py

from django.shortcuts import render, redirect
from django.contrib.auth import login
from django.contrib.auth.views import LoginView
from django.views import View
from .forms import CustomUserCreationForm
from django.views.decorators.cache import never_cache
from django.contrib.auth import logout
from apps.perfil.models import Perfil
from django.views.generic import TemplateView
from django.utils.decorators import method_decorator
from django.contrib.auth.decorators import login_required
from apps.perfil.decorators import solo_suscritos, solo_invitados, solo_basicos
from ..pomodoro.models import SesionPomodoro
from ..winds.models import Wind
from django.db.models import Count, Sum
from datetime import timedelta
from reportlab.lib.pagesizes import A4
from reportlab.pdfgen import canvas
from reportlab.lib.units import cm
from django.http import HttpResponse
from apps.notas.models import Nota
from apps.tareas.models import Tarea
from django.utils.timezone import now



@method_decorator([login_required, never_cache], name='dispatch')
class DashboardView(View):
    def get(self, request):
        perfil = request.user.perfil

        if perfil.rol == Perfil.Rol.ADMIN_FREE or perfil.rol == Perfil.Rol.ADMIN_SUBSCRIBED:
            return render(request, 'usuarios/dashboard_admin.html')
        elif perfil.rol == Perfil.Rol.SUBSCRIBED_USER:
            return render(request, 'usuarios/dashboard_user.html', {'premium': True})
        elif perfil.rol == Perfil.Rol.FREE_USER:
            return render(request, 'usuarios/dashboard_user.html', {'premium': False})
        elif perfil.rol == Perfil.Rol.GUEST:
            return render(request, 'usuarios/guest_dashboard.html')
        else:
            return render(request, 'usuarios/dashboard_user.html')  # fallback


def logout_view(request):
    logout(request)
    return redirect('home')


class CustomLoginView(LoginView):
    template_name = 'usuarios/login.html'  # 🔥 ESTA LÍNEA ES CLAVE

    def dispatch(self, request, *args, **kwargs):
        if request.user.is_authenticated:
            return redirect('dashboard')
        return super().dispatch(request, *args, **kwargs)


class RegisterView(View):
    def dispatch(self, request, *args, **kwargs):
        if request.user.is_authenticated:
            return redirect('dashboard')
        return super().dispatch(request, *args, **kwargs)

    def get(self, request):
        form = CustomUserCreationForm()
        return render(request, 'usuarios/register.html', {'form': form})

    def post(self, request):
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            rol_elegido = form.cleaned_data['rol_inicial']
            if rol_elegido == 'admin_free':
                perfil = Perfil.objects.create(user=user, rol=Perfil.Rol.ADMIN_FREE)
            else:
                perfil = Perfil.objects.create(user=user, rol=Perfil.Rol.FREE_USER)
            login(request, user)
            return redirect('dashboard')
        return render(request, 'usuarios/register.html', {'form': form})


class GuestView(TemplateView):
    template_name = 'usuarios/guest_dashboard.html'


@method_decorator([login_required, solo_suscritos], name='dispatch')
class DashboardSuscritoView(TemplateView):
    template_name = 'usuarios/user_suscribed_dashboard.html'


@login_required
@solo_suscritos
def estadisticas_usuario(request):
    perfil = request.user.perfil

    # Datos base
    notas = Nota.objects.filter(perfil=perfil)
    tareas = Tarea.objects.filter(perfil=perfil)
    winds = Wind.objects.filter(perfil=perfil)
    pomodoros = SesionPomodoro.objects.filter(perfil=perfil)

    # Métricas extra
    hoy = now().date()
    semana = hoy - timedelta(days=7)

    pomodoros_hoy = pomodoros.filter(inicio__date=hoy).count()
    pomodoros_semana = pomodoros.filter(inicio__date__gte=semana).count()
    tiempo_total = pomodoros.aggregate(Sum('duracion'))['duracion__sum'] or 0

    tareas_completadas = tareas.filter(estado='completada').count()
    tareas_pendientes = tareas.filter(estado='pendiente').count()
    total_tareas = tareas.count()
    productividad = round((tareas_completadas / total_tareas) * 100, 1) if total_tareas else 0

    #ultima_nota = notas.order_by('-id').first()

    wind_mas_usado = winds.annotate(
        pomodoros_count=Count('sesiones_pomodoro')
    ).order_by('-pomodoros_count').first()

    promedio_elementos_wind = round(winds.annotate(total=Count('tareas') + Count('notas')).aggregate(Sum('total'))['total__sum'] / winds.count(), 1) if winds.count() else 0

    return render(request, 'usuarios/estadisticas_usuario.html', {
        'num_notas': notas.count(),
        'num_tareas': total_tareas,
        'num_winds': winds.count(),
        'num_pomodoros': pomodoros.count(),
        'pomodoros_hoy': pomodoros_hoy,
        'pomodoros_semana': pomodoros_semana,
        'tiempo_total': tiempo_total,
        'tareas_completadas': tareas_completadas,
        'tareas_pendientes': tareas_pendientes,
        'productividad': productividad,
        #'ultima_nota': ultima_nota,
        'wind_mas_usado': wind_mas_usado,
        'promedio_wind': promedio_elementos_wind,
    })


@login_required
@solo_suscritos
def exportar_notas_pdf(request):
    notas = Nota.objects.filter(perfil=request.user.perfil)
    response = HttpResponse(content_type='application/pdf')
    response['Content-Disposition'] = f'attachment; filename=notas_{request.user.username}.pdf'

    p = canvas.Canvas(response, pagesize=A4)
    y = A4[1] - 2 * cm
    p.setFont("Helvetica-Bold", 14)
    p.drawString(2 * cm, y, f"📝 Notas de {request.user.username}")
    y -= 1 * cm
    p.setFont("Helvetica", 10)

    for nota in notas:
        if y < 3 * cm:
            p.showPage()
            y = A4[1] - 2 * cm
            p.setFont("Helvetica", 10)
        p.drawString(2 * cm, y, f"• {nota.fecha.strftime('%d/%m/%Y %H:%M')}")
        y -= 0.6 * cm
        p.drawString(2.5 * cm, y, nota.contenido[:120] + "..." if len(nota.contenido) > 120 else nota.contenido)
        y -= 1 * cm

    p.save()
    return response


@login_required
@solo_suscritos
def exportar_tareas_pdf(request):
    tareas = Tarea.objects.filter(perfil=request.user.perfil)
    response = HttpResponse(content_type='application/pdf')
    response['Content-Disposition'] = f'attachment; filename=tareas_{request.user.username}.pdf'

    p = canvas.Canvas(response, pagesize=A4)
    y = A4[1] - 2 * cm
    p.setFont("Helvetica-Bold", 14)
    p.drawString(2 * cm, y, f"✅ Tareas de {request.user.username}")
    y -= 1 * cm
    p.setFont("Helvetica", 10)

    for tarea in tareas:
        if y < 3 * cm:
            p.showPage()
            y = A4[1] - 2 * cm
            p.setFont("Helvetica", 10)

        p.drawString(2 * cm, y, f"• {tarea.titulo} ({tarea.get_estado_display()})")
        y -= 0.5 * cm
        if tarea.descripcion:
            p.drawString(2.5 * cm, y, tarea.descripcion[:100] + "..." if len(tarea.descripcion) > 100 else tarea.descripcion)
            y -= 0.5 * cm
        p.drawString(2.5 * cm, y, f"Creada: {tarea.fecha_creacion.strftime('%d/%m/%Y')} - Límite: {tarea.fecha_limite.strftime('%d/%m/%Y') if tarea.fecha_limite else 'No establecida'}")
        y -= 0.9 * cm

    p.save()
    return response


@login_required
@solo_suscritos
def exportar_estadisticas_pdf(request):
    perfil = request.user.perfil

    notas_total = perfil.notas.count()
    tareas_total = perfil.tareas.count()
    tareas_completadas = perfil.tareas.filter(estado='completada').count()
    winds_total = perfil.winds.count()
    pomodoros = perfil.pomodoros.all()
    tiempo_total = pomodoros.aggregate(Sum('duracion'))['duracion__sum'] or 0

    response = HttpResponse(content_type='application/pdf')
    response['Content-Disposition'] = f'attachment; filename=estadisticas_{request.user.username}.pdf'

    p = canvas.Canvas(response, pagesize=A4)
    y = A4[1] - 2 * cm

    p.setFont("Helvetica-Bold", 14)
    p.drawString(2 * cm, y, f"📊 Estadísticas de {request.user.username}")
    y -= 1 * cm

    p.setFont("Helvetica", 11)
    p.drawString(2 * cm, y, f"- Notas: {notas_total}")
    y -= 0.6 * cm
    p.drawString(2 * cm, y, f"- Tareas: {tareas_total} (completadas: {tareas_completadas})")
    y -= 0.6 * cm
    p.drawString(2 * cm, y, f"- Winds: {winds_total}")
    y -= 0.6 * cm
    p.drawString(2 * cm, y, f"- Sesiones Pomodoro: {pomodoros.count()}")
    y -= 0.6 * cm
    p.drawString(2 * cm, y, f"- Tiempo total Pomodoro: {round(tiempo_total)} min")
    y -= 0.6 * cm


    p.save()
    return response

