from rest_framework import serializers
from .models import (
    Status, Branch,
    Paper, Customer,
    CustomerDebt, Order,
    OrderPayment, ServiceOrder,
    Service, Purchase,
    Debt, PaperType,
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
        fields = ['id', 'name', 'cost', 'price', 'branch', 'available']

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


class OrderReadSerializer(serializers.ModelSerializer):
    customer = CustomerSerializer()
    paper = PaperReadSerializer()
    status = StatusSerializer()
    branch = BranchSerializer()
    class Meta:
        model = Order
        fields = "__all__"

