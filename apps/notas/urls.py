# notas/urls.py

from django.urls import path
from .views import nota_ajax_form, editar_nota_ajax, eliminar_nota_ajax
from .views_guest import GuestNotasView, EliminarNotaGuestView, EditarNotaGuestView
from . import views

urlpatterns = [
    path('', views.user_notas, name='user_notas'),
    path('editar/<uuid:nota_id>/', views.editar_nota, name='editar_nota'),
    path('eliminar/<uuid:nota_id>/', views.eliminar_nota, name='eliminar_nota'),
    path('guest/', GuestNotasView.as_view(), name='guest_notas'),
    path('guest/eliminar/', EliminarNotaGuestView.as_view(), name='eliminar_nota_guest'),
    path('guest/editar/<str:nota_id>/', EditarNotaGuestView.as_view(), name='editar_nota_guest'),
    path('ajax/crear/', nota_ajax_form, name='nota_ajax_form'),
    path('ajax/editar/', editar_nota_ajax, name='editar_nota_ajax'),
    path('ajax/eliminar/', eliminar_nota_ajax, name='eliminar_nota_ajax'),

]
