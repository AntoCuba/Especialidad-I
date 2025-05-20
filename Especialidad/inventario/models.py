from django.db import models

class Producto(models.Model):
    nombre_producto = models.CharField(max_length=100)
    numero_orden = models.CharField(max_length=50, blank=True, null=True)
    valor_producto_unidad = models.DecimalField(max_digits=10, decimal_places=2, blank=True, null=True)
    numero_tracking = models.CharField(max_length=100, blank=True, null=True)
    proveedor = models.CharField(max_length=100, blank=True, null=True)
    precio_venta = models.DecimalField(max_digits=10, decimal_places=2)
    boleta_factura = models.FileField(upload_to='boletas_facturas/', blank=True, null=True)

    def __str__(self):
        return self.nombre_producto

    def sin_stock(self):
        return not self.productotalla_set.filter(cantidad__gt=0).exists()

    def get_tallas_cantidades_str(self):
        parts = []
        for pt in self.productotalla_set.all():
            parts.append(f"{pt.talla} ({pt.cantidad})")
        return " ; ".join(parts)

class ProductoTalla(models.Model):
    producto = models.ForeignKey(Producto, on_delete=models.CASCADE)
    talla = models.CharField(max_length=10)
    cantidad = models.IntegerField()

    def __str__(self):
        return f"{self.producto.nombre_producto} - Talla: {self.talla} - Cantidad: {self.cantidad}"
