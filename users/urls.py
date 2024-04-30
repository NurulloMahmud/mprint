from django.urls import path, include
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
)

from rest_framework.routers import DefaultRouter

from .views import (
    UserRegisterView, UserUpdateView,
    UserListView, 
            )


router = DefaultRouter()
# router.register(r'roles', UserRoleViewset, basename='roles')



urlpatterns = [
    path('register/', UserRegisterView.as_view(), name='register'),
    path('users/', UserListView.as_view(), name='user-list'),
    path('update-user/<int:pk>/', UserUpdateView.as_view(), name='user-update'),

    # router's urls
    path('', include(router.urls)),

    # Your other URLs...
    path('api/token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('api/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
]
