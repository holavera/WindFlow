# tareas/views.py

from django.core.paginator import Paginator
from django.shortcuts import redirect, get_object_or_404, render
from django.template.loader import render_to_string
from django.contrib.auth.decorators import login_required
from .forms import TareaForm
from django.views.decorators.http import require_http_methods
from django.views.decorators.http import require_POST
from django.http import JsonResponse
from .models import Tarea
from ..perfil.decorators import solo_admins, solo_usuarios
from datetime import datetime


@login_required
@solo_usuarios
def user_tareas(request):
    perfil = request.user.perfil
    filtro = request.GET.get('estado')
    tareas_qs = Tarea.objects.filter(perfil=perfil)

    if filtro in dict(Tarea.ESTADO_CHOICES):
        tareas_qs = tareas_qs.filter(estado=filtro)

    tareas_qs = tareas_qs.order_by('-fecha_creacion')
    paginator = Paginator(tareas_qs, 5)
    page_number = request.GET.get('page')
    tareas = paginator.get_page(page_number)

    error_msg = None  # Variable para almacenar el error

    if request.method == 'POST':
        titulo = request.POST.get('titulo', '').strip()
        descripcion = request.POST.get('descripcion', '').strip()
        fecha_raw = request.POST.get('fecha_limite')

        fecha_limite = None
        if fecha_raw:
            try:
                fecha_limite = datetime.strptime(fecha_raw, '%Y-%m-%d').date()
            except ValueError:
                error_msg = "La fecha tiene un formato inválido. Debe ser YYYY-MM-DD."

        if not titulo or not fecha_limite:
            error_msg = "El título y la fecha límite son obligatorios."
        else:
            Tarea.objects.create(perfil=perfil, titulo=titulo, descripcion=descripcion, fecha_limite=fecha_limite)
            return redirect('user_tareas')

    return render(request, 'tareas/user_tareas.html', {
        'tareas': tareas,
        'filtro_actual': filtro,
        'error_msg': error_msg,
    })


@login_required
@solo_usuarios
def editar_tarea(request, tarea_id):
    tarea = get_object_or_404(Tarea, id=tarea_id, perfil=request.user.perfil)
    if request.method == 'POST':
        tarea.titulo = request.POST.get('titulo', '').strip()
        tarea.descripcion = request.POST.get('descripcion', '').strip()

        fecha_raw = request.POST.get('fecha_limite')
        if fecha_raw:
            try:
                tarea.fecha_limite = datetime.strptime(fecha_raw, '%Y-%m-%d').date()
            except ValueError:
                tarea.fecha_limite = None  # O puedes mostrar un error si prefieres
        else:
            tarea.fecha_limite = None

        tarea.estado = request.POST.get('estado')
        tarea.save()
        return redirect('user_tareas')

    return render(request, 'tareas/editar_tarea.html', {'tarea': tarea})



@login_required
@solo_usuarios
def eliminar_tarea(request, tarea_id):
    tarea = get_object_or_404(Tarea, id=tarea_id, perfil=request.user.perfil)
    tarea.delete()
    return redirect('user_tareas')


@require_POST
@login_required
@solo_usuarios
def actualizar_estado_tarea(request):
    tarea_id = request.POST.get('tarea_id')
    completada = request.POST.get('completada') == 'true'

    try:
        tarea = Tarea.objects.get(id=tarea_id, perfil=request.user.perfil)
        tarea.completada = completada
        tarea.save()
        return JsonResponse({'ok': True})
    except Tarea.DoesNotExist:
        return JsonResponse({'ok': False, 'error': 'Tarea no encontrada'}, status=404)


@require_http_methods(["GET", "POST"])
@login_required
@solo_admins
def tarea_ajax_form(request):
    if request.method == 'POST':
        form = TareaForm(request.POST)
        if form.is_valid():
            tarea = form.save(commit=False)
            tarea.perfil = request.user.perfil  # asignación automática del perfil
            tarea.save()
            form.save_m2m()  # por si usas M2M en el futuro
            return JsonResponse({'success': True, 'id': str(tarea.id), 'titulo': tarea.titulo})
        else:
            html = render_to_string('tareas/_form_tarea.html', {'form': form}, request=request)
            return JsonResponse({'success': False, 'form_html': html})
    else:
        form = TareaForm()
        html = render_to_string('tareas/_form_tarea.html', {'form': form}, request=request)
        return JsonResponse({'form_html': html})


# esto es para editar en el wind de grupos - admin
@require_POST
@login_required
@solo_admins
def editar_tarea_ajax(request):
    tarea_id = request.POST.get('id')
    nuevo_titulo = request.POST.get('titulo', '').strip()

    if not nuevo_titulo:
        return JsonResponse({'success': False, 'error': 'Título vacío'})

    try:
        tarea = Tarea.objects.get(id=tarea_id, perfil=request.user.perfil)
        tarea.titulo = nuevo_titulo
        tarea.save()
        return JsonResponse({'success': True, 'titulo': tarea.titulo})
    except Tarea.DoesNotExist:
        return JsonResponse({'success': False, 'error': 'Tarea no encontrada'})


# tareas para wind admin
@require_POST
@login_required
@solo_admins
def eliminar_tarea_ajax(request):
    tarea_id = request.POST.get('id')

    try:
        tarea = Tarea.objects.get(id=tarea_id, perfil=request.user.perfil)
        tarea.delete()
        return JsonResponse({'success': True})
    except Tarea.DoesNotExist:
        return JsonResponse({'success': False, 'error': 'Tarea no encontrada'})
