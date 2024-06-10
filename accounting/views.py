from django.db.models import Sum, Q, FloatField, F
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.viewsets import ModelViewSet
from rest_framework import generics

from .models import ExpenseCategory, Expenses, InventoryExpense
from .serializers import ExpenseCategorySerializer, PaymentMethodSerializer, OrderPaymentReadSerializer, OrderPaymentWriteSerializer \
    , CustomerDebtReadSerializer, OrdersDebtListSerializer, ExpensesWriteSerializer, ExpensesReadSerializer \
    , InventorySerializer, InventoryExpenseSerializer, PaperUsageSummarySerializer, InventoryExpenseSummarySerializer, \
    InventoryExpenseCreateSerializer, CustomerDebtListSerializer, OrderDetailSerializer
from users.permissions import IsAdminRole, IsManagerRole
from main.models import PaymentMethod, OrderPayment, Customer, CustomerDebt
from drf_yasg.utils import swagger_auto_schema
from drf_yasg import openapi

from main.models import Order, CustomerDebt, Inventory, Paper




class ExpenseCategoryViewSet(ModelViewSet):
    queryset = ExpenseCategory.objects.all()
    serializer_class = ExpenseCategorySerializer
    permission_classes = [IsAdminRole]

class ExpensesModelViewset(ModelViewSet):
    queryset = Expenses.objects.all()
    permission_classes = [IsAdminRole]

    def get_serializer_class(self):
        if self.action in ['list', 'retrieve']:
            return ExpensesReadSerializer
        return ExpensesWriteSerializer

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
    queryset = Customer.objects.all()
    serializer_class = CustomerDebtReadSerializer
    permission_classes = [IsAdminRole]

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
        debts = CustomerDebt.objects.filter(customer__id=pk)
        serializer = CustomerDebtReadSerializer(debts, many=True)
        return Response(serializer.data)

class OrdersDebtList(generics.ListAPIView):
    serializer_class = OrdersDebtListSerializer
    permission_classes = [IsManagerRole]

    def get_queryset(self):
        orders_with_debt = Order.objects.filter(Q(debt__amount__gt=0)).distinct()
        return orders_with_debt

class InventoryViewset(ModelViewSet):
    queryset = Inventory.objects.all()
    serializer_class = InventorySerializer
    permission_classes = [IsManagerRole]

    def get_queryset(self):
        if self.request.user.role.lower() == 'manager':
            if self.action in ['list', 'retrieve']:
                return Inventory.objects.all().exclude('amount')
        return Inventory.objects.all()

class InventoryExpenseViewset(ModelViewSet):
    queryset = Inventory.objects.all()
    serializer_class = InventoryExpenseSerializer
    permission_classes = [IsManagerRole]

class PaperUsageSummaryView(generics.ListAPIView):
    serializer_class = PaperUsageSummarySerializer
    permission_classes = [IsAdminRole]

    def get_queryset(self):
        start_date = self.request.query_params.get('start_date')
        end_date = self.request.query_params.get('end_date')

        if not start_date or not end_date:
            return Paper.objects.none()

        # Aggregate data from PaperExpenses within the date range
        return Paper.objects.filter(
            paperexpenses__created_at__range=[start_date, end_date]
        ).annotate(
            quantity=Sum('paperexpenses__quantity'),
            total_cost=Sum(F('paperexpenses__quantity') * F('cost'), output_field=FloatField()),
            total_price=Sum(F('paperexpenses__quantity') * F('price'), output_field=FloatField())
        )

class InventoryExpenseSummaryView(generics.ListAPIView):
    serializer_class = InventoryExpenseSummarySerializer

    def get_queryset(self):
        start_date = self.request.query_params.get('start_date')
        end_date = self.request.query_params.get('end_date')

        if not start_date or not end_date:
            return InventoryExpense.objects.none()  # Return an empty queryset if dates are not provided

        return InventoryExpense.objects.filter(
            created_at__range=[start_date, end_date]
        ).values('item__name').annotate(
            total_quantity=Sum('quantity'),
            total_amount=Sum(F('amount'))
        )

class InventoryExpenseCreateView(generics.CreateAPIView):
    serializer_class = InventoryExpenseCreateSerializer
    permission_classes = [IsManagerRole]
    queryset = InventoryExpense.objects.all()

class OrderDetailView(generics.RetrieveAPIView):
    serializer_class = OrderDetailSerializer
    permission_classes = [IsManagerRole]
    queryset = Order.objects.all()

class OrderDebtListView(generics.ListAPIView):
    serializer_class = CustomerDebtListSerializer
    permission_classes = [IsManagerRole]
    queryset = CustomerDebt.objects.all()

    def get_queryset(self):
        return CustomerDebt.objects.filter(amount__gt=0).order_by('customer__name', '-amount')

class OrderDebtByCustomerListView(APIView):
    permission_classes = [IsManagerRole]

    def get(self, request, pk):
        customer = Customer.objects.get(id=pk)
        debt = CustomerDebt.objects.filter(customer=customer).order_by('-amount', '-order__date')
        serializer = CustomerDebtListSerializer(debt, many=True)
        return Response(serializer.data)
