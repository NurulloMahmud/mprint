# Generated by Django 4.2.13 on 2024-11-20 21:32

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='orderpayment',
            name='date',
            field=models.DateField(default=datetime.date.today),
        ),
    ]
