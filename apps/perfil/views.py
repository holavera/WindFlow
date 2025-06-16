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
'''
import stripe
from django.conf import settings
from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from apps.perfil.decorators import solo_usuarios
stripe.api_key = settings.STRIPE_SECRET_KEY

@login_required
@solo_usuarios
def upgrade_view(request):
    intent = stripe.PaymentIntent.create(
        amount=299,  # cantidad en céntimos (2.99€)
        currency='eur',
        metadata={'user_id': request.user.id}
    )
    context = {
        'client_secret': intent.client_secret,
        'STRIPE_PUBLIC_KEY': settings.STRIPE_PUBLIC_KEY
    }
    return render(request, 'perfil/upgrade.html', context)


@login_required
@solo_usuarios
def pago_completado(request):
    perfil = request.user.perfil
    perfil.rol = Perfil.Rol.SUBSCRIBED_USER
    perfil.save()

    # Crea o reactiva la suscripción
    suscripcion, creada = Suscripcion.objects.get_or_create(perfil=perfil)
    suscripcion.fecha_inicio = timezone.now()
    suscripcion.activa = True
    suscripcion.save()

    messages.success(request, '¡Pago completado! Tu suscripción está activa.')
    return redirect('dashboard_suscrito')


@login_required
@solo_suscritos
def cancelar_suscripcion(request):
    suscripcion = request.user.perfil.suscripcion
    suscripcion.cancelar()
    request.user.perfil.rol = Perfil.Rol.FREE_USER
    request.user.perfil.save()

    messages.info(request, 'Has cancelado tu suscripción. Tienes acceso hasta el final del período.')
    return redirect('dashboard')
'''