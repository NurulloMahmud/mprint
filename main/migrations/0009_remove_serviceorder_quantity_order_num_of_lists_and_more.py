# Generated by Django 5.0.4 on 2024-05-13 22:36

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0008_remove_service_price_service_minimum_price_and_more'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='serviceorder',
            name='quantity',
        ),
        migrations.AddField(
            model_name='order',
            name='num_of_lists',
            field=models.IntegerField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name='order',
            name='paper',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='main.paper'),
        ),
        migrations.AddField(
            model_name='order',
            name='possible_defect_list',
            field=models.IntegerField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name='order',
            name='price_per_list',
            field=models.DecimalField(blank=True, decimal_places=2, max_digits=10, null=True),
        ),
        migrations.DeleteModel(
            name='OrderPaper',
        ),
    ]
