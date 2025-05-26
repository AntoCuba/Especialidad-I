from django.db import migrations

def populate_proveedor_fk(apps, schema_editor):
    Producto = apps.get_model('inventario', 'Producto')
    Proveedor = apps.get_model('proveedores', 'Proveedor')

    for producto in Producto.objects.all():
        proveedor_name = producto.proveedor
        if proveedor_name:
            try:
                proveedor_obj = Proveedor.objects.get(nombre=proveedor_name)
                producto.proveedor_fk = proveedor_obj
                producto.save()
            except Proveedor.DoesNotExist:
                pass

class Migration(migrations.Migration):

    dependencies = [
        ('inventario', '0003_alter_producto_proveedor'),
    ]

    operations = [
        migrations.RunPython(populate_proveedor_fk),
    ]
