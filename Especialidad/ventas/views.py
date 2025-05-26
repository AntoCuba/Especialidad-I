from django.shortcuts import render, redirect, get_object_or_404
from .models import Venta, ESTADOS_ENVIO
from inventario.models import Producto
from django.http import HttpResponseRedirect
from django.urls import reverse
from django.http import HttpResponse
import json
from django.core.serializers.json import DjangoJSONEncoder
from django.views.decorators.csrf import csrf_exempt
from administracion.models import ActivityLog
from django.core.paginator import Paginator


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
        try:
            id_pedido = int(request.POST.get('id_pedido'))
            monto_total = float(request.POST.get('monto_total'))
        except (ValueError, TypeError):
            return HttpResponse("Datos inválidos", status=400)

        nombre_cliente = request.POST.get('nombre_cliente')
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



# Editar una venta existente
@csrf_exempt
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


def seguimiento_venta(request):
    id_venta = request.GET.get('id_venta')

    venta = None
    completadas = []

    if id_venta:
        try:
            id_venta_int = int(id_venta)

            venta = Venta.objects.get(id=id_venta_int)

            estado_actual = venta.estado_envio
            valores_estados = [v for v, l in ESTADOS_ENVIO]

            if estado_actual == 'cancelado':
                completadas = []
            else:
                index_actual = valores_estados.index(estado_actual)
                completadas = valores_estados[:index_actual + 1]

        except ValueError:
            print("[ERROR] ID de la venta no es un número válido.")
            venta = None
        except Venta.DoesNotExist:
            print(f"[ERROR] No se encontró venta con ID: {id_venta}")
            venta = None

    context = {
        'venta': venta,
        'completadas': completadas,
        'estados_envio': ESTADOS_ENVIO
    }

    return render(request, 'seguimiento_venta.html', context)
