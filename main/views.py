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
    Paper, Service
)

from .serializers import (
    BranchSerializer, StatusSerializer, 
    PaperReadSerializer, PaperWriteSerializer,
    CustomerSerializer, OrderReadSerializer,
    OrderWriteSerializer, OrderCreateSerializer,
    PaperTypeSerializer, InventoryReadSerializer,
    InventoryWriteSerializer, ServiceSerializer
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


class OrderCreateView(generics.CreateAPIView):
    queryset = Order.objects.all()
    serializer_class = OrderCreateCustomSerializer


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

