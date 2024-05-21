from rest_framework.response import Response
from rest_framework.viewsets import ModelViewSet
from rest_framework import generics
from rest_framework.views import APIView
from rest_framework import status

from decimal import Decimal

from django.shortcuts import get_object_or_404
from django.db import transaction

from drf_yasg.utils import swagger_auto_schema
from drf_yasg import openapi

from .models import (
    Branch, Status,
    Customer, Order,
    PaperType, Inventory,
    Paper, Service, CustomerDebt,
    OrderPayment, ServiceOrder,
    OrderPics, PaymentMethod
)

from .serializers import (
    BranchSerializer, StatusSerializer, 
    PaperReadSerializer, PaperWriteSerializer,
    CustomerSerializer, OrderReadSerializer,
    PaperTypeSerializer, InventoryReadSerializer,
    InventoryWriteSerializer, ServiceSerializer,
    OrderDeleteSerializer, InventorySerializer,
    StatusReadSerializer
)

from .custom import OrderCreateCustomSerializer


from users.permissions import IsAdminRole, IsManagerRole
from main.pagination import CustomPagination



class StatusViewSet(ModelViewSet):
    queryset = Status.objects.all()
    permission_classes = (IsManagerRole,)

    def get_serializer_class(self):
        if self.action in ['list', 'retrieve']:
            return StatusReadSerializer
        return StatusSerializer


class BranchViewset(ModelViewSet):
    queryset = Branch.objects.all()
    serializer_class = BranchSerializer
    permission_classes = (IsAdminRole,)


class PaperListView(generics.ListAPIView):
    queryset = Paper.objects.all()
    serializer_class = PaperReadSerializer
    permission_classes = [IsManagerRole]


class PaperRetrieveUpdateDestroyView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Paper.objects.all()
    serializer_class = PaperWriteSerializer
    permission_classes = [IsManagerRole]


class PaperCreateView(APIView):
    permission_classes = [IsAdminRole]

    @swagger_auto_schema(
        operation_description="Create a new paper entry.",
        request_body=openapi.Schema(
            type=openapi.TYPE_OBJECT,
            required=['name', 'cost', 'price', 'branch_id', 'quantity'],  # Specify the required fields here
            properties={
                'name': openapi.Schema(type=openapi.TYPE_STRING, description='Name of the paper'),
                'paper_type': openapi.Schema(type=openapi.TYPE_INTEGER, description='Foreign key ID of the paper type', format='int32'),
                'grammaj': openapi.Schema(type=openapi.TYPE_STRING, description='Weight/grammaj of the paper'),
                'cost': openapi.Schema(type=openapi.TYPE_NUMBER, format='decimal', description='Cost of the paper'),
                'price': openapi.Schema(type=openapi.TYPE_NUMBER, format='decimal', description='Price of the paper'),
                'branch_id': openapi.Schema(type=openapi.TYPE_INTEGER, description='Foreign key ID of the branch', format='int32'),
                'quantity': openapi.Schema(type=openapi.TYPE_INTEGER, description='Quantity of the paper'),
            }
        ),
        responses={
            status.HTTP_201_CREATED: "Successfully created",
            status.HTTP_400_BAD_REQUEST: "Invalid data input or missing field",
            status.HTTP_401_UNAUTHORIZED: "User is not authorized",
        },
    )
    def post(self, request):
        if not request.user or not request.user.role.lower() == "admin":
            context = {
                "success": False,
                "message": "User is not authorized"
            }
            return Response(context, status=status.HTTP_401_UNAUTHORIZED)

        data = request.data
        serializer = PaperWriteSerializer(data=data)

        if serializer.is_valid():
            serializer.save()
            context = {
                "success": True,
                "message": "Created successfully",
                "data": serializer.data,
            }
            return Response(context, status=status.HTTP_201_CREATED)

        context = {
            "success": False,
            "message": "Invalid data input or missing field",
        }
        return Response(context, status=status.HTTP_400_BAD_REQUEST)


class CustomerViewset(ModelViewSet):
    queryset = Customer.objects.all()
    serializer_class = CustomerSerializer


class OrderListView(generics.ListAPIView):
    queryset = Order.objects.all()
    pagination_class = CustomPagination
    serializer_class = OrderReadSerializer


