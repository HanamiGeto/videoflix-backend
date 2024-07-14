from django.conf import settings
from rest_framework import serializers
from .models import CustomUser
from django.contrib.auth import authenticate
from rest_framework_simplejwt.tokens import RefreshToken
from django.utils.translation import gettext_lazy as _
from django_rest_passwordreset.models import ResetPasswordToken
from django.utils import timezone
from datetime import timedelta

class SignUpSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True)
    class Meta:
        model = CustomUser
        fields = ['id', 'username', 'email', 'password']
        read_only_fields = ['id']

    def create(self, validated_data):
        user = CustomUser.objects.create_user(**validated_data)
        return user
    
class EmailVerificationSerializer(serializers.Serializer):
    token = serializers.CharField(max_length=555)

class LoginSerializer(serializers.ModelSerializer):
    email = serializers.EmailField()
    password = serializers.CharField(write_only=True)
    class Meta:
        model = CustomUser
        fields = ['email', 'password']

    def validate(self, data):
        email = data.get('email')
        password = data.get('password')

        if email and password:
            user = authenticate(request=self.context.get('request'), email=email, password=password)

            if user is None:
                raise serializers.ValidationError('Invalid login credentials')
            
            if not user.is_verified:
                raise serializers.ValidationError('Email is not verified')
            
            refresh = RefreshToken.for_user(user)
            return {
                'refresh': str(refresh),
                'access': str(refresh.access_token),
                'user': {
                    'id': user.id,
                    'username': user.username,
                    'email': user.email,
                }
            }
        else:
            raise serializers.ValidationError('Both email and password are required')
        
class CustomPasswordTokenSerializer(serializers.Serializer):
    password = serializers.CharField(label=_("Password"), style={'input_type': 'password'})
    password_confirm = serializers.CharField(label=_("Password Confirm"), style={'input_type': 'password'})
    token = serializers.CharField()

    def validate(self, data):
        if data['password'] != data['password_confirm']:
            raise serializers.ValidationError({"password": "The two password fields didn't match."})

        token = data.get('token')
        password_reset_token_validation_time = getattr(settings, 'DJANGO_REST_PASSWORDRESET_TOKEN_EXPIRY_TIME', 24)

        try:
            reset_password_token = ResetPasswordToken.objects.get(key=token)
        except ResetPasswordToken.DoesNotExist:
            raise serializers.ValidationError({"token": "Invalid or expired token"})

        expiry_date = reset_password_token.created_at + timedelta(hours=password_reset_token_validation_time)
        if timezone.now() > expiry_date:
            reset_password_token.delete()
            raise serializers.ValidationError({"token": "The token has expired"})

        if reset_password_token.user.check_password(data['password']):
            raise serializers.ValidationError({"password": "The new password cannot be the same as the old password."})

        data['user'] = reset_password_token.user
        return data

    def save(self, **kwargs):
        password = self.validated_data['password']
        user = self.validated_data['user']
        user.set_password(password)
        user.save()
