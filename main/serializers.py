from rest_framework import serializers
from .models import (
    Status, Branch,
    Paper, Customer,
    CustomerDebt, Order,
    OrderPayment, ServiceOrder,
    Service, PaperType,
    OrderPics, Inventory,
)

class PaperTypeSerializer(serializers.ModelSerializer):
    class Meta:
        model = PaperType
        fields = "__all__"

class StatusSerializer(serializers.ModelSerializer):
    class Meta:
        model = Status
        fields = "__all__"

class StatusReadSerializer(serializers.ModelSerializer):
    count = serializers.SerializerMethodField()
    class Meta:
        model = Status
        fields = ['id', 'name', 'count']

    def get_count(self, obj):
        return obj.orders.count()

class BranchSerializer(serializers.ModelSerializer):
    class Meta:
        model = Branch
        fields = "__all__"

class PaperReadSerializer(serializers.ModelSerializer):
    paper_type = PaperTypeSerializer()
    branch = BranchSerializer()
    
    class Meta:
        model = Paper
        fields = "__all__"

class PaperWriteSerializer(serializers.ModelSerializer):
    class Meta:
        model = Paper
        fields = "__all__"

class CustomerSerializer(serializers.ModelSerializer):
    class Meta:
        model = Customer
        fields = "__all__"
   
class ServiceSerializer(serializers.ModelSerializer):
    class Meta:
        model = Service
        fields = "__all__"

class InventoryReadSerializer(serializers.ModelSerializer):
    branch = BranchSerializer(read_only=True)

    class Meta:
        model = Inventory
        fields = ['id', 'name', 'cost', 'branch', 'available']

    def to_representation(self, instance):
        """
        Modify the serialized data based on the user's role.
        """
        data = super().to_representation(instance)
        request = self.context.get('request')

        if request and request.user.role.lower() != 'admin':
            data.pop('cost', None)  # Remove 'cost' field if user is not admin

        return data

class InventoryWriteSerializer(serializers.ModelSerializer):
    class Meta:
        model = Inventory
        fields = "__all__"

class OrderPicsSerializer(serializers.ModelSerializer):
    class Meta:
        model = OrderPics
        fields = ['pic']

class CustomerDebtSerializer(serializers.ModelSerializer):
    class Meta:
        model = CustomerDebt
        fields = "__all__"

class OrderPaymentSerializer(serializers.ModelSerializer):
    class Meta:
        model = OrderPayment
        fields = "__all__"

class ServiceOrderSerializer(serializers.ModelSerializer):
    service = ServiceSerializer()
    class Meta:
        model = ServiceOrder
        fields = ['service', 'total_price']

class OrderReadSerializer(serializers.ModelSerializer):
    customer = CustomerSerializer()
    paper = PaperReadSerializer()
    status = StatusSerializer()
    branch = BranchSerializer()
    pics = OrderPicsSerializer(many=True, read_only=True)
    debt = CustomerDebtSerializer(many=True, read_only=True)
    payments = OrderPaymentSerializer(many=True, read_only=True)
    services = ServiceOrderSerializer(many=True, read_only=True)

    class Meta:
        model = Order
        fields = "__all__"

class OrderDeleteSerializer(serializers.ModelSerializer):
    class Meta:
        model = Order
        fields = ['id']
    
    def delete(self, instance):
        if instance.status.name != 'Kutishda':
            raise serializers.ValidationError('Order cannot be deleted')
        else:
            instance.delete()
            return instance

class InventorySerializer(serializers.ModelSerializer):
    branch = BranchSerializer()
    
    class Meta:
        model = Inventory
        fields = "__all__"
    
    def create(self, validated_data):
        branch_data = validated_data.pop('branch')
        branch_obj = Branch.objects.get(id=branch_data['id'])
        inventory = Inventory.objects.create(branch=branch_obj, **validated_data)
        return inventory

    def update(self, instance, validated_data):
        branch_data = validated_data.pop('branch')
        branch_obj = Branch.objects.get(id=branch_data['id'])
        instance.branch = branch_obj
        return super().update(instance, validated_data)
