from rest_framework.response import Response
from rest_framework.viewsets import ModelViewSet
from rest_framework import generics
from rest_framework.views import APIView
from rest_framework import status

from django.shortcuts import get_object_or_404

from drf_yasg.utils import swagger_auto_schema
from drf_yasg import openapi

from .models import (
    Branch, Status,
    Customer, Order,
    PaperType, Inventory,
    Paper, Service, CustomerDebt,
    OrderPayment, ServiceOrder,
    OrderPics
)

from .serializers import (
    BranchSerializer, StatusSerializer, 
    PaperReadSerializer, PaperWriteSerializer,
    CustomerSerializer, OrderReadSerializer,
    PaperTypeSerializer, InventoryReadSerializer,
    InventoryWriteSerializer, ServiceSerializer,
)

from .custom import OrderCreateCustomSerializer


from users.permissions import IsAdminRole, IsManagerRole


class StatusViewSet(ModelViewSet):
    queryset = Status.objects.all()
    serializer_class = StatusSerializer
    permission_classes = (IsAdminRole,)


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


#
class PaperDetailUpdateDestroyView(APIView):
    def get(self, request, id: int):
        paper = get_object_or_404(Paper, id=id)
        serializer = PaperReadSerializer(paper)

        context = {
            "success": True,
            "data": serializer.data,
        }

        return Response(context, status=status.HTTP_200_OK)

    def put(self, request, id: int):

        if not request.user or request.user.role.lower() == "admin":
            context = {
                "success": False,
                "message": "user is not authorized"
            }
            return Response(context, status=status.HTTP_401_UNAUTHORIZED)
        
        paper = get_object_or_404(Paper, id=id)
        serializer = PaperWriteSerializer(paper, data=request.data)

        if serializer.is_valid():
            serializer.save()
            context = {
                "success": True,
                "message": "updated the object successfully",
                "data": serializer.data
            }

            return Response(context, status=status.HTTP_200_OK)
        context = {
            "success": False,
            "message": "invalid data input"
        }

        return Response(context, status=status.HTTP_400_BAD_REQUEST)
    
    def delete(self, request, id: int):

        if not request.user or request.user.role.lower() == "admin":
            context = {
                "success": False,
                "message": "user is not authorized"
            }
            return Response(context, status=status.HTTP_401_UNAUTHORIZED)
        
        paper = get_object_or_404(Paper, id=id)
        paper.delete()

        context = {
            "success": True,
            "message": "data has been deleted successfully"
        }

        return Response(context, status=status.HTTP_204_NO_CONTENT)


class CustomerViewset(ModelViewSet):
    queryset = Customer.objects.all()
    serializer_class = CustomerSerializer


class OrderListView(generics.ListAPIView):
    queryset = Order.objects.all()
    serializer_class = OrderReadSerializer


class OrderCreateView(APIView):
    @swagger_auto_schema(
        operation_summary="Create a new Order",
        operation_description="Creates a new order with all related details including services and images.",
        request_body=openapi.Schema(
            type=openapi.TYPE_OBJECT,
            required=['name', 'customer_id', 'branch', 'paper_id', 'num_of_lists', 'total_sqr_meter', 'final_price', 'num_of_lists_per_paper', 'initial_payment_amount'],
            properties={
                'num_of_lists_per_paper': openapi.Schema(type=openapi.TYPE_INTEGER, description='Number of lists per paper'),
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
            branch_obj = get_object_or_404(Branch, id=data['branch'])
            paper_obj = get_object_or_404(Paper, id=data['paper_id'])
            # Ensure the default status is set if the order is new
            status_obj = Status.objects.get(name="Pending")
        except Exception as e:
            return Response({"success": False, "message": str(e)}, status=status.HTTP_400_BAD_REQUEST)

        try:
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
                final_price=data['final_price'],
                price_per_product=None,  # to be calculated
                status=status_obj,
                branch=branch_obj,
            )

            # Calculate prices and totals based on related service and paper costs
            total_service_price = 0
            for service_id in data.get('services', []):
                service_obj = get_object_or_404(Service, id=service_id)
                service_order = ServiceOrder(
                    service=service_obj,
                    order=order,
                    total_price=service_obj.minimum_price if service_obj.minimum_price else 0  # default to zero if not set
                )
                service_order.save()  # This will adjust price if below minimum in ServiceOrder save()
                total_service_price += service_order.total_price

            # Calculate paper price (simplified example, add error checking as necessary)
            num_of_papers = int(order.num_of_lists) // int(data['num_of_lists_per_paper'])
            paper_cost = paper_obj.price * num_of_papers if paper_obj.price else 0
            order.total_price = total_service_price + paper_cost

            # Calculate final price
            order.final_price = order.total_price  # Adjust as needed based on additional logic
            order.price_per_list = order.final_price / order.num_of_lists
            order.price_per_product = order.final_price / order.products_qty
            order.save()

            # Handle Payments and Debts
            if float(data.get('initial_payment_amount', 0)) < order.final_price:
                CustomerDebt.objects.create(customer=customer_obj, order=order, amount=order.final_price - float(data['initial_payment_amount']))
            if float(data.get('initial_payment_amount', 0)) > 0:
                OrderPayment.objects.create(order=order, amount=float(data['initial_payment_amount']))

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
            kv = float(kv)
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
    permission_classes = [IsManagerRole]


class OrderUpdateView(generics.UpdateAPIView):
    queryset = Order.objects.all()
    serializer_class = OrderCreateCustomSerializer
    permission_classes = [IsAdminRole]

