from django.shortcuts import render, redirect, get_object_or_404
from .models import Usuario, ActivityLog
from django.contrib.auth.views import LoginView, LogoutView
from django.urls import reverse_lazy
from django.contrib.auth.decorators import login_required
from .forms import CustomUserCreationForm, CustomUserChangeForm, EmailAuthenticationForm
from django.http import JsonResponse, HttpResponseForbidden
from inventario.models import Producto, ProductoTalla
from proveedores.models import Proveedor
from django.db.models import Sum
from django.utils.timezone import localtime, now
from ventas.models import Venta
from django.db.models.functions import ExtractMonth
import json

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
            ActivityLog.objects.create(
                user=request.user,
                action='add',
                description=f'Usuario {usuario.email} creado.'
            )
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
        email = usuario.email
        usuario.delete()
        ActivityLog.objects.create(
            user=request.user,
            action='delete',
            description=f'Usuario {email} eliminado.'
        )
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
def api_activity_logs(request):
    if request.GET.get('distinct_users'):
        users = ActivityLog.objects.select_related('user').values_list('user__first_name', 'user__email').distinct()
        user_list = []
        for first_name, email in users:
            user_list.append(first_name or email)
        return JsonResponse({'users': user_list})

    logs = ActivityLog.objects.select_related('user').all()

    data = []
    for log in logs:
        data.append({
            'user': log.user.first_name or log.user.email,
            'action': log.get_action_display(),
            'description': log.description,
            'timestamp': localtime(log.timestamp).strftime('%d %B - %H:%M'),
        })
    return JsonResponse({
        'logs': data,
    })

@login_required
def dashboard(request):
    total_stock = Producto.objects.annotate(
        total_cantidad=Sum('productotalla__cantidad')
    ).aggregate(total=Sum('total_cantidad'))['total'] or 0

    users_activos = Usuario.objects.filter(is_active=True).count()
    productos_bajo_stock = ProductoTalla.objects.filter(cantidad__lt=3).select_related('producto')

    ventas_en_proceso_count = Venta.objects.filter(estado_envio='proceso').count()
    current_year = now().year
    monthly_sales = (
        Venta.objects
        .filter(fecha_compra__year=current_year)
        .exclude(estado_envio='cancelado')
        .annotate(month=ExtractMonth('fecha_compra'))
        .values('month')
        .annotate(total=Sum('monto_total'))
        .order_by('month')
    )
    ventas_mensuales = [0] * 12
    for entry in monthly_sales:
        month_index = entry['month'] - 1
        ventas_mensuales[month_index] = float(entry['total'])

    proveedores = Proveedor.objects.all()
    context = {
        'total_stock': total_stock,
        'users_activos': users_activos,
        'productos_bajo_stock': productos_bajo_stock,
        'pedidos_pendientes_total': ventas_en_proceso_count,
        'ventas_mensuales': json.dumps(ventas_mensuales),
        'proveedores': proveedores,
    }
    return render(request, 'dashboard.html', context)

class CustomLoginView(LoginView):
    template_name = 'login.html'
    redirect_authenticated_user = True
    form_class = EmailAuthenticationForm

    def form_valid(self, form):
        response = super().form_valid(form)
        ActivityLog.objects.create(
            user=self.request.user,
            action='login',
            description='Inició sesión'
        )
        return response

class CustomLogoutView(LogoutView):
    next_page = reverse_lazy('login')

    def dispatch(self, request, *args, **kwargs):
        if request.user.is_authenticated:
            ActivityLog.objects.create(
                user=request.user,
                action='logout',
                description='Cerró sesión'
            )
        return super().dispatch(request, *args, **kwargs)
