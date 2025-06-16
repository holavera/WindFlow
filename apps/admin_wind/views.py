# admin_wind/views.py

from datetime import date, timedelta
from uuid import UUID

from .forms import GrupoForm, CrearWindGrupoForm
from django.views.generic import CreateView, ListView
from django.urls import reverse_lazy
from .forms import GrupoForm
from django.views.generic import DetailView
from .forms import AgregarUsuarioGrupoForm
from django.http import HttpResponseRedirect
from django.views.generic import DeleteView
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.urls import reverse
from apps.winds.forms import WindGrupoForm
from django.views.generic import TemplateView
from django.views import View
from apps.perfil.models import Perfil
from apps.winds.models import Wind
from apps.pomodoro.models import SesionPomodoro
from apps.admin_wind.models import GrupoPersonal
from django.db.models import Sum, Avg, Max, Count
from apps.perfil.decorators import solo_admins
from django.utils.decorators import method_decorator
from django.utils.timezone import localtime
from datetime import datetime, timedelta
from django.http import HttpResponse
import json
from apps.tareas.models import Tarea
from apps.notas.models import Nota




@method_decorator(solo_admins, name='dispatch')
class EstadisticasAdminView(TemplateView):
    template_name = "admin_wind/estadisticas_completas.html"


class GrupoListView(ListView):
    model = GrupoPersonal
    template_name = 'admin_wind/gestion_grupos.html'

    def get_queryset(self):
        return GrupoPersonal.objects.filter(admin=self.request.user.perfil)


@method_decorator(solo_admins, name='dispatch')
class CrearGrupoView(CreateView):
    model = GrupoPersonal
    form_class = GrupoForm
    template_name = "admin_wind/crear_grupo.html"

    def form_valid(self, form):
        form.instance.admin = self.request.user.perfil
        response = super().form_valid(form)
        return response

    def get_success_url(self):
        return reverse_lazy('detalle_grupo', kwargs={'pk': self.object.pk})


@method_decorator(solo_admins, name='dispatch')
class ListaGruposAdminView(ListView):
    model = GrupoPersonal
    template_name = 'admin_wind/gestion_grupos.html'

    def get_queryset(self):
        return GrupoPersonal.objects.filter(admin=self.request.user.perfil)


@method_decorator(solo_admins, name='dispatch')
class GestionGrupoDetalleView(DetailView):
    model = GrupoPersonal
    template_name = "admin_wind/grupo_detalle.html"
    context_object_name = "grupo"

    def get_queryset(self):
        return GrupoPersonal.objects.filter(admin=self.request.user.perfil)

    def post(self, request, *args, **kwargs):
        self.object = self.get_object()
        form = AgregarUsuarioGrupoForm(request.POST)
        if form.is_valid():
            perfil = form.cleaned_data['query']
            self.object.usuarios.add(perfil)
            return redirect('detalle_grupo', pk=self.object.pk)
        return self.render_to_response(self.get_context_data(form=form))

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['form'] = kwargs.get('form', AgregarUsuarioGrupoForm())
        context['form_wind'] = CrearWindGrupoForm(grupo=self.object)
        return context


class EliminarUsuarioDeGrupoView(View):
    def post(self, request, grupo_id: UUID, usuario_id):
        grupo = get_object_or_404(GrupoPersonal, id=grupo_id, admin=request.user.perfil)
        perfil = get_object_or_404(Perfil, id=usuario_id)

        if perfil in grupo.usuarios.all():
            grupo.usuarios.remove(perfil)
            messages.success(request, f"El usuario {perfil.user.username} fue eliminado del grupo.")

        return HttpResponseRedirect(reverse('detalle_grupo', kwargs={'pk': grupo_id}))


class EliminarGrupoView(DeleteView):
    model = GrupoPersonal
    success_url = reverse_lazy('gestion_grupos')
    template_name = 'admin_wind/confirmar_eliminar_grupo.html'

    def get_queryset(self):
        return GrupoPersonal.objects.filter(admin=self.request.user.perfil)

    def delete(self, request, *args, **kwargs):
        grupo = self.get_object()
        messages.success(request, f"El grupo '{grupo.nombre}' fue eliminado correctamente.")
        return super().delete(request, *args, **kwargs)

