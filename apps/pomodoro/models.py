from django.db import models
from apps.perfil.models import Perfil
from django.utils import timezone



class SesionPomodoro(models.Model):
    perfil = models.ForeignKey(Perfil, on_delete=models.CASCADE, related_name='pomodoros')
    config_nombre = models.CharField(max_length=100, null=True, blank=True)
    wind = models.ForeignKey("winds.Wind", on_delete=models.SET_NULL, null=True, blank=True,
                             related_name='sesiones_pomodoro')
    inicio = models.DateTimeField(default=timezone.now)
    fin = models.DateTimeField(null=True, blank=True)
    pausas = models.IntegerField(default=0)
    duracion = models.FloatField(default=0)
    tipo = models.CharField(
        max_length=20,
        choices=[
            ('foco', 'Foco'),
            ('descanso_corto', 'Descanso Corto'),
            ('descanso_largo', 'Descanso Largo'),
        ],
        default='foco'
    )

    def __str__(self):
        return f"{self.tipo} - {self.inicio.strftime('%d/%m/%Y %H:%M')}"

    def esta_completada(self):
        return self.fin is not None and self.fin > self.inicio

    def tiempo_total(self):
        return (self.fin - self.inicio).total_seconds() / 60 if self.fin else None

class ConfiguracionPomodoro(models.Model):
    nombre = models.CharField(max_length=100)
    foco_min = models.IntegerField(default=25)
    descanso_corto_min = models.FloatField(default=5.0)
    descanso_largo_min = models.IntegerField(default=15)
    ciclos = models.IntegerField(default=4)

    def __str__(self):
        return f"{self.nombre} ({self.foco_min}/{self.descanso_corto_min}/{self.descanso_largo_min}) x{self.ciclos}"
