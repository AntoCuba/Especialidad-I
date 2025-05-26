from django.db import models
from inventario.models import Producto, ProductoTalla
from django.core.validators import RegexValidator, EmailValidator

ESTADOS_ENVIO = [
    ('proceso', 'En Proceso'),
    ('enviado', 'Enviado'),
    ('entregado', 'Entregado'),
    ('cancelado', 'Cancelado'),
]

REGIONES = [
    ('arica_parinacota', 'Región de Arica y Parinacota'),
    ('tarapaca', 'Región de Tarapacá'),
    ('antofagasta', 'Región de Antofagasta'),
    ('atacama', 'Región de Atacama'),
    ('coquimbo', 'Región de Coquimbo'),
    ('valparaiso', 'Región de Valparaíso'),
    ('metropolitana', 'Región Metropolitana'),
    ('ohiggins', 'Región de O’Higgins'),
    ('maule', 'Región del Maule'),
    ('nuble', 'Región del Ñuble'),
    ('biobio', 'Región de Biobío'),
    ('araucania', 'Región de La Araucanía'),
    ('rios', 'Región de Los Ríos'),
    ('lagos', 'Región de Los Lagos'),
    ('aysen', 'Región de Aysén'),
    ('magallanes', 'Región de Magallanes'),
]

class Venta(models.Model):
    id_pedido = models.PositiveIntegerField(unique=True,null=False, verbose_name="ID del Pedido")
    id_pedido = models.ForeignKey(Producto, on_delete=models.SET_NULL, null=True, blank=True, verbose_name="ID del Pedido")
    talla = models.ForeignKey(ProductoTalla, on_delete=models.SET_NULL, null=True, blank=True, verbose_name="Talla")
    nombre_cliente = models.CharField(max_length=100)
    direccion = models.CharField(max_length=255, verbose_name="Dirección")
    email = models.EmailField(max_length=254, validators=[EmailValidator()], verbose_name="Correo Electrónico")
    telefono = models.CharField(
        max_length=20,
        validators=[RegexValidator(regex=r'^\+?1?\d{9,15}$', message="Número de teléfono inválido.")],
        verbose_name="Teléfono"
    )
    monto_total = models.DecimalField(max_digits=10, decimal_places=2)
    estado_envio = models.CharField(max_length=10, choices=ESTADOS_ENVIO)
    region = models.CharField(max_length=30, choices=REGIONES, verbose_name="Región")
    fecha_compra = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Pedido #{self.id_pedido} - {self.nombre_cliente}"

