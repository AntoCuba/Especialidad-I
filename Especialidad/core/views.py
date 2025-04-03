from django.shortcuts import render

def home(request):
    return render(request, 'layout.html')

def about(request):
    return render(request, 'about.html')

def usuarios(request):
    return render(request, 'usuarios.html')

def historial_actividades(request):
    return render(request, 'historial_actividades.html')

def dashboard(request):
    return render(request, 'dashboard.html')

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
