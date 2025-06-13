from django.shortcuts import render
from django.shortcuts import render, redirect, get_object_or_404
from .models import Proveedor
from django.views.decorators.csrf import csrf_exempt
from django.http import HttpResponseRedirect
from django.urls import reverse
from administracion.models import ActivityLog
from django.core.paginator import Paginator
from django.db.models import Q

def listar_proveedores(request):
    query = request.GET.get('q', '')
    proveedores = Proveedor.objects.all()
    if query:
        proveedores = proveedores.filter(
            Q(nombre__icontains=query) |
            Q(producto__icontains=query) |
            Q(descripcion__icontains=query)
        ).distinct()
    return render(request, 'listar_proveedores.html', {'proveedores': proveedores, 'search_query': query})

@csrf_exempt
def agregar_proveedor(request):
    if request.method == 'POST':
        nombre = request.POST.get('nombre')
        producto = request.POST.get('producto')
        autenticacion = request.POST.get('autenticacion', 'off') == 'on'  
        tiempo_envio = request.POST.get('tiempo_envio')
        url_pagina = request.POST.get('url_pagina')
        url_imagen = request.POST.get('url_imagen')
        descripcion = request.POST.get('descripcion', '')

        Proveedor.objects.create(
            nombre=nombre,
            producto=producto,
            autenticacion=autenticacion,
            tiempo_envio=tiempo_envio,
            url_pagina=url_pagina,
            url_imagen=url_imagen,
            descripcion=descripcion
        )
        ActivityLog.objects.create(
            user=request.user if request.user.is_authenticated else None,
            action='add_proveedor',
            description=f'Proveedor {nombre} creado.'
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
        proveedor.url_pagina = request.POST.get('url_pagina')
        proveedor.url_imagen = request.POST.get('url_imagen')
        proveedor.descripcion = request.POST.get('descripcion', '')
        proveedor.save()
        ActivityLog.objects.create(
            user=request.user if request.user.is_authenticated else None,
            action='edit_proveedor',
            description=f'Proveedor {proveedor.nombre} editado.'
        )

        return HttpResponseRedirect(reverse('listar_proveedores'))

@csrf_exempt
def eliminar_proveedor(request, proveedor_id):
    proveedor = get_object_or_404(Proveedor, id=proveedor_id)
    if request.method == 'POST':
        nombre = proveedor.nombre
        proveedor.delete()
        ActivityLog.objects.create(
            user=request.user if request.user.is_authenticated else None,
            action='delete_proveedor',
            description=f'Proveedor {nombre} eliminado.'
        )
        return HttpResponseRedirect(reverse('listar_proveedores'))

