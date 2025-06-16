#usuarios/urls.py
from django.urls import path
from .views import logout_view, GuestView, DashboardSuscritoView, estadisticas_usuario, exportar_notas_pdf, \
    exportar_tareas_pdf, exportar_estadisticas_pdf
from .views import RegisterView, CustomLoginView, DashboardView

urlpatterns = [
    path('register/', RegisterView.as_view(), name='register'),
    path('login/', CustomLoginView.as_view(), name='login'),
    path('logout/', logout_view, name='logout'),
    path('dashboard/', DashboardView.as_view(), name='dashboard'),
    path('guest/', GuestView.as_view(), name='guest_mode'),
    path('dashboard/suscrito/', DashboardSuscritoView.as_view(), name='dashboard_suscrito'),
    path('dashboard/estadisticas/', estadisticas_usuario, name='estadisticas_usuario'),
    path('exportar/notas/', exportar_notas_pdf, name='exportar_notas_pdf'),
    path('exportar/tareas/', exportar_tareas_pdf, name='exportar_tareas_pdf'),
    path('exportar/estadisticas/', exportar_estadisticas_pdf, name='exportar_estadisticas_pdf'),
]
