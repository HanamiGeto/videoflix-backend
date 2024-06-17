from django.urls import path

from accounts.views import SignUpView, VerifyEmailView



urlpatterns = [
    path('signup/', SignUpView.as_view() , name='signup' ),
    path('email-verify/', VerifyEmailView.as_view(), name="email-verify"),
]