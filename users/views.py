from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.viewsets import ModelViewSet
from rest_framework import status
from rest_framework.permissions import IsAuthenticated

from django.contrib.auth.models import User
from django.shortcuts import get_object_or_404

from .models import Role
from .permissions import IsManagementRole
from .serializers import RoleSerializer, UserListSerializer, UserRoleUpdateSerializer


class UserRoleViewset(ModelViewSet):
    queryset = Role.objects.all()
    serializer_class = RoleSerializer
    permission_classes = [IsManagementRole]


class UserRegisterView(APIView):
    """
    post:
    Register a new user.

    Register a new user by providing a username and password. The user will be created with an inactive status initially.

    ### Request Body

    - `username`: String, required. The username for the new user account.
    - `password`: String, required. The password for the new user account.

    ### Responses

    - `201 Created`: Successfully created the user.
        - `id`: Integer. The unique ID of the newly created user.

    - `400 Bad Request`: The required fields were not provided in the request body or were invalid.
    """
    def post(self, request):
        # Check if required fields are provided
        if 'username' not in request.data or 'password' not in request.data:
            return Response({'error': 'Missing username or password'}, status=400)

        # Create a new user
        user = User.objects.create_user(
            username=request.data['username'],
            password=request.data['password'],
            is_active=False,
        )
        return Response({'id': user.id}, status=201)


class UserListView(APIView):
    def get(self, request):
        users = User.objects.all()
        serialized_users = UserListSerializer(users, many=True)

        context = {
            "success": True,
            "data": serialized_users.data,
        }
        return Response(context, status=status.HTTP_200_OK)


class UserUpdateAPIView(APIView):
    permission_classes = [IsAuthenticated, IsManagementRole]

    def put(self, request, user_id):
        user = get_object_or_404(User, pk=user_id)
        serializer = UserRoleUpdateSerializer(user, data=request.data)
        
        if serializer.is_valid():
            serializer.save()
            context = {
                "success": True, 
                "message": 'User and role updated successfully.',
                "data": serializer.data
                }
            return Response(context, status=status.HTTP_200_OK)
        
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

