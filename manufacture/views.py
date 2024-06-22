from django.shortcuts import get_object_or_404
from django.db.models import Q

from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework import generics
from rest_framework.permissions import IsAuthenticated 

from drf_yasg.utils import swagger_auto_schema
from drf_yasg import openapi

from main.models import Branch, Service, Order, Status, Inventory, ServiceOrder
from users.permissions import IsAdminRole, IsManagerRole, IsPrinterRole, IsFactoryRole

from .serializers import OrderUpdateSerializer, ActiveOrdersSerializer \
    , InventoryReadAdminSerializer, InventoryReadManagerSerializer \
    , InventoryUpdateSerializer, PechatUserJobSerializer, ServiceOrderByUserSerializer
from main.serializers import OrderReadSerializer
from main.pagination import CustomPagination
from main.bot import send_telegram_message


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
            if order.status.name.lower() == "pending":
                status_obj = Status.objects.get(name="Pechat")
            elif order.status.name.lower() == "pechat":
                status_obj = Status.objects.get(name="Qayta ishlash")
                text = f"Sizning {order.id} raqamli buyurtmangiz pechat qilindi va qayta ishlash jarayoniga o'tkazildi.\nBuyurtma nomi: {order.name}"
                try:
                    send_telegram_message(text, 5769837552)
                except:
                    pass
            elif order.status.name.lower() == "qayta ishlash":
                status_obj = Status.objects.get(name="Completed")
                text = f"Sizning {order.id} raqamli buyurtmangiz tayyor bo'ldi.\nBuyurtma nomi: {order.name}"
                try:
                    send_telegram_message(text, 5769837552)
                except:
                    pass
            elif order.status.name.lower() == "review":
                status_obj = Status.objects.get(name="Completed")
            elif order.status.name.lower() == "completed":
                return Response({"success": False}, status=404)
        elif request.user.role.lower() == "pechat":
            status_obj = Status.objects.get(name="Qayta ishlash")
        elif request.user.role.lower() == "qayta ishlash":
            status_obj = Status.objects.get(name="Review")
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
    # permission_classes = [IsManagerRole]

    def get_queryset(self):
        status = self.kwargs['status']
        return Order.objects.filter(status__id=status)

class OrderListByUser(generics.ListAPIView):
    serializer_class = OrderReadSerializer
    permission_classes = [IsAuthenticated]
    pagination_class = CustomPagination

    @swagger_auto_schema(
        operation_description="Retrieve a list of orders for the authenticated user based on role and branch",
        responses={200: OrderReadSerializer(many=True)},
        manual_parameters=[
            openapi.Parameter(
                'Authorization', 
                openapi.IN_HEADER,
                description="Bearer Token",
                type=openapi.TYPE_STRING
            )
        ]
    )
    def get_queryset(self):
        """
        Retrieves a list of orders. Admin users get all orders,
        while other users get orders filtered by their branch and role.
        """
        user = self.request.user
        if user.role.lower() in ["admin", "manager"]:
            return Order.objects.all().order_by('-date').exclude(status__name="Completed")
        else:
            return Order.objects.filter(branch=user.branch, status__name=user.role.capitalize()).order_by('-date')

class CompletedOrdersList(generics.ListAPIView):
    serializer_class = OrderReadSerializer
    permission_classes = [IsManagerRole]
    pagination_class = CustomPagination

    def get_queryset(self):
        start_date = self.request.query_params.get('start_date')
        end_date = self.request.query_params.get('end_date')
        if not start_date or not end_date:
            return Order.objects.none()
        return Order.objects.filter(status__name="Completed", date__range=[start_date, end_date]).order_by('-date')

class ActiveOrdersList(generics.ListAPIView):
    serializer_class = ActiveOrdersSerializer
    permission_classes = [IsManagerRole]

    def get_queryset(self):
        return Order.objects.all().exclude(status__name="Completed").values('id', 'name', 'final_price', 'date')

class InventoryListAPIView(generics.ListAPIView):
    queryset = Inventory.objects.all()
    serializer_class = InventoryReadAdminSerializer
    permission_classes = [IsManagerRole]

    def get_queryset(self):
        if self.request.user.role.lower() == "manager":
            return Inventory.objects.filter(branch=self.request.user.branch).order_by('id')
        return Inventory.objects.all().order_by('id')
    
    def get_serializer_class(self):
        if self.request.user.role.lower() == "manager":
            return InventoryReadManagerSerializer
        return InventoryReadAdminSerializer

class InventoryUpdateView(generics.UpdateAPIView):
    queryset = Inventory.objects.all()
    serializer_class = InventoryUpdateSerializer
    permission_classes = [IsAdminRole]

class OrderServiceByUser(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request, order_id):
        order_obj = get_object_or_404(Order, id=order_id)
        if request.user.role.lower() == "pechat":
            services = ServiceOrder.objects.filter(
                order=order_obj,
                service__name__icontains="pechat",
                order__branch=request.user.branch,
                order__status__name="Pechat",
            ).order_by('-order__date')

            serializer = ServiceOrderByUserSerializer(services, many=True)

            return Response(serializer.data)
        elif request.user.role.lower() == "qayta ishlash":
            services = ServiceOrder.objects.filter(
                Q(order=order_obj) &
                ~Q(service__name__icontains="pechat") &
                Q(order__branch=request.user.branch) &
                Q(order__status__name="Qayta ishlash")
            ).order_by('-order__date')

            serializer = ServiceOrderByUserSerializer(services, many=True)

            return Response(serializer.data)
        else:
            services = ServiceOrder.objects.filter(
                order=order_obj
            ).order_by('-order__date')

            serializer = ServiceOrderByUserSerializer(services, many=True)

            return Response(serializer.data)
