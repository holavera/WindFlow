"""
windflow/uels.py
URL configuration for windflow project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path

from django.contrib import admin
from django.urls import path, include
from .views import home

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', home, name='home'),
    path('usuarios/', include('apps.usuarios.urls')),
    path('tareas/', include('apps.tareas.urls')),
    path('notas/', include('apps.notas.urls')),
    path('pomodoro/', include('apps.pomodoro.urls')),
    path('winds/', include('apps.winds.urls')),
    path('admin-wind/', include('apps.admin_wind.urls')),
    path('perfil/', include('apps.perfil.urls')),  # upgrade

]
