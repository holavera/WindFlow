# winds/models.py
import uuid

from django.db import models
from apps.perfil.models import Perfil
from apps.tareas.models import Tarea
from apps.notas.models import Nota
from apps.pomodoro.models import ConfiguracionPomodoro

class Wind(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    perfil = models.ForeignKey(Perfil, on_delete=models.CASCADE, related_name='winds', null=True, blank=True)
    titulo = models.CharField(max_length=100)
    descripcion = models.TextField(blank=True)
    tareas = models.ManyToManyField(Tarea, blank=True)
    notas = models.ManyToManyField(Nota, blank=True)
    pomodoro = models.ForeignKey(ConfiguracionPomodoro, on_delete=models.SET_NULL, null=True, blank=True, related_name='winds')
    focus_mode = models.BooleanField(default=True, help_text="¿Usar este Wind en modo Focus (Pomodoro incluido)?")

    def __str__(self):
        return f"Wind: {self.titulo} ({self.perfil.user.username})"

