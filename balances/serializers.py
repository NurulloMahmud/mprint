from rest_framework import serializers
from django.db.models import Sum

from .models import BalanceSheet, Stakeholder, Expenses

from decimal import Decimal


class StakeHolderViewSerializer(serializers.ModelSerializer):
    total = serializers.SerializerMethodField()
    class Meta:
        model = Stakeholder
        fields = ['id', 'name', 'percent']

    def get_total(self, obj):
        total_income = BalanceSheet.objects.filter(stakeholder=obj).aggregate(Sum('balance'))['balance__sum'] or 0
        total_expenses = Expenses.objects.filter(stakeholder=obj).aggregate(Sum('amount'))['amount__sum'] or 0
        return Decimal(total_income) - Decimal(total_expenses)
    

class StakeHolderWriteSerializer(serializers.ModelSerializer):
    class Meta:
        model = Stakeholder
        fields = ['id', 'name', 'percent']


class ExpensesViewSerializer(serializers.ModelSerializer):
    stakeholder = StakeHolderWriteSerializer()
    class Meta:
        model = Expenses
        fields = '__all__'


class ExpensesWriteSerializer(serializers.ModelSerializer):
    class Meta:
        model = Expenses
        fields = '__all__'

