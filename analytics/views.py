from rest_framework.views import APIView
from rest_framework.response import Response
from django.db.models import Sum, Count, F
from rest_framework import status

from accounting.models import (
    PaperExpenses, Expenses, ExpenseCategory, InventoryExpense
)
from main.models import (
    OrderManager, Order
)
from users.permissions import IsAdminRole

from .serializers import CategoryTotalSerializer
from datetime import datetime



class CategoryExpenseSummaryView(APIView):
    permission_classes = [IsAdminRole]
    def get(self, request):
        # Retrieve the start and end date from the request
        start_date = request.query_params.get('start_date')
        end_date = request.query_params.get('end_date')

        # Validate date inputs
        if not start_date or not end_date:
            return Response({'error': 'Please provide both start_date and end_date parameters'}, status=status.HTTP_400_BAD_REQUEST)
        
        try:
            start_date = datetime.strptime(start_date, '%Y-%m-%d').date()
            end_date = datetime.strptime(end_date, '%Y-%m-%d').date()
        except ValueError:
            return Response({'error': 'Invalid date format. Use YYYY-MM-DD.'}, status=status.HTTP_400_BAD_REQUEST)
        
        # Aggregate the total amount spent for each category within the date range
        expenses_summary = Expenses.objects.filter(date__range=(start_date, end_date)) \
            .values('category__name') \
            .annotate(total_amount=Sum('amount')) \
            .order_by('category__name')

        # Format the data
        summary_data = [
            {
                'name': expense['category__name'],
                'total_amount': expense['total_amount']
            }
            for expense in expenses_summary
        ]
        
        # Serialize the data
        serializer = CategoryTotalSerializer(summary_data, many=True)
        
        return Response(serializer.data, status=status.HTTP_200_OK)

class PaperExpenseSummaryView(APIView):
    permission_classes = [IsAdminRole]
    def get(self, request):
        # Retrieve the start and end date from the request
        start_date = request.query_params.get('start_date')
        end_date = request.query_params.get('end_date')

        # Validate date inputs
        if not start_date or not end_date:
            return Response({'error': 'Please provide both start_date and end_date parameters'}, status=status.HTTP_400_BAD_REQUEST)
        
        try:
            start_date = datetime.strptime(start_date, '%Y-%m-%d').date()
            end_date = datetime.strptime(end_date, '%Y-%m-%d').date()
        except ValueError:
            return Response({'error': 'Invalid date format. Use YYYY-MM-DD.'}, status=status.HTTP_400_BAD_REQUEST)
        
        # Aggregate the total amount spent within the date range
        total_amount = PaperExpenses.objects.filter(created_at__range=(start_date, end_date)) \
            .aggregate(total_amount=Sum('amount'))['total_amount'] or 0

        # Prepare the data
        summary_data = {
            'total_amount': total_amount
        }
        
        return Response(summary_data, status=status.HTTP_200_OK)

class InventoryExpenseSummaryView(APIView):
    permission_classes = [IsAdminRole]
    def get(self, request):
        # Retrieve the start and end date from the request
        start_date = request.query_params.get('start_date')
        end_date = request.query_params.get('end_date')

        # Validate date inputs
        if not start_date or not end_date:
            return Response({'error': 'Please provide both start_date and end_date parameters'}, status=status.HTTP_400_BAD_REQUEST)
        
        try:
            start_date = datetime.strptime(start_date, '%Y-%m-%d').date()
            end_date = datetime.strptime(end_date, '%Y-%m-%d').date()
        except ValueError:
            return Response({'error': 'Invalid date format. Use YYYY-MM-DD.'}, status=status.HTTP_400_BAD_REQUEST)
        
        # Aggregate the total amount spent within the date range
        total_amount = InventoryExpense.objects.filter(created_at__range=(start_date, end_date)) \
            .aggregate(total_amount=Sum('amount'))['total_amount'] or 0

        # Prepare the data
        summary_data = {
            'total_amount': total_amount
        }
        
        return Response(summary_data, status=status.HTTP_200_OK)

class ManagerOrderSummaryView(APIView):

    def get(self, request):
        # Retrieve the start and end date from the request
        start_date = request.query_params.get('start_date')
        end_date = request.query_params.get('end_date')

        # Validate date inputs
        if not start_date or not end_date:
            return Response({'error': 'Please provide both start_date and end_date parameters'}, status=status.HTTP_400_BAD_REQUEST)
        
        try:
            start_date = datetime.strptime(start_date, '%Y-%m-%d').date()
            end_date = datetime.strptime(end_date, '%Y-%m-%d').date()
        except ValueError:
            return Response({'error': 'Invalid date format. Use YYYY-MM-DD.'}, status=status.HTTP_400_BAD_REQUEST)
        
        # Aggregate the data
        summary = OrderManager.objects.filter(created_at__range=(start_date, end_date)) \
            .values(manager=F('manager__username')) \
            .annotate(order_count=Count('order'), total_amount=Sum('order__final_price')) \
            .order_by('manager')

        # Format the data for response
        summary_data = [
            {
                'manager': entry['manager_username'],
                'order_count': entry['order_count'],
                'total_amount': entry['total_amount']
            }
            for entry in summary
        ]
        
        return Response(summary_data, status=status.HTTP_200_OK)