class OrderCreateView(APIView):
    @swagger_auto_schema(
        operation_summary="Create a new Order",
        operation_description="Creates a new order with all related details including services and images.",
        request_body=openapi.Schema(
            type=openapi.TYPE_OBJECT,
            required=['name', 'customer_id', 'branch', 'paper_id', 
                      'num_of_lists', 'total_sqr_meter', 'final_price', 
                      'num_of_lists_per_paper', 'initial_payment_amount', 
                      'num_of_product_per_list', 'lists_per_paper'],
            properties={
                'num_of_lists_per_paper': openapi.Schema(type=openapi.TYPE_INTEGER, description='Number of lists per paper'),
                'lists_per_paper': openapi.Schema(type=openapi.TYPE_INTEGER, description='How many lists per paper'),
                'num_of_product_per_list': openapi.Schema(type=openapi.TYPE_INTEGER, description='Number of products per list'),
                'customer_id': openapi.Schema(type=openapi.TYPE_INTEGER, description='ID of the customer'),
                'final_price': openapi.Schema(type=openapi.FORMAT_DECIMAL, description='Final price of the order'),
                'branch': openapi.Schema(type=openapi.TYPE_INTEGER, description='ID of the branch'),
                'paper_id': openapi.Schema(type=openapi.TYPE_INTEGER, description='ID of the paper used'),
                'name': openapi.Schema(type=openapi.TYPE_STRING, description='Name of the order'),
                'products_qty': openapi.Schema(type=openapi.TYPE_INTEGER, description='Quantity of products', default=0),
                'num_of_lists': openapi.Schema(type=openapi.TYPE_INTEGER, description='Number of lists'),
                'num_possible_defect_list': openapi.Schema(type=openapi.TYPE_INTEGER, description='Number of possible defective lists', default=0),
                'total_sqr_meter': openapi.Schema(type=openapi.TYPE_NUMBER, format=openapi.FORMAT_FLOAT, description='Total square meters'),
                'services': openapi.Schema(
                    type=openapi.TYPE_ARRAY,
                    items=openapi.Items(type=openapi.TYPE_INTEGER),
                    description='List of service IDs involved'
                ),
                'initial_payment_amount': openapi.Schema(type=openapi.TYPE_NUMBER, format=openapi.FORMAT_FLOAT, description='Initial payment amount', default=0),
                'initial_payment_method': openapi.Schema(type=openapi.TYPE_INTEGER, description='ID of the payment method'),
                'pics': openapi.Schema(
                    type=openapi.TYPE_ARRAY,
                    description='List of images for the order',
                    items=openapi.Items(type=openapi.TYPE_FILE),
                )
            },
        ),
        responses={201: openapi.Response('Order successfully created')}
    )
    def post(self, request):
        data = request.data

        # Validate and fetch related objects
        try:
            customer_obj = get_object_or_404(Customer, id=data['customer_id'])
            if request.user.role.lower() == "admin":
                branch_obj = get_object_or_404(Branch, id=data['branch'])
            else:
                branch_obj = request.user.branch
            paper_obj = get_object_or_404(Paper, id=data['paper_id'])
            # Ensure the default status is set if the order is new
            status_obj = Status.objects.get(name="Pending")
        except Exception as e:
            return Response({"success": False, "message": str(e)}, status=status.HTTP_400_BAD_REQUEST)

        try:
            with transaction.atomic():
                # Assuming all the numerical data is valid and conversions are not needed (handled in frontend or here with try-except)
                order = Order.objects.create(
                    name=data['name'],
                    customer=customer_obj,
                    products_qty=data['products_qty'],
                    paper=paper_obj,
                    num_of_lists=data['num_of_lists'],
                    total_sqr_meter=data['total_sqr_meter'],
                    possible_defect_list=data.get('num_possible_defect_list', 0),
                    price_per_list=None,  # to be calculated
                    total_price=0,  # to be calculated
                    final_price=Decimal(data['final_price']),
                    price_per_product=None,  # to be calculated
                    status=status_obj,
                    branch=branch_obj,
                    num_of_product_per_list=data['num_of_product_per_list'],
                    lists_per_paper=data['num_of_lists_per_paper']
                )

                order.num_of_lists = (int(order.products_qty) // int(order.num_of_product_per_list)) + int(order.possible_defect_list)

                # Calculate total price of order
                service_ids = request.data.get('services', [])
                order.calculate(service_ids)

                # Handle Payments and Debts
                initial_payment_amount = Decimal(data.get('initial_payment_amount', 0))
                final_price = Decimal(order.final_price)
                if initial_payment_amount < final_price:
                    CustomerDebt.objects.create(customer=customer_obj, order=order, amount=final_price - initial_payment_amount)
                if initial_payment_amount > 0:
                    initial_payment_method = data.get('initial_payment_method', None)
                    method_obj = get_object_or_404(PaymentMethod, id=initial_payment_method)
                    OrderPayment.objects.create(order=order, amount=initial_payment_amount, method=method_obj)

                # Handle image uploads
                for image_file in request.FILES.getlist('pics'):
                    OrderPics.objects.create(order=order, pic=image_file)

            return Response({"success": True, "message": "Order created successfully", "order_id": order.id}, status=status.HTTP_201_CREATED)
        
        except Exception as e:
            return Response({"success": False, "message": str(e)}, status=status.HTTP_400_BAD_REQUEST)


class PaperTypeViewset(ModelViewSet):
    queryset = PaperType.objects.all()
    serializer_class = PaperTypeSerializer
    permission_classes = [IsAdminRole]


class InventoryListAPIView(generics.ListAPIView):
    queryset = Inventory.objects.all()
    serializer_class = InventoryReadSerializer
    permission_classes = [IsManagerRole]

    def get_serializer_context(self):
        # Add the request context to the serializer
        context = super().get_serializer_context()
        context.update({'request': self.request})
        return context


class InventoryCreateAPIView(generics.CreateAPIView):
    queryset = Inventory.objects.all()
    serializer_class = InventoryWriteSerializer
    permission_classes = [IsAdminRole]


class InventoryUpdateDestroyAPIView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Inventory.objects.all()
    serializer_class = InventoryWriteSerializer
    permission_classes = [IsAdminRole]

    def get_serializer(self, *args, **kwargs):
        if self.request.method == 'GET':
            return InventoryReadSerializer(*args, **kwargs)
        return InventoryWriteSerializer(*args, **kwargs)


class ServiceViewset(ModelViewSet):
    queryset = Service.objects.all()
    serializer_class = ServiceSerializer
    permission_classes = [IsAdminRole]


class CheckServicePrice(APIView):
    @swagger_auto_schema(
        operation_description="Get the price for a given service based on kv or quantity",
        responses={200: 'Price calculation successful', 400: 'Bad Request', 401: 'Unauthorized'}
    )
    def get(self, request, service_id: int, kv: str = None, quantity: int = None):
        if not request.user or not request.user.role.lower() == "admin":
            context = {
                "success": False,
                "message": "User is not authorized"
            }
            return Response(context, status=status.HTTP_401_UNAUTHORIZED)
        try:
            kv = Decimal(kv)
        except:
            context = {
                "success": False,
                "message": "Invalid input for kv"
            }
            return Response(context, status=status.HTTP_400_BAD_REQUEST)
        
        if not quantity and not kv:
            context = {
                "success": False,
                "message": "kv or quantity must be provided"
            }
            return Response(context, status=status.HTTP_400_BAD_REQUEST)
    
        service = get_object_or_404(Service, id=service_id)
        if service.price_per_sqr:
            price = service.price_per_sqr * kv
        else:
            price = service.price_per_qty * quantity
        
        if price < service.minimum_price:
            price = service.minimum_price

        context = {
            "success": True,
            "data": price
        }

        return Response(context, status=status.HTTP_200_OK)


class OrderReadView(generics.RetrieveAPIView):
    queryset = Order.objects.all()
    serializer_class = OrderReadSerializer
    # permission_classes = [IsManagerRole]


class OrderUpdateView(generics.UpdateAPIView):
    queryset = Order.objects.all()
    serializer_class = OrderCreateCustomSerializer
    permission_classes = [IsAdminRole]


class OrderDestroyView(generics.DestroyAPIView):
    queryset = Order.objects.all()
    serializer_class = OrderDeleteSerializer
    permission_classes = [IsAdminRole]


class PaperByType(APIView):
    def get(self, request, paper_type_id: int):
        paper_type = get_object_or_404(PaperType, id=paper_type_id)
        papers = Paper.objects.filter(paper_type=paper_type)
        serializer = PaperReadSerializer(papers, many=True)
        return Response(serializer.data)


class InventoryModelViewset(ModelViewSet):
    queryset = Inventory.objects.all()
    serializer_class = InventorySerializer
    permission_classes = [IsAdminRole]

