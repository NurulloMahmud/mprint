from django.db.models import Sum
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.viewsets import ModelViewSet
from rest_framework import generics

from .models import ExpenseCategory, Expenses
from .serializers import ExpenseCategorySerializer, PaymentMethodSerializer, OrderPaymentReadSerializer, OrderPaymentWriteSerializer \
    , CustomerDebtReadSerializer
from users.permissions import IsAdminRole, IsManagerRole
from main.models import PaymentMethod, OrderPayment, Customer, CustomerDebt
from drf_yasg.utils import swagger_auto_schema
from drf_yasg import openapi




class ExpenseCategoryViewSet(ModelViewSet):
    queryset = ExpenseCategory.objects.all()
    serializer_class = ExpenseCategorySerializer
    permission_classes = [IsAdminRole]


class ExpensesModelViewset(ModelViewSet):
    queryset = Expenses.objects.all()
    serializer_class = ExpenseCategorySerializer
    permission_classes = [IsAdminRole]


class PaymentMethodViewSet(ModelViewSet):
    queryset = PaymentMethod.objects.all()
    serializer_class = PaymentMethodSerializer
    permission_classes = [IsAdminRole]


class OrderPaymentViewset(ModelViewSet):
    queryset = OrderPayment.objects.all()
    permission_classes = [IsManagerRole]

    def get_serializer_class(self):
        if self.action in ['list', 'retrieve']:
            return OrderPaymentReadSerializer
        return OrderPaymentWriteSerializer


class CustomerDebtListView(generics.ListAPIView):
    serializer_class = CustomerDebtReadSerializer
    permission_classes = [IsManagerRole]

    def get_queryset(self):
        user = self.request.user
        if user.role.lower() != 'admin':
            return OrderPayment.objects.filter(branch=user.branch)
        return OrderPayment.objects.all()


class DebtListByCustomer(APIView):
    permission_classes = [IsManagerRole]

    @swagger_auto_schema(
        operation_description="Retrieve list of debts for a specific customer",
        responses={
            200: openapi.Response(
                description="List of debts for the specified customer",
                examples={
                    "application/json": [
                        {
                            "id": 5,
                            "order": [
                                {
                                    "id": 23,
                                    "name": "test number of product per list 10",
                                    "final_price": 2025.0,
                                    "date": "2024-05-16",
                                    "status__name": "Pending"
                                }
                            ],
                            "customer": {
                                "id": 1,
                                "name": "test customer1",
                                "phone": "123456789",
                                "email": "testingemail1@gmail.com",
                                "telegram_id": 111234
                            },
                            "amount": "1975.00",
                            "last_update": "2024-05-16"
                        }
                    ]
                }
            )
        }
    )
    def get(self, request, pk):
        customer = Customer.objects.get(id=pk)
        debts = CustomerDebt.objects.filter(customer=customer)
        serializer = CustomerDebtReadSerializer(debts, many=True)
        return Response(serializer.data)