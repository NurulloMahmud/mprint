from django.urls import path, include
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
)

from .views import (
    UserRegisterView, UserUpdateView,
    UserListView
        )



urlpatterns = [
    path('register/', UserRegisterView.as_view(), name='register'),
    path('list/', UserListView.as_view(), name='user-list'),
    path('update-user/<int:pk>/', UserUpdateView.as_view(), name='user-update'),

    # Your other URLs...
    path('api/token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('api/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
]
