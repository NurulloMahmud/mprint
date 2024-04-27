from rest_framework import serializers
from .models import (
    Status, Branch,
    Product, Inventory,
    InventoryOrder, Customer,
    CustomerDebt, Order,
    OrderPayment, ServiceOrder,
    Service, Purchase,
    Debt, Size,
)


class StatusSerializer(serializers.ModelSerializer):
    class Meta:
        model = Status
        fields = "__all__"


class BranchSerializer(serializers.ModelSerializer):
    class Meta:
        model = Branch
        fields = "__all__"


class ProductSerializer(serializers.ModelSerializer):
    branch = StatusSerializer()

    class Meta:
        model = Product
        fields = "__all__"

