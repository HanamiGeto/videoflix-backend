from django.urls import include, path
from accounts.views import CustomPasswordResetConfirmView, LoginView, SignUpView, VerifyEmailView, preview_email, preview_pw_email
from rest_framework_simplejwt.views import (TokenObtainPairView, TokenRefreshView)
from django_rest_passwordreset.views import ResetPasswordRequestToken, ResetPasswordValidateToken

urlpatterns = [
    path('token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('login/', LoginView.as_view(), name='login'),
    path('signup/', SignUpView.as_view() , name='signup' ),
    path('email-verify/', VerifyEmailView.as_view(), name="email-verify"),
    path('preview-email/', preview_email, name='preview_email'),
    path('preview-pw-email/', preview_pw_email, name='preview_pw_email'),
    path('password_reset/', include(([
        path('', ResetPasswordRequestToken.as_view(), name='reset-password-request'),
        path('validate_token/', ResetPasswordValidateToken.as_view(), name='reset-password-validate'),
        path('confirm/', CustomPasswordResetConfirmView.as_view(), name='reset-password-confirm'),
    ], 'password_reset'), namespace='password_reset')),    
]