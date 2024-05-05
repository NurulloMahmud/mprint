from rest_framework import serializers
from .models import (
    Status, Branch,
    Paper, Customer,
    CustomerDebt, Order,
    OrderPayment, ServiceOrder,
    Service, Purchase,
    Debt, PaperType
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
    branch = BranchSerializer()
    paper_type = PaperTypeSerializer()

    class Meta:
        model = Paper
        fields = "__all__"


class PaperWriteSerializer(serializers.ModelSerializer):
    class Meta:
        model = Paper
        fields = "__all__"

