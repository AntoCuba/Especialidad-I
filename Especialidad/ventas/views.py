from django.shortcuts import render, redirect, get_object_or_404
from .models import Venta, ESTADOS_ENVIO
from django.views.decorators.csrf import csrf_exempt
from django.http import HttpResponseRedirect
from django.urls import reverse
from django.http import HttpResponse



# Listar todas las ventas
def listar_ventas(request):
    ventas = Venta.objects.all()
    return render(request, 'ventas.html', {'ventas': ventas, 'estados_envio': ESTADOS_ENVIO})

# Agregar nueva venta
@csrf_exempt
def agregar_venta(request):
    if request.method == 'POST':
        try:
            id_pedido = int(request.POST.get('id_pedido'))
            monto_total = float(request.POST.get('monto_total'))
        except (ValueError, TypeError):
            return HttpResponse("Datos inválidos", status=400)

        nombre_cliente = request.POST.get('nombre_cliente')
        estado_envio = request.POST.get('estado_envio')

        Venta.objects.create(
            id_pedido=id_pedido,
            nombre_cliente=nombre_cliente,
            monto_total=monto_total,
            estado_envio=estado_envio
        )
        return HttpResponseRedirect(reverse('listar_ventas'))


# Editar una venta existente
@csrf_exempt
def editar_venta(request, venta_id):
    venta = get_object_or_404(Venta, id=venta_id)
    if request.method == 'POST':
        venta.id_pedido = int(request.POST.get('id_pedido', venta.id_pedido))
        venta.nombre_cliente = request.POST.get('nombre_cliente')
        venta.monto_total = float(request.POST.get('monto_total', venta.monto_total))
        venta.estado_envio = request.POST.get('estado_envio')
        venta.save()
        return HttpResponseRedirect(reverse('listar_ventas'))

# Eliminar una venta
@csrf_exempt
def eliminar_venta(request, venta_id):
    venta = get_object_or_404(Venta, id=venta_id)
    if request.method == 'POST':
        venta.delete()
        return HttpResponseRedirect(reverse('listar_ventas'))


def seguimiento_venta(request):
    id_pedido = request.GET.get('id_pedido')

    venta = None
    completadas = []

    if id_pedido:
        try:
            id_pedido_int = int(id_pedido)
            print(f"[DEBUG] ID del pedido recibido: {id_pedido_int}") 

            venta = Venta.objects.get(id_pedido=id_pedido_int)
            estado_actual = venta.estado_envio

            valores_estados = [v for v, l in ESTADOS_ENVIO]

            if estado_actual == 'cancelado':
                completadas = []
            else:
                index_actual = valores_estados.index(estado_actual)
                completadas = valores_estados[:index_actual + 1]

        except ValueError:
            print("[ERROR] ID del pedido no es un número válido.")
            venta = None
        except Venta.DoesNotExist:
            print(f"[ERROR] No se encontró venta con ID de pedido: {id_pedido}")
            venta = None

    context = {
        'venta': venta,
        'completadas': completadas,
        'estados_envio': ESTADOS_ENVIO
    }

    return render(request, 'seguimiento_venta.html', context)
