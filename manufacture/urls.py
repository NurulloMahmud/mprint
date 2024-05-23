from django.urls import path

from .views import (
    OrderStatusAutoChange, OrderStatusChange,
    OrderListByStatusAPIView, OrderListByUser,
    CompletedOrdersList
)



urlpatterns = [
    path('status/change/<int:pk>/', OrderStatusChange.as_view()),
    path('status/auto/change/<int:pk>/', OrderStatusAutoChange.as_view()),
    path('status/list/<int:status>/', OrderListByStatusAPIView.as_view()),
    path('orders/list/', OrderListByUser.as_view()),
    path('orders/completed/list/', CompletedOrdersList.as_view()),
]