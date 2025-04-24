from django.shortcuts import render, redirect, get_object_or_404
from .models import Producto
from django.views.decorators.csrf import csrf_exempt
from django.http import HttpResponseRedirect
from django.urls import reverse

def productos(request):
    productos = Producto.objects.all()
    return render(request, 'productos.html', {'productos': productos})

@csrf_exempt
def agregar_producto(request):
    if request.method == 'POST':
        nombre_producto = request.POST.get('nombre_producto')
        numero_orden = request.POST.get('numero_orden')
        valor_producto_unidad = request.POST.get('valor_producto_unidad')
        numero_tracking = request.POST.get('numero_tracking')
        proveedor = request.POST.get('proveedor')
        cantidad = request.POST.get('cantidad')
        precio_venta = request.POST.get('precio_venta')
        talla = request.POST.get('talla')
        boleta_factura = request.FILES.get('boleta_factura')

        Producto.objects.create(
            nombre_producto=nombre_producto,
            numero_orden=numero_orden,
            valor_producto_unidad=valor_producto_unidad,
            numero_tracking=numero_tracking,
            proveedor=proveedor,
            cantidad=cantidad,
            precio_venta=precio_venta,
            talla=talla,
            boleta_factura=boleta_factura
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
        producto.proveedor = request.POST.get('proveedor')
        producto.cantidad = request.POST.get('cantidad')
        producto.precio_venta = request.POST.get('precio_venta')
        producto.talla = request.POST.get('talla')
        boleta_factura = request.FILES.get('boleta_factura')
        if boleta_factura:
            producto.boleta_factura = boleta_factura
        producto.save()
        return HttpResponseRedirect(reverse('productos'))

@csrf_exempt
def eliminar_producto(request, producto_id):
    producto = get_object_or_404(Producto, id=producto_id)
    if request.method == 'POST':
        producto.delete()
        return HttpResponseRedirect(reverse('productos'))
