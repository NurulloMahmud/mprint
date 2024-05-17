from django.urls import path, include

from rest_framework.routers import DefaultRouter


from .views import (
    StatusViewSet, BranchViewset,
    PaperDetailUpdateDestroyView, PaperCreateView,
    CustomerViewset, OrderListView, InventoryListAPIView,
    OrderCreateView, PaperListView,
    PaperTypeViewset, PaperRetrieveUpdateDestroyView,
    InventoryCreateAPIView, InventoryUpdateDestroyAPIView,
    ServiceViewset, CheckServicePrice,
    OrderReadView, OrderUpdateView, PaperByType
)

router = DefaultRouter()
router.register(r'status', StatusViewSet, basename='status')
router.register(r'branch', BranchViewset, basename='branch')
router.register(r'customer', CustomerViewset, basename='customer')
router.register(r'paper_type', PaperTypeViewset, basename='paper_type')
router.register(r'service', ServiceViewset, basename='service')


urlpatterns = [
    path('paper/', PaperCreateView.as_view()),
    path('paper/list/<int:paper_type_id>/', PaperByType.as_view()),
    path('paper/list/', PaperListView.as_view()),
    path('paper/<int:pk>/', PaperRetrieveUpdateDestroyView.as_view()),
    path('orders/list/', OrderListView.as_view()),
    path('orders/create/', OrderCreateView.as_view()),
    path('orders/detail/<int:pk>/', OrderReadView.as_view()),
    path('orders/update/<int:pk>/', OrderUpdateView.as_view()),
    path('inventory/list/', InventoryListAPIView.as_view()),
    path('inventory/create/', InventoryCreateAPIView.as_view()),
    path('inventory/<int:pk>/', InventoryUpdateDestroyAPIView.as_view()),
    path('check_service_price/<int:service_id>/<str:kv>/<int:quantity>/', CheckServicePrice.as_view()),

    # viewsets endpoints
    path('', include(router.urls))
]