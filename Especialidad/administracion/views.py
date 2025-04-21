from django.shortcuts import render, redirect
from .models import Usuario
from django.contrib.auth.views import LoginView, LogoutView
from django.urls import reverse_lazy
from .forms import CustomUserCreationForm
from django.contrib.auth.decorators import login_required
from .forms import CustomUserCreationForm

@login_required
def usuario_view(request):
    usuarios = Usuario.objects.all()
    form = CustomUserCreationForm()
    return render(request, 'usuarios.html', {'usuarios': usuarios, 'form': form} )

from django.http import JsonResponse

@login_required
def agregar_usuario(request):
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
def historial_actividades(request):
    return render(request, 'historial_actividades.html')

@login_required
def dashboard(request):
    return render(request, 'dashboard.html')

from .forms import EmailAuthenticationForm

class CustomLoginView(LoginView):
    template_name = 'login.html'
    redirect_authenticated_user = True
    form_class = EmailAuthenticationForm

class CustomLogoutView(LogoutView):
    next_page = reverse_lazy('login')
