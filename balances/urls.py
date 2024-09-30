from django.urls import path
from .views import (
    CloseMonth, StakeHolderListView,
    StakeHolderUpdateDestroyView, ExpensesListView,
    ExpensesCreateView,
)


urlpatterns = [
    path('close-month/', CloseMonth.as_view()),
    path('stakeholder/list/', StakeHolderListView.as_view()),
    path('stakeholder/update/<int:pk>/', StakeHolderUpdateDestroyView.as_view()),
    path('expenses/list/', ExpensesListView.as_view()),
    path('expenses/create/', ExpensesCreateView.as_view()),
]