# crear winds para usuarios

@method_decorator(solo_admins, name='dispatch')
class CrearWindParaGrupoView(View):
    def post(self, request, grupo_id):
        grupo = get_object_or_404(GrupoPersonal, id=grupo_id, admin=request.user.perfil)
        form = WindGrupoForm(request.POST, grupo=grupo)

        if form.is_valid():
            titulo = form.cleaned_data['titulo']
            descripcion = form.cleaned_data['descripcion']

            tareas_ids = [id for id in request.POST.get('tareas_ids', '').split(',') if id]
            notas_ids = [id for id in request.POST.get('notas_ids', '').split(',') if id]


            tareas = Tarea.objects.filter(id__in=tareas_ids)
            notas = Nota.objects.filter(id__in=notas_ids)

            pomodoro = form.cleaned_data['pomodoro']
            focus_mode = form.cleaned_data['focus_mode']
            usuarios = form.cleaned_data['usuarios']

            for perfil in usuarios:
                wind = Wind.objects.create(
                    titulo=titulo,
                    descripcion=descripcion,
                    perfil=perfil,
                    pomodoro=pomodoro,
                    focus_mode=focus_mode
                )

                for tarea in tareas:
                    copia = tarea
                    copia.pk = None
                    copia.perfil = perfil
                    copia.save()
                    wind.tareas.add(copia)
                    

                for nota in notas:
                    copia = nota
                    copia.pk = None
                    copia.perfil = perfil
                    copia.save()
                    wind.notas.add(copia)

                tareas.filter(perfil=request.user.perfil).delete()
                notas.filter(perfil=request.user.perfil).delete()
            

            messages.success(request, f"Wind creado para {usuarios.count()} usuario(s) del grupo.")
            return redirect('detalle_grupo', pk=grupo.id)

        # Si el formulario no es válido, volvemos a mostrar la vista con errores
        return render(request, 'admin_wind/grupo_detalle.html', {
            'grupo': grupo,
            'form': AgregarUsuarioGrupoForm(),
            'form_wind': form,
        })


@method_decorator(solo_admins, name='dispatch')
class EstadisticasGrupoView(TemplateView):
    template_name = 'admin_wind/estadisticas_completas.html'

    def get_context_data(self, **kwargs):
        from django.db.models import Max
        contexto = super().get_context_data(**kwargs)
        grupo = GrupoPersonal.objects.get(pk=self.kwargs['grupo_id'], admin=self.request.user.perfil)
        usuarios = grupo.usuarios.all()
        datos = []

        labels = []
        valores = []

        # para filtrar
        rango = self.request.GET.get('rango')
        fecha_hoy = date.today()

        # Variables para filtrar sesiones
        fecha_inicio = None
        fecha_fin = None

        if rango == 'hoy':
            fecha_inicio = fecha_hoy
            fecha_fin = fecha_hoy
        elif rango == 'semana':
            fecha_inicio = fecha_hoy - timedelta(days=fecha_hoy.weekday())  # lunes
            fecha_fin = fecha_hoy  # hasta hoy

        for perfil in usuarios:

            winds = Wind.objects.filter(perfil=perfil)
            total_elementos = 0
            for w in winds:
                total_elementos += w.tareas.count() + w.notas.count()

            promedio_elementos = round(total_elementos / winds.count(), 1) if winds.exists() else 0

            sesiones = SesionPomodoro.objects.filter(perfil=perfil)
            completadas = sesiones.filter(fin__isnull=False)
            total = sesiones.count()
            total_min = sesiones.aggregate(total=Sum('duracion'))['total'] or 0
            pausas_prom = sesiones.aggregate(p=Avg('pausas'))['p'] or 0
            mas_larga = sesiones.aggregate(m=Max('duracion'))['m'] or 0

            if fecha_inicio and fecha_fin:
                sesiones = sesiones.filter(inicio__date__range=(fecha_inicio, fecha_fin))

            # Para la grafica
            labels.append(perfil.user.username)
            valores.append(winds.count())

            # Configuración más usada
            config_mas_usada = sesiones.exclude(config_nombre__isnull=True).exclude(config_nombre__exact='') \
                .values('config_nombre') \
                .annotate(c=Count('id')).order_by('-c').first()

            config_nombre = config_mas_usada['config_nombre'] if config_mas_usada else 'N/A'

            datos.append({
                'usuario': perfil.user.username,
                'email': perfil.user.email,
                'num_winds': winds.count(),
                'promedio_elementos': promedio_elementos,
                'winds_focus': winds.filter(focus_mode=True).count(),
                'pomodoros': total,
                'completadas': completadas.count(),
                'porcentaje_completadas': round(completadas.count() / total * 100, 1) if total else 0,
                'minutos': round(total_min, 1),
                'pausas_promedio': round(pausas_prom, 1),
                'mas_larga': round(mas_larga, 1),
                'config': config_nombre,
                'perfil_id': perfil.id,

            })

        contexto['grupo'] = grupo
        contexto['estadisticas'] = datos
        contexto['labels'] = json.dumps(labels)
        contexto['valores'] = json.dumps(valores)
        return contexto


