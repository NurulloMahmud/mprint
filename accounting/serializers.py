from django.db.models import Sum
from rest_framework import serializers
from .models import ExpenseCategory, Expenses, InventoryExpense, Debt
from main.serializers import BranchSerializer, OrderReadSerializer, CustomerSerializer, PaperReadSerializer, \
    ServiceOrderSerializer, OrderPicsSerializer
from main.models import Branch, PaymentMethod, OrderPayment, CustomerDebt, Customer, Order, Inventory, Paper
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
    orders = serializers.SerializerMethodField()

    class Meta:
        model = Customer
        fields = '__all__'

    def get_debt(self, obj):
        if CustomerDebt.objects.filter(customer=obj).exists():
            debt_amount = CustomerDebt.objects.filter(customer=obj).aggregate(Sum('amount'))['amount__sum']
            return Decimal(debt_amount) if debt_amount is not None else Decimal(0)
        return Decimal(0)
    def get_orders(self, obj):
        return Order.objects.filter(customer=obj).count()
    
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

class InventorySerializer(serializers.ModelSerializer):
    branch_name = serializers.SerializerMethodField()

    class Meta:
        model = Inventory
        fields = '__all__'
    def get_branch_name(self, obj):
        return Branch.objects.get(id=obj.branch.id).name

class InventoryExpenseSerializer(serializers.ModelSerializer):
    item = serializers.PrimaryKeyRelatedField(queryset=Inventory.objects.all())
    order = serializers.PrimaryKeyRelatedField(queryset=Order.objects.all().values('id', 'name', 'final_price', 'date'))

    class Meta:
        model = InventoryExpense
        fields = '__all__'

class PaperUsageSummarySerializer(serializers.ModelSerializer):
    paper_type = serializers.SerializerMethodField()
    branch = serializers.SerializerMethodField()
    quantity = serializers.IntegerField()
    total_cost = serializers.DecimalField(max_digits=40, decimal_places=2)
    total_price = serializers.DecimalField(max_digits=40, decimal_places=2)
    
    class Meta:
        model = Paper
        fields = ['id', 'paper_type', 'grammaj', 'branch', 'quantity', 'total_cost', 'total_price']

    def get_paper_type(self, obj):
        return obj.paper_type.name

    def get_branch(self, obj):
        return obj.branch.name

class InventoryExpenseSummarySerializer(serializers.Serializer):
    item_name = serializers.CharField(source='item__name')
    total_quantity = serializers.FloatField()
    total_amount = serializers.DecimalField(max_digits=40, decimal_places=2)

class InventoryExpenseCreateSerializer(serializers.ModelSerializer):
    item = serializers.PrimaryKeyRelatedField(queryset=Inventory.objects.all())
    order = serializers.PrimaryKeyRelatedField(queryset=Order.objects.all())

    class Meta:
        model = InventoryExpense
        fields = ['item', 'order', 'quantity']

class CustomerDebtListSerializer(serializers.ModelSerializer):
    customer = CustomerSerializer()
    order = serializers.SerializerMethodField()
    class Meta:
        model = CustomerDebt
        fields = '__all__'

    def get_order(self, obj):
        order = Order.objects.filter(customer=obj.customer).values('id', 'name', 'final_price', 'date')
        return order

class OrderDetailSerializer(serializers.ModelSerializer):
    customer = CustomerSerializer()
    paper = PaperReadSerializer()
    services = ServiceOrderSerializer(many=True, read_only=True)
    pics = OrderPicsSerializer(many=True, read_only=True)
    class Meta:
        model = Order
        fields = '__all__'

class DebtSerializer(serializers.ModelSerializer):
    class Meta:
        model = Debt
        fields = '__all__'
