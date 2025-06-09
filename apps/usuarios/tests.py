
from django.test import TestCase
from django.urls import reverse
from django.contrib.auth.models import User
from django.test import TestCase
from django.urls import reverse
from django.contrib.auth.models import User
from apps.perfil.models import Perfil  

class LoginTests(TestCase):

    def setUp(self):
        self.username = 'testuser'
        self.password = 'securepassword123'
        self.user = User.objects.create_user(username=self.username, email='test@example.com', password=self.password)
        Perfil.objects.create(user=self.user, rol=Perfil.Rol.FREE_USER)  # Añadir perfil

    def test_usuario_puede_iniciar_sesion(self):
        response = self.client.get(reverse('login'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'usuarios/login.html')

        response = self.client.post(reverse('login'), {
            'username': self.username,
            'password': self.password
        }, follow=True)

        self.assertRedirects(response, reverse('dashboard'))
        user = response.context['user']
        self.assertTrue(user.is_authenticated)
        self.assertEqual(user.username, self.username)
