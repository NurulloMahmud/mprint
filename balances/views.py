from rest_framework.views import APIView
from rest_framework import generics
from rest_framework.response import Response
from rest_framework import status
from datetime import datetime
from .models import BalanceSheet, Stakeholder, Expenses
from .serializers import (
    StakeHolderViewSerializer, StakeHolderWriteSerializer, 
    ExpensesViewSerializer, ExpensesWriteSerializer
)

from django.db.models import Sum
from decimal import Decimal



class CloseMonth(APIView):
    def post(self, request):
        from accounting.models import Expenses, InventoryExpense, PaperExpenses
        from main.models import OrderPayment

        year = request.data.get('year')
        month = request.data.get('month')

        if not year or not month:
            return Response({'error': 'Please provide both year and month parameters'}, status=status.HTTP_400_BAD_REQUEST)
        
        if BalanceSheet.objects.filter(date__year=year, date__month=month).exists():
            return Response({'error': 'Month already closed'}, status=status.HTTP_400_BAD_REQUEST)

        date_obj = datetime(year=int(year), month=int(month), day=1)

        total_expenses = Expenses.objects.filter(date__year=date_obj.year, date__month=date_obj.month).aggregate(Sum('amount'))['amount__sum'] or 0
        inventory_expenses = InventoryExpense.objects.filter(created_at__year=date_obj.year, created_at__month=date_obj.month).aggregate(Sum('amount'))['amount__sum'] or 0
        paper_expenses = PaperExpenses.objects.filter(created_at__year=date_obj.year, created_at__month=date_obj.month).aggregate(Sum('amount'))['amount__sum'] or 0
        total_incomes = OrderPayment.objects.filter(date__year=date_obj.year, date__month=date_obj.month).aggregate(Sum('amount'))['amount__sum'] or 0

        total_balance = Decimal(total_incomes) - Decimal(total_expenses) - Decimal(inventory_expenses) - Decimal(paper_expenses)

        botir_aka_obj = Stakeholder.objects.filter(name__icontains="botir").first()

        if total_balance < 0:
            today = datetime.now().date()
            
            Expenses.objects.create(
                date=today,
                amount=Decimal(total_balance),
                stakeholder=botir_aka_obj,
                description="Yopilgan oydan zarar"
            )
            return Response({'message': 'Month closed successfully'}, status=status.HTTP_200_OK)
        else:
            stake_holders = Stakeholder.objects.all()

            for stake_holder in stake_holders:
                balance = total_balance * stake_holder.percent / 100
                BalanceSheet.objects.create(
                    date=date_obj,
                    stakeholder=stake_holder,
                    balance=Decimal(balance)
                )

        return Response({'message': 'Month closed successfully'}, status=status.HTTP_200_OK)


class StakeHolderListView(generics.ListAPIView):
    serializer_class = StakeHolderViewSerializer
    queryset = Stakeholder.objects.all()


class StakeHolderUpdateDestroyView(generics.RetrieveUpdateDestroyAPIView):
    serializer_class = StakeHolderWriteSerializer
    queryset = Stakeholder.objects.all()


class ExpensesListView(generics.ListAPIView):
    serializer_class = ExpensesViewSerializer
    queryset = Expenses.objects.all()  

    def get_queryset(self):
        # get stakeholder id from query params
        stakeholder_id = self.request.query_params.get('stakeholder_id')

        if not stakeholder_id:
            return Expenses.objects.all()

        if stakeholder_id and not stakeholder_id.isdigit() or not Stakeholder.objects.filter(id=stakeholder_id).exists():
            raise ValueError('Invalid stakeholder ID')

        if stakeholder_id:
            if not Stakeholder.objects.filter(id=stakeholder_id).exists():
                raise ValueError('Stakeholder not found')
            
            return Expenses.objects.filter(stakeholder__id=stakeholder_id)
        else:
            return Expenses.objects.all()


class ExpensesCreateView(generics.CreateAPIView):
    serializer_class = ExpensesWriteSerializer
    queryset = Expenses.objects.all()

