# Generated by Django 4.1.7 on 2023-02-28 16:06

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('odoo', '0002_service_lat_service_lng_service_service_type'),
    ]

    operations = [
        migrations.AlterField(
            model_name='service',
            name='service_type',
            field=models.IntegerField(choices=[(1, '3 Megas'), (2, '5 Megas')], verbose_name='Tipo de Servicio'),
        ),
    ]