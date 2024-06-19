from rest_framework import serializers
from main.models import (
    OrderManager, Order,
    OrderPayment, Customer
)
from accounting.models import (
    PaperExpenses, InventoryExpense,
    ExpenseCategory, Expenses
)
from django.db.models import Sum


class CategoryTotalSerializer(serializers.ModelSerializer):
    total_amount = serializers.DecimalField(max_digits=40, decimal_places=2)

    class Meta:
        model = ExpenseCategory
        fields = ['name', 'total_amount']

class CustomerSummarySerializer(serializers.ModelSerializer):
    total_amount = serializers.DecimalField(max_digits=40, decimal_places=2)
    orders_count = serializers.IntegerField()

    class Meta:
        model = Customer
        fields = ['name', 'total_amount']
    
    def get_total_amount(self, obj):
        return Order.objects.filter(customer=obj).aggregate(Sum('final_price'))['final_price__sum']

    def get_orders_count(self, obj):
        return Order.objects.filter(customer=obj).count()
