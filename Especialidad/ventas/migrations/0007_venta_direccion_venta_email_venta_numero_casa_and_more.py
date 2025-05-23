# Generated by Django 5.2 on 2025-05-24 00:56

import django.core.validators
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('ventas', '0006_venta_talla'),
    ]

    operations = [
        migrations.AddField(
            model_name='venta',
            name='direccion',
            field=models.CharField(default='', max_length=255, verbose_name='Dirección'),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='venta',
            name='email',
            field=models.EmailField(default='', max_length=254, validators=[django.core.validators.EmailValidator()], verbose_name='Correo Electrónico'),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='venta',
            name='numero_casa',
            field=models.CharField(default='', max_length=20, verbose_name='Número de Casa/Departamento'),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='venta',
            name='telefono',
            field=models.CharField(default='', max_length=20, validators=[django.core.validators.RegexValidator(message='Número de teléfono inválido.', regex='^\\+?1?\\d{9,15}$')], verbose_name='Teléfono'),
            preserve_default=False,
        ),
    ]
