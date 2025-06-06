from django.db import models

class Proveedor(models.Model):

    nombre = models.CharField(max_length=100)
    producto = models.CharField(max_length=50)
    autenticacion = models.BooleanField(default=False)
    tiempo_envio = models.CharField(max_length=50)
    url_imagen = models.CharField(max_length=200, blank=True, null=True)
    url_pagina = models.CharField(max_length=200, blank=True, null=True)
    descripcion = models.TextField(blank=True, null=True)

    def __str__(self):
        return self.nombre
