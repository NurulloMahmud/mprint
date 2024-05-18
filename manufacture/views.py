from django.shortcuts import get_object_or_404

from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework import generics
from rest_framework.permissions import IsAuthenticated 

from drf_yasg.utils import swagger_auto_schema
from drf_yasg import openapi

from main.models import Branch, Service, Order, Status
from users.permissions import IsAdminRole, IsManagerRole, IsPrinterRole, IsFactoryRole

from .serializers import OrderUpdateSerializer
from main.serializers import OrderReadSerializer


class OrderStatusAutoChange(APIView):
    permission_classes = [IsAuthenticated]

    @swagger_auto_schema(
        operation_description="Change the status of an order based on user role",
        responses={
            200: openapi.Response(description="Successful operation", examples={"application/json": {"success": True}}),
            404: openapi.Response(description="Order not found"),
            403: openapi.Response(description="Permission denied")
        },
        manual_parameters=[
            openapi.Parameter(
                'pk', openapi.IN_PATH, description="Order ID", type=openapi.TYPE_INTEGER, required=True
            )
        ]
    )
    def post(self, request, pk):
        order = get_object_or_404(Order, id=pk)
        if request.user.role.lower() in ["admin", "manager"]:
            status_obj = Status.objects.get_or_create(name="Pechat")
        elif request.user.role.lower() == "Pechat":
            status_obj = Status.objects.get_or_create(name="Qayta ishlash")
        elif request.user.role.lower() == "qayta ishlash":
            status_obj = Status.objects.get_or_create(name="Final")
        order.status = status_obj
        order.save()
        return Response({"success": True})


class OrderStatusChange(generics.UpdateAPIView):
    queryset = Order.objects.all()
    serializer_class = OrderUpdateSerializer
    permission_classes = [IsManagerRole]

    def get_serializer_context(self):
        return {"request": self.request}

class OrderListByStatusAPIView(generics.ListAPIView):
    serializer_class = OrderReadSerializer
    permission_classes = [IsManagerRole]

    def get_queryset(self):
        status = self.kwargs['status']
        return Order.objects.filter(status__name=status)

