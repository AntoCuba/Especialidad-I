from django.shortcuts import render
from proveedores.models import Proveedor
from django.views.decorators.csrf import csrf_exempt
from django.http import HttpResponseRedirect
from django.urls import reverse

def realizar_compra(request):
    proveedores = Proveedor.objects.all()
    return render(request, 'realizar_compra.html', {'proveedores': proveedores})
