# Generated by Django 4.2.7 on 2023-11-20 16:46

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app_tienda_electronica', '0002_producto_imagen'),
    ]

    operations = [
        migrations.AddField(
            model_name='cliente',
            name='contrasena',
            field=models.CharField(default='12345', max_length=255),
        ),
    ]
