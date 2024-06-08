from django.urls import path, include
from .views import ExpenseCategoryViewSet, ExpensesModelViewset, OrderPaymentViewset, PaymentMethodViewSet \
    , DebtListByCustomer, CustomerDebtListView, OrdersDebtList, \
    InventoryViewset, InventoryExpenseViewset, PaperUsageSummaryView \
    , InventoryExpenseSummaryView, InventoryExpenseCreateView, \
    OrderDetailView, OrderDebtListView, OrderDebtByCustomerListView
from rest_framework.routers import DefaultRouter

router = DefaultRouter()
router.register(r'expense_category', ExpenseCategoryViewSet, basename='expense_category')
router.register(r'expenses', ExpensesModelViewset, basename='expenses')
router.register(r'payment_method', PaymentMethodViewSet, basename='payment_method')
router.register(r'payment', OrderPaymentViewset, basename='payment')
router.register(r'inventory', InventoryViewset, basename='inventory')
router.register(r'inventory_expense', InventoryExpenseViewset, basename='inventory_expense')



urlpatterns = [
    path('', include(router.urls)),
    path('customer/debt/<int:pk>/', DebtListByCustomer.as_view()),
    path('customers/debt/', CustomerDebtListView.as_view()),
    path('orders/debt/list/', OrdersDebtList.as_view()),
    path('paper-usage-summary/', PaperUsageSummaryView.as_view()),
    path('inventory-expense-summary/', InventoryExpenseSummaryView.as_view()),
    path('inventory-expense-create/', InventoryExpenseCreateView.as_view()),
    path('order/<int:pk>/', OrderDetailView.as_view()),
    path('order/debt/list/', OrderDebtListView.as_view()),
    path('order/debt/customer/<int:pk>/', OrderDebtByCustomerListView.as_view()),
]