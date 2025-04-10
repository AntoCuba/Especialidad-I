from django.urls import path
from . import views

urlpatterns=[
    path('usuarios/', views.usuario_view, name='usuarios'),
    path('historial/', views.historial_actividades, name='historial_actividades'),
    path('/', views.dashboard, name='dashboard'),
]