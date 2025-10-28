from django.contrib.auth.password_validation import validate_password
from rest_framework import serializers

from user.models import User


class LoginSerializer(serializers.Serializer):
    phone = serializers.CharField()
    password = serializers.CharField(write_only=True)


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = '__all__'


class RegisterSerializer(serializers.ModelSerializer):
    phone = serializers.CharField(source='phone_number')
    first_name = serializers.CharField(required=False, allow_blank=True)
    last_name = serializers.CharField(required=False, allow_blank=True)
    password = serializers.CharField(write_only=True, required=True, validators=[validate_password])
    password2 = serializers.CharField(write_only=True, required=True)
    role = serializers.CharField(required=False, default='user')

    class Meta:
        model = User
        fields = (
            'phone',
            'first_name',
            'last_name',
            'password',
            'password2',
            'role'
        )

    def validate(self, attrs):
        if attrs['password'] != attrs['password2']:
            raise serializers.ValidationError({"password": "Passwords do not match"})
        return attrs

    def create(self, validated_data):
        password = validated_data.pop('password')
        validated_data.pop('password2')
        phone_number = validated_data.pop('phone_number')

        user = User.objects.create_user(
            phone_number=phone_number,
            password=password,
            first_name=validated_data.get('first_name', ''),
            last_name=validated_data.get('last_name', ''),
            role=validated_data.get('role', 'provider'),
            status=User.Status.new
        )
        return user
