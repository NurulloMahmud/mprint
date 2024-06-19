from django.urls import path
from .views import (
    CategoryExpenseSummaryView, PaperExpenseSummaryView,
    InventoryExpenseSummaryView, ManagerOrderSummaryView
    )



urlpatterns = [
    path('category-expense-summary/', CategoryExpenseSummaryView.as_view()),
    path('paper-expense-summary/', PaperExpenseSummaryView.as_view()),
    path('inventory-expense-summary/', InventoryExpenseSummaryView.as_view()),
    path('manager-order-summary/', ManagerOrderSummaryView.as_view()),
]