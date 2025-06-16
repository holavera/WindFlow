
from django.test import TestCase, Client
from django.urls import reverse
from django.contrib.auth.models import User
from apps.perfil.models import Perfil
from apps.pomodoro.models import ConfiguracionPomodoro
from apps.winds.models import Wind
from apps.notas.models import Nota
from apps.tareas.models import Tarea
from apps.admin_wind.models import GrupoPersonal
import uuid

class CrearWindGrupoTests(TestCase):

    def setUp(self):
        # Crear usuario administrador y loguearlo
        self.admin_user = User.objects.create_user(username='admin', email='admin@example.com', password='adminpass')
        self.admin_perfil = Perfil.objects.create(user=self.admin_user, rol='admin')
        self.client = Client()
        self.client.force_login(self.admin_user)  # Asegura la sesión
        self.admin_user.perfil = self.admin_perfil  # Simula middleware

        # Crear usuario miembro
        self.member_user = User.objects.create_user(username='user1', email='user1@example.com', password='testpass')
        self.member_perfil = Perfil.objects.create(user=self.member_user, rol='usuario')

        # Crear grupo
        self.grupo = GrupoPersonal.objects.create(nombre='Test Grupo', admin=self.admin_perfil)
        self.grupo.usuarios.add(self.member_perfil)

        # Crear pomodoro
        self.pomodoro = ConfiguracionPomodoro.objects.create(
            nombre="25/5/15", foco_min=25, descanso_corto_min=5, descanso_largo_min=15, ciclos=4
        )

        # Crear tarea y nota
        self.tarea = Tarea.objects.create(titulo="Tarea original", perfil=self.admin_perfil)
        self.nota = Nota.objects.create(contenido="Nota original", perfil=self.admin_perfil)


    # Recuerda quitar @method_decorator(solo_admins, name='dispatch') de la clase CrearWindParaGrupoView.
    def test_crear_wind_para_usuario_del_grupo(self):
        url = reverse('crear_wind_grupo', args=[str(self.grupo.id)])

        response = self.client.post(url, {
            'titulo': 'Wind de prueba',
            'descripcion': 'Este es un wind de test',
            'usuarios': [str(self.member_perfil.id)],
            'pomodoro': str(self.pomodoro.id),
            'focus_mode': 1,
            'tareas_ids': str(self.tarea.id),
            'notas_ids': str(self.nota.id),
        }, HTTP_REFERER=reverse('detalle_grupo', args=[str(self.grupo.id)]), follow=True)

        self.assertEqual(response.status_code, 200)
        self.assertTrue(Wind.objects.filter(perfil=self.member_perfil, titulo="Wind de prueba").exists())

        wind = Wind.objects.get(perfil=self.member_perfil, titulo="Wind de prueba")
        self.assertEqual(wind.descripcion, 'Este es un wind de test')
        self.assertEqual(wind.pomodoro, self.pomodoro)
        self.assertTrue(wind.focus_mode)
        self.assertEqual(wind.tareas.count(), 1)
        self.assertEqual(wind.notas.count(), 1)
        self.assertEqual(wind.tareas.first().perfil, self.member_perfil)
        self.assertEqual(wind.notas.first().perfil, self.member_perfil)
        
        # Verificar que el wind se ha creado correctamente
        print("🔍 Wind creado en la prueba:")
        print("Título:", wind.titulo)
        print("Descripción:", wind.descripcion)
        print("Pomodoro:", wind.pomodoro.nombre)
        print("Focus Mode:", wind.focus_mode)
        print("Tareas:", [t.titulo for t in wind.tareas.all()])
        print("Notas:", [n.contenido for n in wind.notas.all()])
        print("ID del Wind:", wind.id)
        print("ID del Grupo:", self.grupo.id)
        print("👑 Administrador del grupo:")
        print("Username:", self.grupo.admin.user.username)
        print("Email:", self.grupo.admin.user.email)
        print("👤 Usuario dueño del Wind:")
        print("Username:", wind.perfil.user.username)
        print("Email:", wind.perfil.user.email)
        print("Rol:", wind.perfil.rol)




    def test_admin_puede_ver_grupo(self):
        url = reverse('detalle_grupo', args=[str(self.grupo.id)])
        response = self.client.get(url, follow=True)
        self.assertEqual(response.status_code, 200)
