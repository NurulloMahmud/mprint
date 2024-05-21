from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.viewsets import ModelViewSet

from .models import ExpenseCategory, Expenses
from .serializers import ExpenseCategorySerializer, PaymentMethodSerializer
from users.permissions import IsAdminRole, IsManagerRole
from main.models import PaymentMethod



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


# class OrderPayment