from django.urls import path
from . import views

urlpatterns = [
    path('upgrade/', views.upgrade_view, name='upgrade'),
]
