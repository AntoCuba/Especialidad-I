from django.shortcuts import render, redirect, get_object_or_404
from .models import Venta, ESTADOS_ENVIO
from inventario.models import Producto
from django.http import HttpResponseRedirect
from django.urls import reverse
import json
from django.core.serializers.json import DjangoJSONEncoder
from administracion.models import ActivityLog

# Listar todas las ventas
def listar_ventas(request):
    ventas = Venta.objects.all()
    productos = Producto.objects.prefetch_related('productotalla_set').all()

    productos_precios = {str(p.id): float(p.precio_venta) for p in productos}
    productos_tallas = {}
    for p in productos:
        productos_tallas[str(p.id)] = [
            {"id": t.id, "talla": t.talla, "cantidad": t.cantidad} for t in p.productotalla_set.all()
        ]

    for venta in ventas:
        venta.formatted_monto_total = f"{venta.monto_total:.2f}"

    context = {
        'ventas': ventas,
        'estados_envio': ESTADOS_ENVIO,
        'productos': productos,
        'productos_precios_json': json.dumps(productos_precios, cls=DjangoJSONEncoder),
        'productos_tallas_json': json.dumps(productos_tallas, cls=DjangoJSONEncoder),
    }
    return render(request, 'ventas.html', context)

# Agregar nueva venta
def agregar_venta(request):
    if request.method == 'POST':
        id_pedido_id = request.POST.get('id_pedido')
        talla_id = request.POST.get('talla')
        nombre_cliente = request.POST.get('nombre_cliente')
        direccion = request.POST.get('direccion')
        email = request.POST.get('email')
        telefono = request.POST.get('telefono')
        monto_total = request.POST.get('monto_total')
        estado_envio = request.POST.get('estado_envio')
        region = request.POST.get('region')


        venta = Venta.objects.create(
            id_pedido_id=id_pedido_id,
            talla_id=talla_id,
            nombre_cliente=nombre_cliente,
            direccion=direccion,
            email=email,
            telefono=telefono,
            monto_total=monto_total,
            estado_envio=estado_envio,
            region=region,
        )

        ActivityLog.objects.create(
            user=request.user if request.user.is_authenticated else None,
            action='add_venta',
            description=f'Venta para cliente {nombre_cliente} creada.'
        )

        return HttpResponseRedirect(reverse('listar_ventas'))
    else:
        productos = Producto.objects.prefetch_related('productotalla_set').all()
        ventas = Venta.objects.all()

        productos_precios = {str(p.id): float(p.precio_venta) for p in productos}
        productos_tallas = {}
        for p in productos:
            productos_tallas[str(p.id)] = [
                {"id": t.id, "talla": t.talla, "cantidad": t.cantidad} for t in p.productotalla_set.all()
            ]

        context = {
            'productos': productos,
            'ventas': ventas,
            'productos_precios_json': json.dumps(productos_precios, cls=DjangoJSONEncoder),
            'productos_tallas_json': json.dumps(productos_tallas, cls=DjangoJSONEncoder),
        }
        return render(request, 'ventas.html', context)

def editar_venta(request, venta_id):
    venta = get_object_or_404(Venta, pk=venta_id)
    if request.method == 'POST':
        venta.id_pedido_id = request.POST.get('id_pedido')
        venta.talla_id = request.POST.get('talla')
        venta.nombre_cliente = request.POST.get('nombre_cliente')
        venta.direccion = request.POST.get('direccion')
        venta.email = request.POST.get('email')
        venta.telefono = request.POST.get('telefono')
        venta.monto_total = request.POST.get('monto_total')
        venta.estado_envio = request.POST.get('estado_envio')
        venta.save()

        ActivityLog.objects.create(
            user=request.user if request.user.is_authenticated else None,
            action='edit_venta',
            description=f'Venta para cliente {venta.nombre_cliente} editada.'
        )

        return HttpResponseRedirect(reverse('listar_ventas'))
    else:
        productos = Producto.objects.prefetch_related('productotalla_set').all()
        productos_precios = {str(p.id): float(p.precio_venta) for p in productos}
        productos_tallas = {}
        for p in productos:
            productos_tallas[str(p.id)] = [
                {"id": t.id, "talla": t.talla, "cantidad": t.cantidad} for t in p.productotalla_set.all()
            ]
        venta.formatted_monto_total = f"{venta.monto_total:.2f}"
        context = {
            'venta': venta,
            'productos': productos,
            'productos_precios_json': json.dumps(productos_precios, cls=DjangoJSONEncoder),
            'productos_tallas_json': json.dumps(productos_tallas, cls=DjangoJSONEncoder),
        }
        return render(request, 'ventas.html', context)

def eliminar_venta(request, venta_id):
    venta = get_object_or_404(Venta, pk=venta_id)
    if request.method == 'POST':
        nombre_cliente = venta.nombre_cliente
        venta.delete()
        ActivityLog.objects.create(
            user=request.user if request.user.is_authenticated else None,
            action='delete_venta',
            description=f'Venta para cliente {nombre_cliente} eliminada.'
        )
        return HttpResponseRedirect(reverse('listar_ventas'))
