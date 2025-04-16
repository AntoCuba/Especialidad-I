from django.shortcuts import render
from .models import Usuario

# Create your views here.

def usuario_view(request):
    usuarios = Usuario.objects.all()
    return render(request, 'usuarios.html', {'usuarios': usuarios} )

def historial_actividades(request):
    return render(request, 'historial_actividades.html')

def dashboard(request):
    return render(request, 'dashboard.html')