from django.urls import path
from .views import CategoryExpenseSummaryView



urlpatterns = [
    path('category-expense-summary/', CategoryExpenseSummaryView.as_view()),
]