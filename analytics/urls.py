from django.urls import path
from .views import (
    CategoryExpenseSummaryView, PaperExpenseSummaryView
    )



urlpatterns = [
    path('category-expense-summary/', CategoryExpenseSummaryView.as_view()),
    path('paper-expense-summary/', PaperExpenseSummaryView.as_view()),
]