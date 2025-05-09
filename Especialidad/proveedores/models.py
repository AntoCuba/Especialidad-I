from django.db import models

class Proveedor(models.Model):
    nombre_proveedor = models.CharField(max_length=100)
    marcas_principales = models.CharField(max_length=50, blank=True, null=True)
    metodo_pago = models.CharField(max_length=10)
    tiempo_envio = models.CharField(max_length=100, blank=True, null=True)
    descripcion = models.CharField(max_length=200, blank=True, null=True)

    def __str__(self):
        return self.nombre_proveedores

