from django.shortcuts import render, redirect, get_object_or_404
from .models import Proveedor
from django.views.decorators.csrf import csrf_exempt
from django.http import HttpResponseRedirect
from django.urls import reverse

def listar_proveedores(request):
    listar_proveedores = Proveedor.objects.all()
    return render(request, 'listar_proveedores.html', {'listar_proveedores': listar_proveedores})

@csrf_exempt
def agregar_proveedor(request):
    if request.method == 'POST':
        nombre_proveedor = request.POST.get('nombre_proveedor')
        marcas_principales = request.POST.get('marcas_principales')
        metodo_pago= request.POST.get('metodo_pago')
        tiempo_envio = request.POST.get('tiempo_envio')
        descripcion = request.POST.get('descripcion')

        Proveedor.objects.create(
            nombre_proveedor=nombre_proveedor,
            marcas_principales=marcas_principales,
            metodo_pago=metodo_pago,
            tiempo_envio=tiempo_envio,
            descripcion=descripcion,
        )
        return HttpResponseRedirect(reverse('listar_proveedores'))

@csrf_exempt
def editar_proveedor(request, proveedor_id):
    proveedor = get_object_or_404(proveedor, id=proveedor_id)
    if request.method == 'POST':
        proveedor.nombre_proveedor = request.POST.get('nombre_proveedor')
        proveedor.marcas_principales = request.POST.get('marcas_principales')
        proveedor.metodo_pago= request.POST.get('metodo_pago')
        proveedor.tiempo_envio = request.POST.get('tiempo_envio')
        proveedor.descripcion = request.POST.get('descripcion')
        return HttpResponseRedirect(reverse('proveedores'))

@csrf_exempt
def eliminar_proveedor(request, proveedor_id):
    proveedor = get_object_or_404(proveedor, id=proveedor_id)
    if request.method == 'POST':
        proveedor.delete()
        return HttpResponseRedirect(reverse('proveedores'))
