# Generated by Django 4.2.7 on 2023-11-22 19:53

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('app_tienda_electronica', '0008_metodopago'),
    ]

    operations = [
        migrations.RenameField(
            model_name='metodopago',
            old_name='metodo_pago_token',
            new_name='numero_tarjeta',
        ),
    ]