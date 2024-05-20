from django.urls import path

from .views import (
    OrderStatusAutoChange, OrderStatusChange,
    OrderListByStatusAPIView, OrderListByUser
)



urlpatterns = [
    path('status/change/<int:pk>/', OrderStatusChange.as_view()),
    path('status/auto/change/<int:pk>/', OrderStatusAutoChange.as_view()),
    path('status/list/<str:status>/', OrderListByStatusAPIView.as_view()),
    path('orders/list/', OrderListByUser.as_view()),
]