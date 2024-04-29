from django.urls import path, include

from rest_framework.routers import DefaultRouter


from .views import (
    StatusViewSet, BranchViewset,
    ProductDetailUpdateDestroyView, ProductListCreateView,
)

router = DefaultRouter()
router.register(r'status', StatusViewSet, basename='status')
router.register(r'branch', BranchViewset, basename='branch')


urlpatterns = [
    path('product/', ProductListCreateView.as_view()),
    path('product/<int:id>/', ProductDetailUpdateDestroyView.as_view()),

    # viewsets endpoints
    path('', include(router.urls))
]