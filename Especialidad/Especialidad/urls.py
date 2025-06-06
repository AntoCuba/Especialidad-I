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
from django.conf import settings
from django.conf.urls.static import static

from core.views import (
    listar_proveedores,
    listar_ventas, 
    seguimiento_venta
    )

from inventario.views import productos, agregar_producto, editar_producto, eliminar_producto
from proveedores.views import listar_proveedores, agregar_proveedor, editar_proveedor, eliminar_proveedor
from administracion.views import CustomLoginView
from proveedores.views import agregar_proveedor, editar_proveedor, eliminar_proveedor
from ventas.views import listar_ventas, agregar_venta, editar_venta, eliminar_venta, seguimiento_venta
from django.conf import settings
from django.conf.urls.static import static
from compra.views import realizar_compra

urlpatterns = [
    #Admin
    path('admin/', admin.site.urls),
    path('administracion/', include('administracion.urls')),

    #Login
    path('', CustomLoginView.as_view(), name='login'),

    #Inventario
    path('inventario/', productos, name='productos'),
    path('inventario/agregar/', agregar_producto, name='agregar_producto'),
    path('inventario/editar/<int:producto_id>/', editar_producto, name='editar_producto'),
    path('inventario/eliminar/<int:producto_id>/', eliminar_producto, name='eliminar_producto'),

    #Proveedores
    path('proveedores/', listar_proveedores, name='listar_proveedores'), 
    path('proveedores/agregar/', agregar_proveedor, name='agregar_proveedor'),
    path('proveedores/editar/<int:proveedor_id>/', editar_proveedor, name='editar_proveedor'),
    path('proveedores/eliminar/<int:proveedor_id>/', eliminar_proveedor, name='eliminar_proveedor'),

    #Compra
    path('compra/', realizar_compra, name='realizar_compra'),

    #Venta
    path('ventas/', listar_ventas, name='listar_ventas'),
    path('ventas/agregar/', agregar_venta, name='agregar_venta'),
    path('ventas/editar/<int:venta_id>/', editar_venta, name='editar_venta'),
    path('ventas/eliminar/<int:venta_id>/', eliminar_venta, name='eliminar_venta'),
    path('ventas/seguimiento/', seguimiento_venta, name='seguimiento_venta'),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
