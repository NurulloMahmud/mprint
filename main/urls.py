from django.urls import path, include

from rest_framework.routers import DefaultRouter


from .views import (
    StatusViewSet, BranchViewset,
    PaperDetailUpdateDestroyView, PaperListCreateView,
)

router = DefaultRouter()
router.register(r'status', StatusViewSet, basename='status')
router.register(r'branch', BranchViewset, basename='branch')


urlpatterns = [
    path('paper/', PaperListCreateView.as_view()),
    path('paper/<int:id>/', PaperDetailUpdateDestroyView.as_view()),

    # viewsets endpoints
    path('', include(router.urls))
]