from django.db.models import Sum
from rest_framework import serializers

from main.models import Order, Customer, Status, Branch, Paper, OrderPics, OrderPayment, ServiceOrder, Service, CustomerDebt


class OrderCreateCustomSerializer(serializers.Serializer):
    name = serializers.CharField(max_length=500)
    customer_id = serializers.IntegerField()
    products_qty = serializers.IntegerField()
    paper_id = serializers.IntegerField()
    num_of_lists = serializers.IntegerField()
    num_possible_defect_list = serializers.IntegerField(required=False)
    price_per_list = serializers.DecimalField(decimal_places=2, max_digits=10, required=False)
    total_price = serializers.DecimalField(decimal_places=2, max_digits=10, required=False)
    final_price = serializers.DecimalField(decimal_places=2, max_digits=10, required=False)
    price_per_product = serializers.DecimalField(decimal_places=2, max_digits=10, required=False)
    status = serializers.IntegerField()
    branch = serializers.IntegerField()
    
    pics = serializers.ListField(
        child=serializers.ImageField(),
        required=False,
        allow_empty=True,
    )

    services = serializers.ListField(
        child=serializers.IntegerField(),
        required=False,
        allow_empty=True,
    )

    total_sqr_meter = serializers.FloatField()
    num_of_lists_per_paper = serializers.IntegerField()
    initial_payment_amount = serializers.DecimalField(decimal_places=2, max_digits=10, required=False)

    def create(self, validated_data):
        sqr_meter = validated_data.get('total_sqr_meter')
        total_num_lists = validated_data.get('num_of_lists', 0) + validated_data.get('num_possible_defect_list', 0)
        initial_payment_amount = validated_data.get('initial_payment_amount', 0)

        # objects
        customer_obj = Customer.objects.get(id=validated_data.get('customer_id'))
        paper_obj = Paper.objects.get(id=validated_data.get('paper_id'))
        status_obj = Status.objects.get(id=validated_data.get('status'))
        branch_obj = Branch.objects.get(id=validated_data.get('branch'))

        # initial order
        order = Order.objects.create(
            name = validated_data.get('name'),
            customer = customer_obj,
            products_qty = validated_data.get('products_qty'),
            paper = paper_obj,
            num_of_lists = total_num_lists,
            sqr_meter = sqr_meter,
            total_price = 0,    # calculated later
            final_price = validated_data.get('final_price'),
            price_per_product = 0,   # calculated later
            status = status_obj,
            branch = branch_obj
        )

        # calculate service prices
        for service in validated_data.get('services', []):
            service_obj = Service.objects.get(id=service)
            new_service_order = ServiceOrder.objects.create(order=order, service=service_obj)
            if service_obj.price_per_sqr:
                new_service_order.total_price = service_obj.price_per_sqr * sqr_meter
                new_service_order.save()
            elif service_obj.price_per_list:
                new_service_order.total_price = service_obj.price_per_list * total_num_lists
                new_service_order.save()
            if new_service_order.total_price < service_obj.min_price:
                new_service_order.total_price = service_obj.min_price
                new_service_order.save()
            order.total_price += new_service_order.total_price
            order.save()
        
        # calculate paper prices
        num_of_papers = (validated_data.get('num_of_lists', 0) + validated_data.get('num_possible_defect_list', 0)) // validated_data.get('num_of_lists_per_paper')
        paper_cost = paper_obj.price * num_of_papers
        order.total_price += paper_cost
        order.save()

        # calculate final
        if not validated_data.get('final_price'):
            order.final_price = order.total_price
        else:
            order.final_price = validated_data.get('final_price')
        order.save()

        # calculate price per product
        order.price_per_product = order.final_price / order.products_qty
        order.save()

        # calculate price per list
        order.price_per_list = order.price_per_product / (order.num_of_lists + order.possible_defect_list)
        order.save()

        # calculate payment and debts
        if initial_payment_amount < order.final_price:
            CustomerDebt.objects.create(order=order, customer=customer_obj, amount=order.final_price - initial_payment_amount)
        if initial_payment_amount:
            OrderPayment.objects.create(order=order, amount=initial_payment_amount)

        # store order images
        for image in validated_data.get('pics', []):
            OrderPics.objects.create(order=order, image=image)
        
        # subtract used paper from inventory
        paper_obj.available_qty -= num_of_papers
        paper_obj.save()

        return order

