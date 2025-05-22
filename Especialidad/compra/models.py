from django.db import models

class Compra(models.Model):

    nombre = models.CharField(max_length=100)
    producto = models.CharField(max_length=20)
    autenticacion = models.BooleanField(default=False)
    tiempo_envio = models.CharField(max_length=50)

    def __str__(self):
        return self.nombre
