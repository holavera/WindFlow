# admin_wind/models.py
import uuid

from django.db import models
from apps.perfil.models import Perfil

class GrupoPersonal(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    nombre = models.CharField(max_length=100)
    descripcion = models.TextField(blank=True)
    admin = models.ForeignKey(Perfil, on_delete=models.CASCADE, related_name='grupos_creados')
    usuarios = models.ManyToManyField(Perfil, related_name='grupos_pertenecientes', blank=True)

    def __str__(self):
        return f"{self.nombre} (admin: {self.admin.user.username})"
