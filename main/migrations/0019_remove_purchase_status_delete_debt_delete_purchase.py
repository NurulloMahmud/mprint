# Generated by Django 5.0.4 on 2024-05-20 11:39

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0018_alter_serviceorder_order'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='purchase',
            name='status',
        ),
        migrations.DeleteModel(
            name='Debt',
        ),
        migrations.DeleteModel(
            name='Purchase',
        ),
    ]
