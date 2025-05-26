from django.db import migrations, models

class Migration(migrations.Migration):

    dependencies = [
        ('inventario', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='producto',
            name='precio_venta',
            field=models.DecimalField(max_digits=10, decimal_places=2),
        ),
    ]
