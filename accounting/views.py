from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.viewsets import ModelViewSet

from .models import ExpenseCategory, Expenses
from .serializers import ExpenseCategorySerializer
from users.permissions import IsAdminRole



class ExpenseCategoryViewSet(ModelViewSet):
    queryset = ExpenseCategory.objects.all()
    serializer_class = ExpenseCategorySerializer
    permission_classes = [IsAdminRole]


class ExpensesModelViewset(ModelViewSet):
    queryset = Expenses.objects.all()
    serializer_class = ExpenseCategorySerializer
    permission_classes = [IsAdminRole]


