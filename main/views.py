from rest_framework.response import Response
from rest_framework.viewsets import ModelViewSet
from rest_framework import generics
from rest_framework.views import APIView
from rest_framework import status

from django.shortcuts import get_object_or_404

from .models import (
    Product, Size,
    Branch, Status
)

from .serializers import (
    BranchSerializer, StatusSerializer,
    SizeReadSerializer, ProductReadSerializer,
    ProductWriteSerializer,
)


from users.permissions import IsAdminRole


class StatusViewSet(ModelViewSet):
    queryset = Status.objects.all()
    serializer_class = StatusSerializer
    permission_classes = (IsAdminRole,)


class BranchViewset(ModelViewSet):
    queryset = Branch.objects.all()
    serializer_class = BranchSerializer
    permission_classes = (IsAdminRole,)


class ProductListCreateView(APIView):
    def get(self, request):
        queryset = Product.objects.all()
        serializer = ProductReadSerializer(queryset, many=True)

        context = {
            "success": True,
            "data": serializer.data
        }

        return Response(context, status=status.HTTP_200_OK)
    
    def post(self, request):
        
        if not request.user or request.user.role.lower() == "admin":
            context = {
                "success": False,
                "message": "user is not authorized"
            }
            return Response(context, status=status.HTTP_401_UNAUTHORIZED)
        
        data = request.data
        serializer = ProductWriteSerializer(data=data)

        if serializer.is_valid():
            serializer.save()

            context = {
                "success": True,
                "message": "created successfully",
                "data": serializer.data,
            }

            return Response(context, status=status.HTTP_201_CREATED)
        
        context = {
            "success": False,
            "message": "Invalid data input or/and missing filed",
        }

        return Response(context, status=status.HTTP_400_BAD_REQUEST)


class ProductDetailUpdateDestroyView(APIView):
    def get(self, request, id: int):
        product = get_object_or_404(Product, id=id)
        serializer = ProductReadSerializer(product)

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
        
        product = get_object_or_404(Product, id=id)
        serializer = ProductWriteSerializer(product, data=request.data)

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
        
        product = get_object_or_404(Product, id=id)
        product.delete()

        context = {
            "success": True,
            "message": "data has been deleted successfully"
        }

        return Response(context, status=status.HTTP_204_NO_CONTENT)

