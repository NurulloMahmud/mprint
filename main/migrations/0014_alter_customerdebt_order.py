# Generated by Django 5.0.4 on 2024-05-15 23:31

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0013_order_num_of_product_per_list'),
    ]

    operations = [
        migrations.AlterField(
            model_name='customerdebt',
            name='order',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='debt', to='main.order'),
        ),
    ]
