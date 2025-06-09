from django.shortcuts import render
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from .models import SesionPomodoro
from django.utils import timezone
import json
from django.contrib.auth.decorators import login_required
from django.views.decorators.http import require_POST
from datetime import timedelta
from django.views.generic import TemplateView
from ..perfil.decorators import solo_suscritos, solo_usuarios
from ..winds.models import Wind
from .models import ConfiguracionPomodoro

class GuestPomodoroView(TemplateView):
    template_name = 'pomodoro/guest_dashboard_pomodoro.html'


@csrf_exempt
@require_POST
@login_required
@solo_usuarios
def iniciar_pomodoro(request):
    datos = json.loads(request.body)
    tipo = datos.get('tipo', 'foco')
    wind_id = datos.get('wind_id')

    wind = Wind.objects.filter(id=wind_id, perfil=request.user.perfil).first() if wind_id else None

    config_id = datos.get('config_id')
    config = ConfiguracionPomodoro.objects.filter(id=config_id).first()

    sesion = SesionPomodoro.objects.create(
        perfil=request.user.perfil,
        tipo=tipo,
        wind=wind,
        inicio=timezone.now(),
        config_nombre=config.nombre if config else None  # ✅ GUARDAR NOMBRE
    )
    return JsonResponse({'status': 'ok', 'id': str(sesion.id)})


@csrf_exempt
@require_POST
@login_required
@solo_usuarios
def finalizar_pomodoro(request):
    datos = json.loads(request.body)
    id_sesion = datos.get('id')
    #pausas = datos.get('pausas', 0)
    duracion = datos.get('duracion')

    try:
        sesion = SesionPomodoro.objects.get(id=id_sesion, perfil=request.user.perfil)
        sesion.fin = timezone.now()
        #sesion.pausas = pausas
        sesion.duracion = duracion
        sesion.save()
        return JsonResponse({'status': 'finalizado'})
    except SesionPomodoro.DoesNotExist:
        return JsonResponse({'error': 'Sesión no encontrada'}, status=404)


@login_required
@solo_usuarios
def user_pomodoro(request):
    config_id = request.GET.get('config')
    wind_id = request.GET.get('wind')

    config = ConfiguracionPomodoro.objects.filter(id=config_id).first() if config_id else None
    wind = Wind.objects.filter(id=wind_id, perfil=request.user.perfil).first() if wind_id else None

    if wind and not config:
        config = wind.pomodoro

    return render(request, 'pomodoro/user_pomodoro.html', {
        'config': config,
        'wind': wind
    })


@login_required
@solo_suscritos
def historial_pomodoros(request):
    perfil = request.user.perfil
    filtro = request.GET.get('filtro', 'semana')
    ahora = timezone.now()

    if filtro == 'hoy':
        inicio = ahora.replace(hour=0, minute=0, second=0)
        sesiones = SesionPomodoro.objects.filter(perfil=perfil, inicio__gte=inicio)
    elif filtro == 'semana':
        inicio = ahora - timedelta(days=7)
        sesiones = SesionPomodoro.objects.filter(perfil=perfil, inicio__gte=inicio)
    else:
        sesiones = SesionPomodoro.objects.filter(perfil=perfil)

    sesiones = sesiones.order_by('-inicio')
    return render(request, 'pomodoro/historial.html', {'sesiones': sesiones, 'filtro': filtro})


@login_required
@solo_usuarios
def seleccionar_configuracion(request):
    configuraciones = ConfiguracionPomodoro.objects.all()
    return render(request, 'pomodoro/seleccionar.html', {'configuraciones': configuraciones})
