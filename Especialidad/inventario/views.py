from django.shortcuts import render, redirect, get_object_or_404
from .models import Producto, ProductoTalla
from django.views.decorators.csrf import csrf_exempt
from django.http import HttpResponseRedirect
from django.urls import reverse
from django.db.models import Q
from administracion.models import ActivityLog

def productos(request):
    productos = Producto.objects.all()
    low_stock_products = Producto.objects.filter(productotalla__cantidad__lt=2).distinct()
    return render(request, 'productos.html', {'productos': productos, 'low_stock_products': low_stock_products})

@csrf_exempt
def agregar_producto(request):
    if request.method == 'POST':
        nombre_producto = request.POST.get('nombre_producto')
        numero_orden = request.POST.get('numero_orden')
        valor_producto_unidad = request.POST.get('valor_producto_unidad')
        numero_tracking = request.POST.get('numero_tracking')
        proveedor_id = request.POST.get('proveedor')
        precio_venta = request.POST.get('precio_venta')
        boleta_factura = request.FILES.get('boleta_factura')

        proveedor_fk = None
        if proveedor_id:
            from proveedores.models import Proveedor
            try:
                proveedor_fk = Proveedor.objects.get(id=proveedor_id)
            except Proveedor.DoesNotExist:
                proveedor_fk = None

        producto = Producto.objects.create(
            nombre_producto=nombre_producto,
            numero_orden=numero_orden,
            valor_producto_unidad=valor_producto_unidad,
            numero_tracking=numero_tracking,
            proveedor_fk=proveedor_fk,
            precio_venta=precio_venta,
            boleta_factura=boleta_factura
        )

        tallas = request.POST.getlist('talla[]')
        cantidades = request.POST.getlist('cantidad[]')

        for talla, cantidad in zip(tallas, cantidades):
            if talla and cantidad:
                if talla.isdigit():
                    talla = talla + " US"
                ProductoTalla.objects.create(
                    producto=producto,
                    talla=talla,
                    cantidad=int(cantidad)
                )
        ActivityLog.objects.create(
            user=request.user if request.user.is_authenticated else None,
            action='add_producto',
            description=f'Producto {nombre_producto} creado.'
        )

        return HttpResponseRedirect(reverse('productos'))

@csrf_exempt
def editar_producto(request, producto_id):
    producto = get_object_or_404(Producto, id=producto_id)
    if request.method == 'POST':
        producto.nombre_producto = request.POST.get('nombre_producto')
        producto.numero_orden = request.POST.get('numero_orden')
        producto.valor_producto_unidad = request.POST.get('valor_producto_unidad')
        producto.numero_tracking = request.POST.get('numero_tracking')
        proveedor_id = request.POST.get('proveedor')
        proveedor_fk = None
        if proveedor_id:
            try:
                proveedor_fk = Proveedor.objects.get(id=proveedor_id)
            except Proveedor.DoesNotExist:
                proveedor_fk = None
        producto.proveedor_fk = proveedor_fk
        producto.precio_venta = request.POST.get('precio_venta')
        boleta_factura = request.FILES.get('boleta_factura')
        if boleta_factura:
            producto.boleta_factura = boleta_factura
        producto.save()

        ProductoTalla.objects.filter(producto=producto).delete()
        tallas = request.POST.getlist('talla[]')
        cantidades = request.POST.getlist('cantidad[]')

        for talla, cantidad in zip(tallas, cantidades):
            if talla and cantidad:
                if talla.isdigit():
                    talla = talla + "US"
                ProductoTalla.objects.create(
                    producto=producto,
                    talla=talla,
                    cantidad=int(cantidad)
                )
        ActivityLog.objects.create(
            user=request.user if request.user.is_authenticated else None,
            action='edit_producto',
            description=f'Producto {producto.nombre_producto} editado.'
        )

        return HttpResponseRedirect(reverse('productos'))

@csrf_exempt
def eliminar_producto(request, producto_id):
    producto = get_object_or_404(Producto, id=producto_id)
    if request.method == 'POST':
        nombre_producto = producto.nombre_producto
        producto.delete()
        ActivityLog.objects.create(
            user=request.user if request.user.is_authenticated else None,
            action='delete_producto',
            description=f'Producto {nombre_producto} eliminado.'
        )
        return HttpResponseRedirect(reverse('productos'))
