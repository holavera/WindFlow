from django.urls import path
from . import views
from .views import tarea_ajax_form, editar_tarea_ajax, eliminar_tarea_ajax

urlpatterns = [
    path('', views.user_tareas, name='user_tareas'),
    path('editar/<uuid:tarea_id>/', views.editar_tarea, name='editar_tarea'),
    path('eliminar/<uuid:tarea_id>/', views.eliminar_tarea, name='eliminar_tarea'),
    path('actualizar-estado/', views.actualizar_estado_tarea, name='actualizar_estado_tarea'),
    path('ajax/crear/', tarea_ajax_form, name='tarea_ajax_form'),
    path('ajax/editar/', editar_tarea_ajax, name='editar_tarea_ajax'),
    path('ajax/eliminar/', eliminar_tarea_ajax, name='eliminar_tarea_ajax'),
]
