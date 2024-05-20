from django.urls import path, include
from .views import ExpenseCategoryViewSet, ExpensesModelViewset
from rest_framework.routers import DefaultRouter

router = DefaultRouter()
router.register(r'expense_category', ExpenseCategoryViewSet, basename='expense_category')
router.register(r'expenses', ExpensesModelViewset, basename='expenses')



urlpatterns = [
    path('', include(router.urls))
]