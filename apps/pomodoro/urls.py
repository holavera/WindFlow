from django.urls import path
from . import views
from .views import GuestPomodoroView

urlpatterns = [
    path('guest/', GuestPomodoroView.as_view(), name='guest_pomodoro'),
    path('', views.user_pomodoro, name='user_pomodoro'),
    path('iniciar/', views.iniciar_pomodoro, name='iniciar_pomodoro'),
    path('finalizar/', views.finalizar_pomodoro, name='finalizar_pomodoro'),
    path('historial/', views.historial_pomodoros, name='historial_pomodoros'),
    path('configurar/', views.seleccionar_configuracion, name='seleccionar_configuracion'),
]
