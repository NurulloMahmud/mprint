from django.db.models import Sum
from rest_framework import serializers
from .models import ExpenseCategory, Expenses
from main.serializers import BranchSerializer, OrderReadSerializer, CustomerSerializer
from main.models import Branch, PaymentMethod, OrderPayment, CustomerDebt, Customer, Order
from decimal import Decimal


class ExpenseCategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = ExpenseCategory
        fields = '__all__'
    

class ExpensesReadSerializer(serializers.ModelSerializer):
    category = ExpenseCategory()
    branch = BranchSerializer()

    class Meta:
        model = Expenses
        fields = '__all__'
    
    def create(self, validated_data):
        branch = validated_data.pop('branch')
        branch_obj = Branch.objects.get(id=branch['id'])
        category = validated_data.pop('category')
        category_obj = ExpenseCategory.objects.get(id=category['id'])
        expense = Expenses.objects.create(category=category_obj, branch=branch_obj, **validated_data)
        return expense
    
    def update(self, instance, validated_data):
        branch = validated_data.pop('branch')
        branch_obj = Branch.objects.get(id=branch['id'])
        category = validated_data.pop('category')
        category_obj = ExpenseCategory.objects.get(id=category['id'])
        instance.category = category_obj
        instance.branch = branch_obj
        return super().update(instance, validated_data)
    

class PaymentMethodSerializer(serializers.ModelSerializer):
    class Meta:
        model = PaymentMethod
        fields = '__all__'


class OrderPaymentReadSerializer(serializers.ModelSerializer):
    method = PaymentMethodSerializer()
    order = OrderReadSerializer()

    class Meta:
        model = OrderPayment
        fields = '__all__'


class OrderPaymentWriteSerializer(serializers.ModelSerializer):
    method = serializers.PrimaryKeyRelatedField(queryset=PaymentMethod.objects.all())
    
    class Meta:
        model = OrderPayment
        fields = '__all__'


class CustomerDebtReadSerializer(serializers.ModelSerializer):
    debt = serializers.SerializerMethodField()

    class Meta:
        model = Customer
        fields = '__all__'

    def get_debt(self, obj):
        if CustomerDebt.objects.filter(customer=obj).exists():
            debt_amount = CustomerDebt.objects.filter(customer=obj).aggregate(Sum('amount'))['amount__sum']
            return Decimal(debt_amount) if debt_amount is not None else Decimal(0)
        return Decimal(0)

    
class OrdersDebtListSerializer(serializers.ModelSerializer):
    customer = serializers.SerializerMethodField()
    debt = serializers.SerializerMethodField()

    class Meta:
        model = Order
        fields = ['id', 'name', 'customer', 'final_price', 'debt', 'total_price']
    def get_customer(self, obj):
        return obj.customer.name
    def get_debt(self, obj):
        debt = CustomerDebt.objects.get(order=obj)
        return Decimal(debt.amount)


class ExpensesWriteSerializer(serializers.ModelSerializer):
    category = serializers.PrimaryKeyRelatedField(queryset=ExpenseCategory.objects.all())
    branch = serializers.PrimaryKeyRelatedField(queryset=Branch.objects.all())

    class Meta:
        model = Expenses
        fields = '__all__'

class ExpensesReadSerializer(serializers.ModelSerializer):
    category = ExpenseCategorySerializer()
    branch = BranchSerializer()

    class Meta:
        model = Expenses
        fields = '__all__'

