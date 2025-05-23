from django.db import models

class Proveedor(models.Model):

    nombre = models.CharField(max_length=100)
    producto = models.CharField(max_length=20)
    autenticacion = models.BooleanField(default=False)
    tiempo_envio = models.CharField(max_length=50)
    image_url = models.CharField(max_length=200, blank=True, null=True)
    page_url = models.CharField(max_length=200, blank=True, null=True)

    def __str__(self):
        return self.nombre
