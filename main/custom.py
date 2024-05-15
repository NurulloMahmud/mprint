from rest_framework import serializers
from .models import Order, OrderPics, ServiceOrder, CustomerDebt, OrderPayment, Customer, Paper, Branch, Service

class OrderCreateCustomSerializer(serializers.Serializer):
    name = serializers.CharField(max_length=500)
    customer_id = serializers.IntegerField()
    products_qty = serializers.IntegerField()
    paper_id = serializers.IntegerField()
    num_of_lists = serializers.IntegerField()
    num_possible_defect_list = serializers.IntegerField(required=False, default=0)
    price_per_list = serializers.DecimalField(decimal_places=2, max_digits=10, required=False)
    total_price = serializers.DecimalField(decimal_places=2, max_digits=10, required=False)
    final_price = serializers.DecimalField(decimal_places=2, max_digits=10, required=False)
    price_per_product = serializers.DecimalField(decimal_places=2, max_digits=10, required=False)
    branch = serializers.IntegerField()
    pics = serializers.ListField(child=serializers.ImageField(), required=False, allow_empty=True)
    services = serializers.ListField(child=serializers.IntegerField(), required=False, allow_empty=True)
    total_sqr_meter = serializers.FloatField()
    num_of_lists_per_paper = serializers.IntegerField()
    initial_payment_amount = serializers.DecimalField(decimal_places=2, max_digits=10, required=False, default=0)

    def create(self, validated_data):
        try:
            customer_obj = Customer.objects.get(id=validated_data['customer_id'])
            paper_obj = Paper.objects.get(id=validated_data['paper_id'])
            branch_obj = Branch.objects.get(id=validated_data['branch'])
        except (Customer.DoesNotExist, Paper.DoesNotExist, Branch.DoesNotExist) as e:
            raise serializers.ValidationError(f"Related object not found: {str(e)}")

        total_num_lists = validated_data['num_of_lists'] + validated_data.get('num_possible_defect_list', 0)
        initial_payment_amount = validated_data.get('initial_payment_amount', 0)
        sqr_meter = validated_data['total_sqr_meter']

        order = Order.objects.create(
            name=validated_data['name'],
            customer=customer_obj,
            products_qty=validated_data['products_qty'],
            paper=paper_obj,
            num_of_lists=total_num_lists,
            sqr_meter=sqr_meter,
            total_price=0,    # calculated later
            final_price=validated_data.get('final_price'),
            price_per_product=0,   # calculated later
            branch=branch_obj
        )

        # Calculate service prices
        for service_id in validated_data.get('services', []):
            service_obj = Service.objects.get(id=service_id)
            new_service_order = ServiceOrder.objects.create(order=order, service=service_obj)

            if service_obj.price_per_sqr:
                new_service_order.total_price = max(service_obj.price_per_sqr * sqr_meter, service_obj.minimum_price)
            elif service_obj.price_per_qty:
                new_service_order.total_price = max(service_obj.price_per_qty * total_num_lists, service_obj.minimum_price)
            else:
                new_service_order.total_price = service_obj.minimum_price

            new_service_order.save()
            order.total_price += new_service_order.total_price

        # Calculate paper prices
        num_of_papers = total_num_lists // validated_data['num_of_lists_per_paper']
        paper_cost = paper_obj.price * num_of_papers
        order.total_price += paper_cost

        # Calculate final price
        order.final_price = validated_data.get('final_price', order.total_price)

        # Calculate price per product
        order.price_per_product = order.final_price / order.products_qty

        # Calculate price per list
        order.price_per_list = order.price_per_product / total_num_lists

        order.save()

        # Calculate payment and debts
        if initial_payment_amount < order.final_price:
            CustomerDebt.objects.create(order=order, customer=customer_obj, amount=order.final_price - initial_payment_amount)
        if initial_payment_amount > 0:
            OrderPayment.objects.create(order=order, amount=initial_payment_amount)

        # Store order images
        for image in validated_data.get('pics', []):
            OrderPics.objects.create(order=order, pic=image)

        # Subtract used paper from inventory
        paper_obj.available_qty -= num_of_papers
        paper_obj.save()

        return order

    def to_representation(self, instance):
        representation = super().to_representation(instance)
        representation['status'] = instance.status.id  # Ensure the status is represented by its ID
        return representation
