from django.urls import path
from . import views

urlpatterns = [
    path('', views.user_winds, name='user_winds'),
    path('crear/', views.crear_wind, name='crear_wind'),
    path('editar/<uuid:wind_id>/', views.editar_wind, name='editar_wind'),
    path('ver/<uuid:wind_id>/', views.ver_wind, name='user_wind'),
    path('eliminar/<uuid:wind_id>/', views.eliminar_wind, name='eliminar_wind'),
]
