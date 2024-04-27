from rest_framework import serializers

from django.contrib.auth.models import User

from .models import Role


class RoleSerializer(serializers.ModelSerializer):
    class Meta:
        model = Role
        fields = '__all__'


class UserSerializer(serializers.ModelSerializer):
    role = serializers.SerializerMethodField()
    class Meta:
        model = User
        fields = ['id', 'username', 'role']
    
    def get_role(self, obj):
        role = Role.objects.get(user=obj)
        return role.name


class UserRoleUpdateSerializer(serializers.ModelSerializer):
    role = RoleSerializer()

    class Meta:
        model = User
        fields = ['is_active', 'role']
        depth = 1

    def update(self, instance, validated_data):
        role_data = validated_data.pop('role', {})
        instance.is_active = validated_data.get('is_active', instance.is_active)
        instance.save()

        role, created = Role.objects.update_or_create(user=instance, defaults=role_data)
        return instance
