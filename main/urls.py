from django.urls import path, include

from rest_framework.routers import DefaultRouter


from .views import (
    StatusViewSet, BranchViewset,
    PaperDetailUpdateDestroyView, PaperCreateView,
    PaperStockListCreateView, PaperStockUpdateDestroyAPIView,
    CustomerViewset, OrderListView,
    OrderCreateView, PaperListView,
    PaperTypeViewset, PaperRetrieveUpdateDestroyView
)

router = DefaultRouter()
router.register(r'status', StatusViewSet, basename='status')
router.register(r'branch', BranchViewset, basename='branch')
router.register(r'customer', CustomerViewset, basename='customer')
router.register(r'paper_type', PaperTypeViewset, basename='paper_type')


urlpatterns = [
    path('paper/', PaperCreateView.as_view()),
    path('paper/list/', PaperListView.as_view()),
    path('paper/<int:id>/', PaperRetrieveUpdateDestroyView.as_view()),
    path('paper/stock/', PaperStockListCreateView.as_view()),
    path('paper/stock/<int:id>/', PaperStockUpdateDestroyAPIView.as_view()),
    path('orders/list/', OrderListView.as_view()),
    path('orders/create/', OrderCreateView.as_view()),

    # viewsets endpoints
    path('', include(router.urls))
]