# Generated by Django 4.2.13 on 2024-05-27 19:03

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0023_remove_inventory_price_remove_paper_name_and_more'),
    ]

    operations = [
        migrations.DeleteModel(
            name='InventoryExpense',
        ),
    ]