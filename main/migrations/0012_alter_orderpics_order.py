# Generated by Django 5.0.4 on 2024-05-15 22:33

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0011_rename_sqr_meter_order_total_sqr_meter'),
    ]

    operations = [
        migrations.AlterField(
            model_name='orderpics',
            name='order',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='pics', to='main.order'),
        ),
    ]
