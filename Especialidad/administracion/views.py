from django.shortcuts import render, redirect, get_object_or_404
from .models import Usuario
from django.contrib.auth.views import LoginView, LogoutView
from django.urls import reverse_lazy
from django.contrib.auth.decorators import login_required
from .forms import CustomUserCreationForm, CustomUserChangeForm, EmailAuthenticationForm
from django.http import JsonResponse, HttpResponseForbidden
from django.db import models
from inventario.models import Producto

@login_required
def usuario_view(request):
    usuarios = Usuario.objects.all()
    form = CustomUserCreationForm()
    return render(request, 'usuarios.html', {'usuarios': usuarios, 'form': form} )

@login_required
def agregar_usuario(request):
    if not (request.user.is_superuser or request.user.position == Usuario.ADMINISTRADOR):
        return HttpResponseForbidden("No tienes permiso para realizar esta acción.")
    if request.method == 'POST':
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            usuario = form.save()
            if request.headers.get('x-requested-with') == 'XMLHttpRequest':
                # Respuesta JSON para AJAX
                return JsonResponse({
                    'success': True,
                    'usuario': {
                        'id': usuario.id,
                        'first_name': usuario.first_name,
                        'email': usuario.email,
                        'phone_number': usuario.phone_number,
                        'position': usuario.position,
                    }
                })
            return redirect('usuarios')
        else:
            if request.headers.get('x-requested-with') == 'XMLHttpRequest':
                return JsonResponse({'success': False, 'errors': form.errors}, status=400)
    else:
        form = CustomUserCreationForm()
    return render(request, 'agregar_usuario.html', {'form': form})

@login_required
def eliminar_usuario(request, user_id):
    if not (request.user.is_superuser or request.user.position == Usuario.ADMINISTRADOR):
        if request.headers.get('x-requested-with') == 'XMLHttpRequest':
            return JsonResponse({'success': False, 'error': 'No tienes permiso para eliminar usuarios.'}, status=403)
        else:
            return HttpResponseForbidden("No tienes permiso para eliminar usuarios.")
    if request.method == 'POST':
        usuario = get_object_or_404(Usuario, id=user_id)
        usuario.delete()
    return redirect('usuarios')

@login_required
def editar_usuario(request, user_id):
    if not (request.user.is_superuser or request.user.position == Usuario.ADMINISTRADOR):
        if request.headers.get('x-requested-with') == 'XMLHttpRequest':
            return JsonResponse({'success': False, 'error': 'No tienes permiso para editar usuarios.'}, status=403)
        else:
            return HttpResponseForbidden("No tienes permiso para editar usuarios.")
    usuario = get_object_or_404(Usuario, id=user_id)
    if request.method == 'POST':
        form = CustomUserChangeForm(request.POST, instance=usuario)
        if form.is_valid():
            form.save()
            if request.headers.get('x-requested-with') == 'XMLHttpRequest':
                return JsonResponse({'success': True})
            return redirect('usuarios')
        else:
            print("Errores de validación en editar_usuario:", form.errors)  # Agregado para debug
            if request.headers.get('x-requested-with') == 'XMLHttpRequest':
                return JsonResponse({'success': False, 'errors': form.errors}, status=400)
    else:
        form = CustomUserChangeForm(instance=usuario)
    return render(request, 'editar_usuario.html', {'form': form, 'usuario': usuario})

@login_required
def historial_actividades(request):
    return render(request, 'historial_actividades.html')

@login_required
def dashboard(request):
    total_stock = Producto.objects.filter(cantidad__isnull=False).aggregate(total=models.Sum('cantidad'))['total'] or 0
    users_activos = Usuario.objects.filter(is_active=True).count()
    productos_bajo_stock = Producto.objects.filter(cantidad__lt=3, cantidad__isnull=False)
    context = {
        'total_stock': total_stock,
        'users_activos': users_activos,
        'productos_bajo_stock': productos_bajo_stock,
    }
    return render(request, 'dashboard.html', context)

class CustomLoginView(LoginView):
    template_name = 'login.html'
    redirect_authenticated_user = True
    form_class = EmailAuthenticationForm

class CustomLogoutView(LogoutView):
    next_page = reverse_lazy('login')
