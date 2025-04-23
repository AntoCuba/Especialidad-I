from django.urls import path
from . import views
from django.contrib.auth import views as auth_views

urlpatterns=[
    path('productos/', views.productos_view, name='productos'),
    path('productos/agregar/', views.agregar_producto, name='agregar_producto'),
    path('productos/eliminar/<int:user_id>/', views.eliminar_producto, name='eliminar_producto'),
    path('productos/editar/<int:user_id>/', views.editar_producto, name='editar_producto'),

]
