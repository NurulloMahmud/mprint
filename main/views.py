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
    Paper, PaperStock,
    Customer, Order,
    PaperType
)

from .serializers import (
    BranchSerializer, StatusSerializer, 
    PaperReadSerializer, PaperWriteSerializer,
    PaperStockReadSerializer, PaperStockWriteSerializer,
    CustomerSerializer, OrderReadSerializer,
    OrderWriteSerializer, OrderCreateSerializer,
    PaperTypeSerializer,
)


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
            required=['name', 'cost', 'price'],  # Specify the required fields here
            properties={
                'name': openapi.Schema(type=openapi.TYPE_STRING, description='Name of the paper'),
                'paper_type': openapi.Schema(type=openapi.TYPE_INTEGER, description='Foreign key ID of the paper type', format='int32'),
                'grammaj': openapi.Schema(type=openapi.TYPE_STRING, description='Weight/grammaj of the paper'),
                'cost': openapi.Schema(type=openapi.TYPE_NUMBER, format='decimal', description='Cost of the paper'),
                'price': openapi.Schema(type=openapi.TYPE_NUMBER, format='decimal', description='Price of the paper'),
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
            new_paper = Paper.objects.get(id=serializer.data['id'])
            PaperStock.objects.create(paper=new_paper, quantity=0)
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


class PaperStockListCreateView(generics.ListCreateAPIView):
    queryset = PaperStock.objects.all()
    serializer_class = PaperStockReadSerializer

    def get_serializer_class(self):
        if self.request.method == 'POST':
            return PaperStockWriteSerializer
        return PaperStockReadSerializer


class PaperStockUpdateDestroyAPIView(generics.RetrieveUpdateDestroyAPIView):
    queryset = PaperStock.objects.all()
    serializer_class = PaperStockWriteSerializer
    permission_classes = [IsAdminRole]


class CustomerViewset(ModelViewSet):
    queryset = Customer.objects.all()
    serializer_class = CustomerSerializer


class OrderListView(generics.ListAPIView):
    queryset = Order.objects.all()
    serializer_class = OrderReadSerializer


class OrderCreateView(generics.CreateAPIView):
    queryset = Order.objects.all()
    serializer_class = OrderCreateSerializer


class PaperTypeViewset(ModelViewSet):
    queryset = PaperType.objects.all()
    serializer_class = PaperTypeSerializer
    permission_classes = [IsAdminRole]

