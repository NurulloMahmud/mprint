# Generated by Django 5.0.4 on 2024-05-18 16:56

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0017_order_lists_per_paper'),
    ]

    operations = [
        migrations.AlterField(
            model_name='serviceorder',
            name='order',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='services', to='main.order'),
        ),
    ]