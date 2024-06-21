from django.urls import path
from .views import (
    CategoryExpenseSummaryView, PaperExpenseSummaryView,
    InventoryExpenseSummaryView, ManagerOrderSummaryView,
    PaymentMethodIncomeSummaryView, TotalIncomeSummaryView,
    CustomerSummaryView, OrdersCountByStatusView
    )



urlpatterns = [
    path('category-expense-summary/', CategoryExpenseSummaryView.as_view()),
    path('paper-expense-summary/', PaperExpenseSummaryView.as_view()),
    path('inventory-expense-summary/', InventoryExpenseSummaryView.as_view()),
    path('manager-order-summary/', ManagerOrderSummaryView.as_view()),
    path('payment-method-income-summary/', PaymentMethodIncomeSummaryView.as_view()),
    path('total-income-summary/', TotalIncomeSummaryView.as_view()),
    path('customer-summary/', CustomerSummaryView.as_view()),
    path('orders-count-by-status/', OrdersCountByStatusView.as_view()),
]