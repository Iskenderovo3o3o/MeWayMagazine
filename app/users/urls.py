from django.urls import path
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView, TokenVerifyView

from .views import CreateUserView

urlpatterns = [
    path('register/', CreateUserView.as_view(), name='register'),
    path('login_token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('login_token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('login_token/verify/', TokenVerifyView.as_view(), name='token_verify'),
]