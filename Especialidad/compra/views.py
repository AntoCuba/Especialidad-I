from django.shortcuts import render
from proveedores.models import Proveedor
from django.views.decorators.csrf import csrf_exempt
from django.http import HttpResponseRedirect
from django.urls import reverse
from django.core.paginator import Paginator


def realizar_compra(request):
    proveedores = Proveedor.objects.all()
    paginador = Paginator(proveedores, 10)
    
    num_pagina = request.GET.get('page')
    page_obj = paginador.get_page(num_pagina)
    return render(request, 'realizar_compra.html', {'page_obj': page_obj})
