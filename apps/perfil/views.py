from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from apps.perfil.models import Perfil, Suscripcion
from apps.perfil.decorators import solo_usuarios, solo_suscritos
from django.shortcuts import redirect
from django.contrib import messages
from django.utils import timezone



@login_required
@solo_usuarios
def upgrade_view(request):
    # Aquí normalmente iría la integración con Stripe o pasarela real.
    return render(request, 'perfil/upgrade.html')


@login_required
@solo_usuarios
def pago_completado(request):
    perfil = request.user.perfil
    perfil.rol = Perfil.Rol.SUBSCRIBED_USER
    perfil.save()
    return redirect('dashboard_suscrito')


# PASARELA DE PAGO
