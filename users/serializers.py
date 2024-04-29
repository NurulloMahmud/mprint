from rest_framework import serializers

from django.contrib.auth import get_user_model

from .models import Role


User = get_user_model()



class UserListSerializer(serializers.ModelSerializer):
    role = serializers.SerializerMethodField()

    class Meta:
        model = User
        fields = ['username', 'is_active', 'role']
    
    def get_role(self, obj):
        if hasattr(obj, 'role'):
            return obj.role.name
        return None



class RoleSerializer(serializers.ModelSerializer):
    class Meta:
        model = Role
        fields = '__all__'


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
