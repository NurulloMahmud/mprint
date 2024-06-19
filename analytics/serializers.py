from rest_framework import serializers
from main.models import (
    OrderManager, Order,
    OrderPayment,
)
from accounting.models import (
    PaperExpenses, InventoryExpense,
    ExpenseCategory, Expenses
)

class CategoryTotalSerializer(serializers.ModelSerializer):
    total_amount = serializers.DecimalField(max_digits=40, decimal_places=2)

    class Meta:
        model = ExpenseCategory
        fields = ['name', 'total_amount']
