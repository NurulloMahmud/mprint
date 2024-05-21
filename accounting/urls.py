from django.urls import path, include
from .views import ExpenseCategoryViewSet, ExpensesModelViewset, OrderPaymentViewset, PaymentMethodViewSet
from rest_framework.routers import DefaultRouter

router = DefaultRouter()
router.register(r'expense_category', ExpenseCategoryViewSet, basename='expense_category')
router.register(r'expenses', ExpensesModelViewset, basename='expenses')
router.register(r'payment_method', PaymentMethodViewSet, basename='payment_method')
router.register(r'payment', OrderPaymentViewset, basename='payment')



urlpatterns = [
    path('', include(router.urls))
]