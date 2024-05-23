from rest_framework import serializers

from main.models import Branch, Service, Order


class OrderUpdateSerializer(serializers.ModelSerializer):
    class Meta:
        model=Order
        fields=['status']
    
    def update(self, instance, validated_data):
        user = self.context['request'].user
        if user.role.lower() != 'admin':
            if instance.status.name != 'Pending' and validated_data['status'].name == 'Pending':
                raise serializers.ValidationError('Order cannot be updated as Pending status')
            if instance.status.name in ["review", "completed"] and validated_data['status'].name.lower() == "pending":
                raise serializers.ValidationError('Order cannot be updated as Pending status')
        instance.status = validated_data.get('status', instance.status)
        instance.save()
        return instance

