from django.db import models
from django.contrib.auth.models import AbstractUser, BaseUserManager
from django.utils.translation import gettext_lazy as _


class Administrador(BaseUserManager):
    def create_user(self, email, password, **extra_fields):
        if not email:
            raise ValueError(_("El email es requerido"))
        
        email = self.normalize_email(email) # aplica lowercase al correo
        user = self.model(email=email, **extra_fields )
        user.username = email

        user.set_password(password) # cifra la contraseña 
        user.save()
        return user
        
    def create_superuser(self, email, password, **extra_fields):
        extra_fields.setdefault("is_superuser", True)
        extra_fields.setdefault("is_staff", True)
        extra_fields.setdefault("is_active", True)
        if extra_fields.get("is_staff") is not True:
            raise ValueError(
                _("Superuser debe tener is_staff=True.")
            )
        if extra_fields.get("is_superuser") is not True:
            raise ValueError(
                _("Superuser debe tener is_superuser=True.")
            )
        return self.create_user(email, password, **extra_fields)

class Usuario(AbstractUser):
    ADMINISTRADOR = 'Administrador'
    SUPERVISOR = 'Supervisor'
    LOGISTICA = 'Logistica'
    INVENTARIO = 'Inventario'

    CARGO_CHOICES = [
        (ADMINISTRADOR, 'Administrador'),
        (SUPERVISOR, 'Supervisor'),
        (LOGISTICA, 'Logistica'),
        (INVENTARIO, 'Inventario'),
    ]

    email = models.EmailField(max_length=50, unique=True)
    phone_number = models.CharField(max_length=12)
    position = models.CharField(max_length=15, choices=CARGO_CHOICES)

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []

    objects = Administrador()

    def __str__(self):
        return self.email
