from django.urls import path
from accounts.views import LoginView, SignUpView, VerifyEmailView
from rest_framework_simplejwt.views import (TokenObtainPairView, TokenRefreshView)

urlpatterns = [
    path('token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('login/', LoginView.as_view(), name='login'),
    path('signup/', SignUpView.as_view() , name='signup' ),
    path('email-verify/', VerifyEmailView.as_view(), name="email-verify"),
]