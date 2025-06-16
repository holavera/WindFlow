#admin_wind/urls.py
from django.urls import path
from .views import EstadisticasAdminView, ListaGruposAdminView, CrearGrupoView, GestionGrupoDetalleView, \
    EliminarUsuarioDeGrupoView, EliminarGrupoView, CrearWindParaGrupoView, EstadisticasGrupoView, \
    ExportarEstadisticasPDFView, HistorialPomodoroAdminView

urlpatterns = [
    path('grupos/', ListaGruposAdminView.as_view(), name='gestion_grupos'),
    path('grupos/crear/', CrearGrupoView.as_view(), name='crear_grupo'),
    path('estadisticas/', EstadisticasAdminView.as_view(), name='estadisticas'),
    path('grupos/<uuid:pk>/', GestionGrupoDetalleView.as_view(), name='detalle_grupo'),
    path('grupos/<uuid:grupo_id>/eliminar-usuario/<int:usuario_id>/', EliminarUsuarioDeGrupoView.as_view(), name='eliminar_usuario_grupo'),
    path('grupos/<uuid:pk>/eliminar/', EliminarGrupoView.as_view(), name='eliminar_grupo'),
    path('grupos/<uuid:grupo_id>/crear-wind/', CrearWindParaGrupoView.as_view(), name='crear_wind_grupo'),
    path('grupos/<uuid:grupo_id>/estadisticas/', EstadisticasGrupoView.as_view(), name='estadisticas_grupo'),
    path('grupos/<uuid:grupo_id>/exportar-pdf/', ExportarEstadisticasPDFView.as_view(), name='exportar_estadisticas_pdf'),
    path('grupos/<uuid:grupo_id>/historial/<int:perfil_id>/', HistorialPomodoroAdminView.as_view(), name='historial_usuario_admin'),
]
