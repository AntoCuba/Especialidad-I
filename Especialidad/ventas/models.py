from django.db import models

ESTADOS_ENVIO = [
    ('proceso', 'En Proceso'),
    ('enviado', 'Enviado'),
    ('entregado', 'Entregado'),
    ('cancelado', 'Cancelado'),
]

class Venta(models.Model):
    id_pedido = models.PositiveIntegerField(unique=True,null=True, verbose_name="ID del Pedido")
    nombre_cliente = models.CharField(max_length=100)
    monto_total = models.DecimalField(max_digits=10, decimal_places=2)
    estado_envio = models.CharField(max_length=10, choices=ESTADOS_ENVIO)
    fecha_compra = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Pedido #{self.id_pedido} - {self.nombre_cliente}"
