# notas/views.py
from uuid import UUID

from django.http import JsonResponse
from django.shortcuts import render, redirect
from django.template.loader import render_to_string
from django.views.decorators.cache import never_cache
from django.views.decorators.http import require_http_methods, require_POST
from .forms import NotaForm
from .models import Nota
from django.contrib.auth.decorators import login_required
from django.shortcuts import get_object_or_404
from django.contrib import messages

from ..perfil.decorators import solo_usuarios


@never_cache
@login_required
@solo_usuarios
def user_notas(request):
    perfil = request.user.perfil
    notas = Nota.objects.filter(perfil=perfil).order_by('-fecha')

    if request.method == 'POST':
        contenido = request.POST.get('contenido', '').strip()
        if contenido:
            Nota.objects.create(perfil=perfil, contenido=contenido)
            return redirect('user_notas')

    return render(request, 'notas/user_notas.html', {'notas': notas})


@login_required
@solo_usuarios
def editar_nota(request, nota_id: UUID):
    nota = get_object_or_404(Nota, id=nota_id, perfil=request.user.perfil)
    if request.method == 'POST':
        contenido = request.POST.get('contenido', '').strip()
        if contenido:
            nota.contenido = contenido
            nota.save()
            messages.success(request, "Nota actualizada correctamente.")
        return redirect('user_notas')
    return render(request, 'notas/editar_nota.html', {'nota': nota})


@login_required
@solo_usuarios
def eliminar_nota(request, nota_id: UUID):
    nota = get_object_or_404(Nota, id=nota_id, perfil=request.user.perfil)
    nota.delete()
    messages.success(request, "Nota eliminada correctamente.")
    return redirect('user_notas')


# Los siguientes son mini formularios que rellena el administrador para crear winds para sus usuarios.
# para admin
@require_http_methods(["GET", "POST"])
@login_required
def nota_ajax_form(request):
    if request.method == 'POST':
        form = NotaForm(request.POST)
        if form.is_valid():
            nota = form.save(commit=False)
            nota.perfil = request.user.perfil
            nota.save()
            return JsonResponse({'success': True, 'id': str(nota.id), 'contenido': nota.contenido})
        else:
            html = render_to_string('notas/_form_nota.html', {'form': form}, request=request)
            return JsonResponse({'success': False, 'form_html': html})
    else:
        form = NotaForm()
        html = render_to_string('notas/_form_nota.html', {'form': form}, request=request)
        return JsonResponse({'form_html': html})


# esto es para editar notas en los winds del grupo - admin
@require_POST
@login_required
def editar_nota_ajax(request):
    nota_id = request.POST.get('id')
    nuevo_contenido = request.POST.get('contenido', '').strip()

    if not nuevo_contenido:
        return JsonResponse({'success': False, 'error': 'Contenido vacío'})

    try:
        nota = Nota.objects.get(id=nota_id, perfil=request.user.perfil)
        nota.contenido = nuevo_contenido
        nota.save()
        return JsonResponse({'success': True, 'contenido': nota.contenido})
    except Nota.DoesNotExist:
        return JsonResponse({'success': False, 'error': 'Nota no encontrada'})


# notas para eliminar wind admin
@require_POST
@login_required
def eliminar_nota_ajax(request):
    nota_id = request.POST.get('id')

    try:
        nota = Nota.objects.get(id=nota_id, perfil=request.user.perfil)
        nota.delete()
        return JsonResponse({'success': True})
    except Nota.DoesNotExist:
        return JsonResponse({'success': False, 'error': 'Nota no encontrada'})
