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
from core.views import listar_proveedores, realizar_compra, lista_clientes, seguimiento_venta
from inventario.views import productos, agregar_producto, editar_producto, eliminar_producto
from administracion.views import CustomLoginView
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('admin/', admin.site.urls),
    path('administracion/', include('administracion.urls')),
    path('', CustomLoginView.as_view(), name='login'),
    path('inventario/', productos, name='productos'),
    path('inventario/agregar/', agregar_producto, name='agregar_producto'),
    path('inventario/editar/<int:producto_id>/', editar_producto, name='editar_producto'),
    path('inventario/eliminar/<int:producto_id>/', eliminar_producto, name='eliminar_producto'),
    path('proveedores/', listar_proveedores, name='listar_proveedores'),
    path('compra/', realizar_compra, name='realizar_compra'),
    path('ventas/clientes/', lista_clientes, name='lista_clientes'),
    path('ventas/seguimiento/', seguimiento_venta, name='seguimiento_venta'),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
