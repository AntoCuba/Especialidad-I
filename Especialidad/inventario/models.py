from django.db import models

class Producto(models.Model):
    nombre_producto = models.CharField(max_length=100)
    numero_orden = models.CharField(max_length=50, blank=True, null=True)
    valor_producto_unidad = models.DecimalField(max_digits=10, decimal_places=2, blank=True, null=True)
    talla = models.CharField(max_length=10)
    numero_tracking = models.CharField(max_length=100, blank=True, null=True)
    proveedor = models.CharField(max_length=100, blank=True, null=True)
    cantidad = models.IntegerField(blank=True, null=True)
    precio_venta = models.DecimalField(max_digits=10, decimal_places=2)
    boleta_factura = models.FileField(upload_to='boletas_facturas/', blank=True, null=True)

    def __str__(self):
        return self.nombre_producto

    def sin_stock(self):
        return not self.cantidad or self.cantidad == 0 #Devuelve true si el stock es 0 y false en caso contrario.
