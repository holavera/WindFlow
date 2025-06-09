from django.db import models
from django.contrib.auth.models import User
from django.utils.translation import gettext_lazy as _
from django.utils import timezone
from datetime import timedelta



class Perfil(models.Model):
    class Rol(models.TextChoices):
        GUEST = 'guest', _('Guest')
        FREE_USER = 'free', _('Usuario Gratuito')
        SUBSCRIBED_USER = 'subscribed', _('Usuario Suscrito')
        ADMIN_FREE = 'admin_free', _('Admin Gratuito')
        ADMIN_SUBSCRIBED = 'admin_subscribed', _('Admin Suscrito')

    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='perfil')
    rol = models.CharField(max_length=20, choices=Rol.choices, default=Rol.GUEST)

    def tiene_acceso_premium(self):
        return self.rol in [self.Rol.SUBSCRIBED_USER, self.Rol.ADMIN_SUBSCRIBED]

    @property
    def tiene_suscripcion(self):
        return hasattr(self, 'suscripcion') and self.suscripcion.activa

    def __str__(self):
        return f"{self.user.username} ({self.get_rol_display()})"


class Suscripcion(models.Model):
    perfil = models.OneToOneField('Perfil', on_delete=models.CASCADE, related_name='suscripcion')
    fecha_inicio = models.DateField(default=timezone.now)
    activa = models.BooleanField(default=True)

    def fecha_renovacion(self):
        return self.fecha_inicio + timedelta(days=30)

    def cancelar(self):
        self.activa = False
        self.save()

    def __str__(self):
        return f"Suscripción de {self.perfil.user.username} - Activa: {self.activa}"
