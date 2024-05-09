from rest_framework import serializers
from .models import (
    Status, Branch,
    Paper, Customer,
    CustomerDebt, Order,
    OrderPayment, ServiceOrder,
    Service, Purchase,
    Debt, PaperType,
    OrderPaper, OrderPics, 
    Inventory,
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


class OrderWriteSerializer(serializers.ModelSerializer):
    class Meta:
        model = Order
        fields = "__all__"


class OrderReadSerializer(serializers.ModelSerializer):
    customer = CustomerSerializer()
    status = StatusSerializer()
    branch = BranchSerializer()

    class Meta:
        model = Order
        fields = "__all__"
        

"""
SERIALIZERS FOR ORDER CREATION
"""

class OrderPicsSerializer(serializers.ModelSerializer):
    class Meta:
        model = OrderPics
        fields = ['pic']

class OrderPaymentSerializer(serializers.ModelSerializer):
    class Meta:
        model = OrderPayment
        fields = ['amount', 'date']

class CustomerDebtSerializer(serializers.ModelSerializer):
    class Meta:
        model = CustomerDebt
        fields = ['amount', 'last_update']

class OrderPaperSerializer(serializers.ModelSerializer):
    class Meta:
        model = OrderPaper
        fields = ['paper', 'num_of_lists', 'possible_defect', 'price_per_list', 'price_per_product']

class ServiceOrderSerializer(serializers.ModelSerializer):
    class Meta:
        model = ServiceOrder
        fields = ['service', 'quantity', 'total_price']

class OrderCreateSerializer(serializers.ModelSerializer):
    # Nested serializers to handle related models
    images = OrderPicsSerializer(many=True)
    payments = OrderPaymentSerializer(many=True)
    debt = CustomerDebtSerializer()
    papers = OrderPaperSerializer(many=True)
    services = ServiceOrderSerializer(many=True)

    class Meta:
        model = Order
        fields = ['date', 'name', 'customer', 'products_qty', 'total_price', 'final_price',
                  'price_per_product', 'status', 'branch', 'images', 'payments', 'debt', 'papers', 'services']

    def create(self, validated_data):
        # Extract related data
        images_data = validated_data.pop('images')
        payments_data = validated_data.pop('payments')
        debt_data = validated_data.pop('debt')
        papers_data = validated_data.pop('papers')
        services_data = validated_data.pop('services')

        # Create the main Order object
        order = Order.objects.create(**validated_data)

        # Create related objects
        for image in images_data:
            OrderPics.objects.create(order=order, **image)

        for payment in payments_data:
            OrderPayment.objects.create(order=order, **payment)

        CustomerDebt.objects.create(order=order, **debt_data)

        for paper in papers_data:
            OrderPaper.objects.create(order=order, **paper)

        for service in services_data:
            ServiceOrder.objects.create(order=order, **service)

        return order

"""
END OF ORDER CREATION SERIALIZERS
"""

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