@method_decorator(solo_admins, name='dispatch')
class ExportarEstadisticasPDFView(View):
    def get(self, request, grupo_id):
        from reportlab.lib.pagesizes import A4
        from reportlab.pdfgen import canvas
        from reportlab.lib.units import cm
        from apps.pomodoro.models import SesionPomodoro
        from django.utils.timezone import localtime

        hoy = localtime().date()
        rango = request.GET.get('rango')

        # Definimos rango de fechas según filtro
        fecha_inicio = fecha_fin = hoy
        if rango == 'semana':
            fecha_inicio = hoy - timedelta(days=hoy.weekday())  # lunes

        grupo = GrupoPersonal.objects.get(pk=grupo_id, admin=request.user.perfil)
        usuarios = grupo.usuarios.all()

        # Configuración PDF
        response = HttpResponse(content_type='application/pdf')
        response['Content-Disposition'] = f'attachment; filename="estadisticas_{grupo.nombre}.pdf"'
        p = canvas.Canvas(response, pagesize=A4)
        width, height = A4
        y = height - 2.5 * cm
        row_height = 0.6 * cm

        # Título
        p.setFont("Helvetica-Bold", 16)
        p.drawString(2 * cm, y, f"📊 Estadísticas del grupo: {grupo.nombre}")
        y -= 1 * cm

        columnas = ["Usuario", "Winds", "Prom.", "Focus", "Pomodoros", "%", "Min", "Larga", "Config"]
        col_widths = [2*cm, 1.5*cm, 1.8*cm, 2*cm, 2*cm, 2*cm, 2*cm, 2*cm, 2*cm]

        p.setFont("Helvetica-Bold", 9)
        p.setFillColorRGB(0.9, 0.9, 0.9)
        p.rect(2 * cm, y, sum(col_widths), row_height, fill=True, stroke=False)
        p.setFillColorRGB(0, 0, 0)

        x = 2 * cm
        for i, col in enumerate(columnas):
            p.drawString(x + 2, y + 4, col)
            x += col_widths[i]
        y -= row_height

        # Tabla resumen
        p.setFont("Helvetica", 9)
        for perfil in usuarios:
            sesiones = SesionPomodoro.objects.filter(
                perfil=perfil,
                inicio__date__range=(fecha_inicio, fecha_fin)
            ).order_by('-inicio')

            completadas = sesiones.filter(fin__isnull=False)
            total = sesiones.count()
            total_min = sesiones.aggregate(total=Sum('duracion'))['total'] or 0
            mas_larga = sesiones.aggregate(m=Max('duracion'))['m'] or 0

            winds = Wind.objects.filter(perfil=perfil)
            total_elementos = sum(w.tareas.count() + w.notas.count() for w in winds)
            promedio_elementos = round(total_elementos / winds.count(), 1) if winds.exists() else 0

            config_mas_usada = sesiones.exclude(config_nombre__isnull=True).exclude(config_nombre__exact='') \
                .values('config_nombre').annotate(c=Count('id')).order_by('-c').first()
            config_nombre = config_mas_usada['config_nombre'] if config_mas_usada else 'N/A'

            fila = [
                perfil.user.username,
                str(winds.count()),
                str(promedio_elementos),
                str(winds.filter(focus_mode=True).count()),
                str(total),
                f"{round(completadas.count() / total * 100, 1) if total else 0} %",
                str(round(total_min, 1)),
                str(round(mas_larga, 1)),
                config_nombre[:15]
            ]

            x = 2 * cm
            for i, val in enumerate(fila):
                p.drawString(x + 2, y + 4, val)
                x += col_widths[i]

            y -= row_height
            if y < 4 * cm:
                p.showPage()
                p.setFont("Helvetica", 8)
                p.setFillColorRGB(0, 0, 0)
                y = height - 3 * cm

        # Historial Pomodoro de hoy
        if y < 5 * cm:
            p.showPage()
            y = height - 3 * cm

        p.setFont("Helvetica-Bold", 14)
        p.drawString(2 * cm, y, "📜 Historial de Pomodoro de cada usuario")
        y -= 0.4 * cm
        p.setFont("Helvetica", 9)
        p.drawString(2 * cm, y, f"(Solo sesiones del día: {hoy.strftime('%d/%m/%Y')})")
        y -= 1 * cm

        for perfil in usuarios:
            sesiones = SesionPomodoro.objects.filter(
                perfil=perfil,
                inicio__date=hoy
            ).order_by('-inicio')

            if y < 5 * cm:
                p.showPage()
                y = height - 3 * cm

            p.setFont("Helvetica-Bold", 11)
            p.drawString(2 * cm, y, f"👤 {perfil.user.username} ({perfil.user.email})")
            y -= 0.6 * cm

            p.setFont("Helvetica-Bold", 8)
            p.drawString(2 * cm, y, "Fecha")
            p.drawString(6 * cm, y, "Tipo")
            p.drawString(9 * cm, y, "Duración")
            p.drawString(12 * cm, y, "Config.")
            p.drawString(15 * cm, y, "Wind")
            y -= 0.4 * cm

            p.setFont("Helvetica", 8)
            if sesiones.exists():
                for s in sesiones:
                    if y < 3 * cm:
                        p.showPage()
                        y = height - 3 * cm

                    p.drawString(2 * cm, y, localtime(s.inicio).strftime("%d/%m/%Y %H:%M"))
                    p.drawString(6 * cm, y, s.get_tipo_display())
                    duracion = f"{s.tiempo_total():.1f}" if s.esta_completada() else "-"
                    p.drawString(9 * cm, y, duracion)
                    p.drawString(12 * cm, y, s.config_nombre or "-")
                    p.drawString(15 * cm, y, s.wind.titulo if s.wind else "-")
                    y -= 0.35 * cm
            else:
                p.setFont("Helvetica-Oblique", 8)
                p.drawString(2 * cm, y, "No hay sesiones registradas hoy.")
                y -= 0.5 * cm

            y -= 0.8 * cm

        p.save()
        return response



@method_decorator(solo_admins, name='dispatch')
class HistorialPomodoroAdminView(TemplateView):
    template_name = 'admin_wind/historial_admin.html'

    def get_context_data(self, **kwargs):
        contexto = super().get_context_data(**kwargs)
        grupo = get_object_or_404(GrupoPersonal, pk=kwargs['grupo_id'], admin=self.request.user.perfil)

        # Esta línea asegura que solo usuarios del grupo puedan ser consultados
        perfil = get_object_or_404(grupo.usuarios, pk=kwargs['perfil_id'])

        sesiones = SesionPomodoro.objects.filter(perfil=perfil).order_by('-inicio')

        contexto['grupo'] = grupo
        contexto['usuario'] = perfil.user.username
        contexto['sesiones'] = sesiones
        return contexto
