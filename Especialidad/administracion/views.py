from django.shortcuts import render

# Create your views here.

def usuario_view(request):
    return render(request, 'core/usuarios.html')

def historial_actividades(request):
    return render(request, 'historial_actividades.html')

def dashboard(request):
    return render(request, 'dashboard.html')