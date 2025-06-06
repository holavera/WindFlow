from django.urls import path
from . import views
from .views import cancelar_suscripcion

urlpatterns = [
    path('upgrade/', views.upgrade_view, name='upgrade'),
    path('pago/completado/', views.pago_completado, name='pago_completado'),
    path('cancelar/', cancelar_suscripcion, name='cancelar_suscripcion'),
]
