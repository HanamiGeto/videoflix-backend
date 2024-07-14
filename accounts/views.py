from django.shortcuts import render
from rest_framework.generics import GenericAPIView
from rest_framework import status
from rest_framework.response import Response
from django.contrib.sites.shortcuts import get_current_site
from django.urls import reverse
import jwt
from .models import CustomUser
from .serializers import CustomPasswordTokenSerializer, LoginSerializer, SignUpSerializer, EmailVerificationSerializer
from .utils import Util
from rest_framework_simplejwt.tokens import RefreshToken
from django.template.loader import render_to_string
from django_rest_passwordreset.views import ResetPasswordConfirm
from django_rest_passwordreset.models import ResetPasswordToken

class SignUpView(GenericAPIView):
    authentication_classes = []
    permission_classes = []
    serializer_class = SignUpSerializer
    
    def post(self, request):
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.save()
        user_data = serializer.data

        token = RefreshToken.for_user(user).access_token

        current_site = get_current_site(request).domain
        relative_link = reverse('email-verify')
        absurl = f'http://{current_site}{relative_link}?token={token}'
        
        email_context = {
            'username': user.username,
            'verification_link': absurl
        }

        email_body = render_to_string('verification_email.html', email_context)
        email_data = {
            'email_body': email_body, 
            'to_email': user.email, 
            'email_subject': 'Verify your email'
        }

        Util.send_email(email_data)

        return Response(user_data, status=status.HTTP_201_CREATED)
    

def preview_email(request):
    email_context = {
        'username': 'JohnDoe',
        'verification_link': 'http://example.com/verify?token=exampletoken'
    }
    return render(request, 'verification_email.html', email_context)

def preview_pw_email(request):
    email_context = {
        'username': 'JohnDoe',
        'reset_password_url': 'http://example.com/verify?token=exampletoken'
    }
    return render(request, 'password_reset_email.html', email_context)
    
class VerifyEmailView(GenericAPIView):
    authentication_classes = []
    permission_classes = []
    serializer_class = EmailVerificationSerializer

    def get(self, request):
        token = request.GET.get('token')
        try:
            payload = jwt.decode(token, options={'verify_signature': False})
            print(payload)
            user = CustomUser.objects.get(id=payload['user_id'])
            if not user.is_verified:
                user.is_verified = True
                user.save()
            return Response({'email': 'successfully activated'}, status=status.HTTP_200_OK)
        except jwt.ExpiredSignatureError:
            return Response({'error': 'Activation Expired'}, status=status.HTTP_400_BAD_REQUEST)
        except jwt.InvalidTokenError:
            return Response({'error': 'Invalid token'}, status=status.HTTP_400_BAD_REQUEST)

class LoginView(GenericAPIView):
    authentication_classes = []
    permission_classes = []
    serializer_class = LoginSerializer

    def post(self, request):
        serializer = self.serializer_class(data=request.data)
        if serializer.is_valid():
            user_data = serializer.validated_data
            return Response(user_data, status=status.HTTP_200_OK)
        print(serializer.errors)

class CustomPasswordResetConfirmView(ResetPasswordConfirm):
    serializer_class = CustomPasswordTokenSerializer

    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            ResetPasswordToken.objects.filter(user=serializer.validated_data['user']).delete()
            return Response({"status": "Password reset successfully"}, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
