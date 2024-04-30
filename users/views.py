from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.viewsets import ModelViewSet
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from rest_framework import generics

from rest_framework_simplejwt.views import TokenObtainPairView

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

