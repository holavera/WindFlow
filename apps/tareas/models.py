from django.db import models
from apps.perfil.models import Perfil
from django.utils import timezone
import uuid

class Tarea(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)

    ESTADO_CHOICES = [
        ('pendiente', 'Pendiente'),
        ('en_progreso', 'En progreso'),
        ('completada', 'Completada'),
    ]

    perfil = models.ForeignKey(Perfil, on_delete=models.CASCADE, related_name='tareas')
    titulo = models.CharField(max_length=255)
    descripcion = models.TextField(blank=True)
    estado = models.CharField(max_length=20, choices=ESTADO_CHOICES, default='pendiente')
    fecha_creacion = models.DateTimeField(default=timezone.now)
    fecha_limite = models.DateField(null=True, blank=True)
    completada = models.BooleanField(default=False)

    def __str__(self):
        return f"{self.titulo} ({self.estado})"