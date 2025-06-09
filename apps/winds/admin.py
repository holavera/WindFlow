# winds/admin.py
from django.contrib import admin
from .models import Wind

@admin.register(Wind)
class WindAdmin(admin.ModelAdmin):
    list_display = ('titulo', 'perfil', 'pomodoro')
    search_fields = ('titulo', 'perfil__user__username')
    list_filter = ('pomodoro',)
