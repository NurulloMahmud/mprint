from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.viewsets import ModelViewSet
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from rest_framework import generics

from rest_framework_simplejwt.views import TokenObtainPairView

from drf_yasg.utils import swagger_auto_schema
from drf_yasg import openapi

from django.contrib.auth.models import User
from django.shortcuts import get_object_or_404

from main.models import CustomUser
from .serializers import (
    UserRegistrationSerializer, UserListSerializer,
    UserUpdateSerializer, CustomTokenObtainPairSerializer
)

from .permissions import (
    IsAdminRole
)


class CustomTokenObtainPairView(TokenObtainPairView):
    serializer_class = CustomTokenObtainPairSerializer


class UserRegisterView(generics.CreateAPIView):
    queryset = CustomUser.objects.all()
    serializer_class = UserRegistrationSerializer


class UserListView(generics.ListAPIView):
    queryset = CustomUser.objects.all()
    serializer_class = UserListSerializer
    permission_classes = [IsAdminRole]


class UserUpdateView(generics.UpdateAPIView):
    queryset = CustomUser.objects.all()
    serializer_class = UserUpdateSerializer
    permission_classes = [IsAdminRole]


class UserDetails(APIView):
    permission_classes = [IsAuthenticated]

    @swagger_auto_schema(
        operation_description="Retrieve details of the authenticated user",
        responses={
            200: openapi.Response(
                description="User details retrieved successfully",
                examples={
                    "application/json": {
                        "id": 1,
                        "username": "john_doe",
                        "is_active": True,
                        "branch": {
                            "id": 1,
                            "name": "Main Branch"
                        },
                        "role": "admin"
                    }
                }
            ),
            401: openapi.Response(description="Authentication credentials were not provided or are invalid")
        }
    )
    def get(self, request):
        user = request.user
        serializer = UserListSerializer(user)
        return Response(serializer.data)

