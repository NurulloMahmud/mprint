# Generated by Django 5.0.4 on 2024-05-09 18:03

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0006_inventory'),
    ]

    operations = [
        migrations.AddField(
            model_name='paper',
            name='available_qty',
            field=models.IntegerField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name='paper',
            name='branch',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='main.branch'),
        ),
        migrations.DeleteModel(
            name='PaperStock',
        ),
    ]