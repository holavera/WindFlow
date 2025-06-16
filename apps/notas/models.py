#notas/models.py
import uuid
from dataclasses import dataclass
from django.db import models
from apps.perfil.models import Perfil
from datetime import datetime, date


class Nota(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    perfil = models.ForeignKey(Perfil, on_delete=models.CASCADE, related_name='notas')
    contenido = models.TextField()
    fecha = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Nota de {self.perfil.user.username} - {self.fecha}"

    class Meta:
        ordering = ['-fecha']


@dataclass
class NotaSession:
    id: float
    contenido: str
    fecha: str

    @staticmethod
    def crear(post_data):
        return NotaSession(
            id=datetime.now().timestamp(),
            contenido=post_data.get("contenido", "").strip(),
            fecha=datetime.now().strftime("%Y-%m-%d %H:%M")
        )

    @staticmethod
    def obtener_todas(request):
        return request.session.get('notas_guest', [])

    @staticmethod
    def guardar(request, nota):
        notas = NotaSession.obtener_todas(request)
        notas.append(nota.__dict__)
        request.session['notas_guest'] = notas
        request.session.modified = True

    @staticmethod
    def eliminar(request, nota_id):
        try:
            nota_id_float = float(nota_id)
        except (ValueError, TypeError):
            return
        notas = NotaSession.obtener_todas(request)
        nuevas = [n for n in notas if float(n.get('id', -1)) != nota_id_float]
        request.session['notas_guest'] = nuevas
        request.session.modified = True

    @staticmethod
    def editar(request, nota_id, nuevo_contenido):
        notas = NotaSession.obtener_todas(request)
        for nota in notas:
            if str(nota['id']) == str(nota_id):
                nota['contenido'] = nuevo_contenido
                break
        request.session['notas_guest'] = notas
        request.session.modified = True
