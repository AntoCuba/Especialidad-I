from django.shortcuts import render
from django.shortcuts import render, redirect, get_object_or_404
from .models import Proveedor
from django.views.decorators.csrf import csrf_exempt
from django.http import HttpResponseRedirect
from django.urls import reverse

# Create your views here.
def listar_proveedores(request):
    proveedores = Proveedor.objects.all()
    return render(request, 'listar_proveedores.html', {'proveedores': proveedores})

@csrf_exempt
def agregar_proveedor(request):
    if request.method == 'POST':
        nombre = request.POST.get('nombre')
        producto = request.POST.get('producto')
        autenticacion = request.POST.get('autenticacion', 'off') == 'on'  
        tiempo_envio = request.POST.get('tiempo_envio')

        Proveedor.objects.create(
            nombre=nombre,
            producto=producto,
            autenticacion=autenticacion,
            tiempo_envio=tiempo_envio
        )
        return HttpResponseRedirect(reverse('listar_proveedores'))

@csrf_exempt
def editar_proveedor(request, proveedor_id):
    proveedor = get_object_or_404(Proveedor, id=proveedor_id)
    if request.method == 'POST':
        proveedor.nombre = request.POST.get('nombre')
        proveedor.producto = request.POST.get('producto')
        proveedor.autenticacion = request.POST.get('autenticacion', 'off') == 'on'
        proveedor.tiempo_envio = request.POST.get('tiempo_envio')
        proveedor.save()
        return HttpResponseRedirect(reverse('listar_proveedores'))

@csrf_exempt
def eliminar_proveedor(request, proveedor_id):
    proveedor = get_object_or_404(Proveedor, id=proveedor_id)
    if request.method == 'POST':
        proveedor.delete()
        return HttpResponseRedirect(reverse('listar_proveedores'))
