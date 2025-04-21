"""
URL configuration for Especialidad project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include
from core.views import productos, listar_proveedores, realizar_compra, lista_clientes, seguimiento_venta
from administracion.views import CustomLoginView

urlpatterns = [
    path('admin/', admin.site.urls),
    path('administracion/', include('administracion.urls')),
    path('', CustomLoginView.as_view(), name='login'),
    path('inventario/', productos, name='productos'),
    path('proveedores/', listar_proveedores, name='listar_proveedores'),
    path('compra/', realizar_compra, name='realizar_compra'),
    path('ventas/clientes/', lista_clientes, name='lista_clientes'),
    path('ventas/seguimiento/', seguimiento_venta, name='seguimiento_venta'),
]
