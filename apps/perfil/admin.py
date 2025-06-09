from django.contrib import admin
from .models import Perfil
from django.contrib.auth.models import User
from django.contrib.auth.admin import UserAdmin

class PerfilInline(admin.StackedInline):
    model = Perfil
    can_delete = False
    verbose_name_plural = 'Perfil'

class CustomUserAdmin(UserAdmin):
    inlines = (PerfilInline,)

# Reemplazamos el admin por defecto de User con uno que incluye Perfil
admin.site.unregister(User)
admin.site.register(User, CustomUserAdmin)
