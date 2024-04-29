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


class ProductReadSerializer(serializers.ModelSerializer):
    branch = BranchSerializer()

    class Meta:
        model = Product
        fields = "__all__"


class ProductWriteSerializer(serializers.ModelSerializer):
    class Meta:
        model = Product
        fields = "__all__"


class SizeReadSerializer(serializers.ModelSerializer):
    paper = ProductReadSerializer()

    class Meta:
        model = Size
        fields = "__all__"

