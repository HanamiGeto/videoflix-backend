from rest_framework import serializers
from .models import CustomUser

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