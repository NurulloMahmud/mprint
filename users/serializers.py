from rest_framework import serializers

from django.contrib.auth import get_user_model
from django.contrib.auth.password_validation import validate_password

from main.models import CustomUser
from main.serializers import BranchSerializer

from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from rest_framework import exceptions

class CustomTokenObtainPairSerializer(TokenObtainPairSerializer):
    def validate(self, attrs):
        data = super().validate(attrs)
        # Check if user is active
        if not self.user.is_active:
            raise exceptions.AuthenticationFailed('User is not approved by admin yet.')
        return data



User = get_user_model()

class UserRegistrationSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True, required=True, validators=[validate_password])
    username = serializers.CharField(required=True)

    class Meta:
        model = User
        fields = ('username', 'password')

    def validate_username(self, value):
        # Check for existing username
        if User.objects.filter(username=value).exists():
            raise serializers.ValidationError("This username is already in use.")
        return value

    def create(self, validated_data):
        user = User.objects.create(
            username=validated_data['username']
        )
        user.set_password(validated_data['password'])
        user.is_active = False  # Set user as inactive
        user.save()
        return user


class UserListSerializer(serializers.ModelSerializer):
    branch = BranchSerializer()
    class Meta:
        model = CustomUser
        fields = ['id', 'username', 'is_active', 'branch', 'role']


class UserUpdateSerializer(serializers.ModelSerializer):
    class Meta:
        model = CustomUser
        fields = ['id', 'username', 'is_active', 'branch', 'role']
