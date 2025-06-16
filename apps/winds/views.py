# winds/views.py
from uuid import UUID

from django.shortcuts import render, redirect
from .forms import WindForm
from django.contrib.auth.decorators import login_required
from .models import Wind
from django.shortcuts import get_object_or_404
from django.contrib import messages

from ..perfil.decorators import solo_usuarios


@login_required
@solo_usuarios
def user_winds(request):
    winds = Wind.objects.filter(perfil=request.user.perfil).order_by('-id')
    return render(request, 'winds/user_winds.html', {'winds': winds})


@login_required
@solo_usuarios
def ver_wind(request, wind_id: UUID):
    wind = get_object_or_404(Wind, id=wind_id, perfil=request.user.perfil)

    if wind.focus_mode:
        return render(request, 'winds/focus_mode.html', {'wind': wind})
    else:
        return render(request, 'winds/user_wind.html', {'wind': wind})


@login_required
@solo_usuarios
def crear_wind(request):
    if request.method == 'POST':
        form = WindForm(request.POST, perfil=request.user.perfil)
        if form.is_valid():
            wind = form.save(commit=False)
            wind.perfil = request.user.perfil
            wind.save()
            form.save_m2m()
            return redirect('user_winds')
    else:
        form = WindForm(perfil=request.user.perfil)

    return render(request, 'winds/crear_wind.html', {'form': form})


@login_required
@solo_usuarios
def editar_wind(request, wind_id: UUID):
    wind = get_object_or_404(Wind, id=wind_id, perfil=request.user.perfil)

    if request.method == 'POST':
        form = WindForm(request.POST, perfil=request.user.perfil, instance=wind)
        if form.is_valid():
            form.save()
            return redirect('user_winds')  # redirige al dashboard del usuario o listado de winds
    else:
        form = WindForm(perfil=request.user.perfil, instance=wind)

    return render(request, 'winds/editar_wind.html', {'form': form, 'wind': wind})


@login_required
@solo_usuarios
def eliminar_wind(request, wind_id: UUID):
    wind = get_object_or_404(Wind, id=wind_id, perfil=request.user.perfil)

    if request.method == 'POST':
        wind.delete()
        messages.success(request, "Wind eliminado correctamente.")
        return redirect('user_winds')

    return render(request, 'winds/eliminar_wind_confirmacion.html', {'wind': wind})
