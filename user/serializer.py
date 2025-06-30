from rest_framework import serializers

from user.models import User


class LoginSerializer(serializers.Serializer):
    phone = serializers.CharField()
    password = serializers.CharField(write_only=True)


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = '__all__'
