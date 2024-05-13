from rest_framework import serializers

from main.models import Order, Customer, Status, Branch


class OrderCreateCustomSerializer(serializers.Serializer):
    customer_id = serializers.IntegerField()
    name = serializers.CharField(max_length=100)
    products_qty = serializers.IntegerField()
    total_price = serializers.DecimalField(decimal_places=2, max_digits=10)
    final_price = serializers.DecimalField(decimal_places=2, max_digits=10, required=False)
    price_per_product = serializers.DecimalField(decimal_places=2, max_digits=10, required=False)
    status_id = serializers.IntegerField()
    branch_id = serializers.IntegerField()
    
    pics = serializers.ListField(
        child=serializers.ImageField(),
        required=False,
        allow_empty=True
    )

    service_ids = serializers.ListField(
        child=serializers.IntegerField(),
        required=False,
        allow_empty=True
    )

    paper_id = serializers.IntegerField()
    num_of_lists = serializers.IntegerField()
    possible_defect = serializers.IntegerField()
    initial_payment_amount = serializers.DecimalField(decimal_places=2, max_digits=10)
    lists_per_paper = serializers.IntegerField()

    def create(self, validated_data):
        customer = Customer.objects.get(id=validated_data.pop('customer_id'))
        status = Status.objects.get(id=validated_data.pop('status_id'))
        branch = Branch.objects.get(id=validated_data.pop('branch_id'))
        total = validated_data.get('total_price')
        order = Order.objects.create(
            customer=customer,
            status=status,
            branch=branch,
            name=validated_data.get('name'),
            products_qty=validated_data.get('products_qty'),
            total_price=total,
            final_price=validated_data.get('final_price', total),
        )
        order.price_per_product = order.final_price / order.products_qty
        order.save()
        