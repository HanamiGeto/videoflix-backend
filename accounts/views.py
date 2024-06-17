from rest_framework.generics import GenericAPIView
from rest_framework import status
from rest_framework.response import Response
from django.contrib.sites.shortcuts import get_current_site
from django.urls import reverse
import jwt
from .models import CustomUser
from .serializers import SignUpSerializer, EmailVerificationSerializer
from .utils import Util
from rest_framework_simplejwt.tokens import RefreshToken


class SignUpView(GenericAPIView):
    serializer_class = SignUpSerializer
    
    def post(self, request):
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.save()
        user_data = serializer.data

        token = RefreshToken.for_user(user).access_token

        current_site = get_current_site(request).domain
        relative_link = reverse('email-verify')
        absurl = f'https://{current_site}{relative_link}?token={token}'
        email_body = f'Hi {user.username}, use the link below to verify your email \n{absurl}'
        email_data = {'email_body': email_body, 'to_email': user.email, 'email_subject': 'Verify your email'}

        Util.send_email(email_data)

        return Response(user_data, status=status.HTTP_201_CREATED)
    
class VerifyEmailView(GenericAPIView):
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