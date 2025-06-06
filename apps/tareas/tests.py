
from django.test import TestCase
from django.urls import reverse
from django.contrib.auth.models import User
from apps.perfil.models import Perfil
from .models import Tarea
from datetime import date


class CrearTareaTests(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(username='testuser', password='testpass')
        self.perfil = Perfil.objects.create(user=self.user)
        self.client.login(username='testuser', password='testpass')

    # Recuerda que el decorador @solo_usuarios no es necesario en las pruebas unitarias. Entonces quitalo de la vista `user_tareas` si lo tienes.
    def test_usuario_puede_crear_tarea(self):
        url = reverse('user_tareas')
        datos = {
            'titulo': 'Tarea de prueba',
            'descripcion': 'Esta es una tarea de test.',
            'fecha_limite': date.today().strftime('%Y-%m-%d'),
        }

        response = self.client.post(url, datos)

        self.assertEqual(response.status_code, 302)  # Redirección tras crear
        self.assertEqual(Tarea.objects.count(), 1)

        tarea = Tarea.objects.first()
        self.assertEqual(tarea.titulo, 'Tarea de prueba')
        self.assertEqual(tarea.descripcion, 'Esta es una tarea de test.')
        self.assertEqual(tarea.perfil, self.perfil)
        print(f"Tarea creada: {tarea.titulo} con fecha límite {tarea.fecha_limite}")
        print(f"Perfil asociado: {tarea.perfil.user.username}")
