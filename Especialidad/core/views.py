from django.shortcuts import render

def home(request):
    return render(request, 'layout.html')


def productos(request):
    return render(request, 'productos.html')

def listar_proveedores(request):
    return render(request, 'listar_proveedores.html')

def realizar_compra(request):
    return render(request, 'realizar_compra.html')  

def lista_clientes(request):
    return render(request, 'lista_clientes.html')  

def seguimiento_venta(request):
    return render(request, 'seguimiento_venta.html')  

# Create your views here.
