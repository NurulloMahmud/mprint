from rest_framework import serializers

from main.models import Branch, Service, Order


class OrderUpdateSerializer(serializers.ModelSerializer):
    class Meta:
        model=Order
        fields=['status']

