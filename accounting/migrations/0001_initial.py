# Generated by Django 5.0.4 on 2024-05-20 11:39

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('main', '0019_remove_purchase_status_delete_debt_delete_purchase'),
    ]

    operations = [
        migrations.CreateModel(
            name='Debt',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('amount', models.DecimalField(decimal_places=2, max_digits=40)),
                ('note', models.TextField()),
            ],
        ),
        migrations.CreateModel(
            name='ExpenseCategory',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100)),
            ],
        ),
        migrations.CreateModel(
            name='Expenses',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('date', models.DateField(auto_now_add=True)),
                ('name', models.TextField()),
                ('amount', models.DecimalField(decimal_places=2, max_digits=40)),
                ('branch', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='main.branch')),
                ('category', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='accounting.expensecategory')),
            ],
            options={
                'ordering': ['-date'],
            },
        ),
    ]
