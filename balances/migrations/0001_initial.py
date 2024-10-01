# Generated by Django 4.2.13 on 2024-09-30 01:32

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Stakeholder',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100)),
                ('percent', models.IntegerField()),
            ],
        ),
        migrations.CreateModel(
            name='Expenses',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('date', models.DateField()),
                ('amount', models.DecimalField(decimal_places=2, max_digits=40)),
                ('stakeholder', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='balances.stakeholder')),
            ],
        ),
        migrations.CreateModel(
            name='BalanceSheet',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('date', models.DateField()),
                ('balance', models.DecimalField(decimal_places=2, max_digits=40)),
                ('stakeholder', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='balances.stakeholder')),
            ],
        ),
    ]
