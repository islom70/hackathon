from rest_framework import serializers
from rest_framework.exceptions import ValidationError

from accounts.models import CustomUser


class UserRegisterSerializer(serializers.Serializer):
    username = serializers.CharField(max_length=255, required=True)
    email = serializers.EmailField(required=True)
    password1 = serializers.CharField(max_length=255, required=True)
    password2 = serializers.CharField(max_length=255, required=True)

    class Meta:
        model = CustomUser
        fields = ['username', 'email', 'password1', 'password2']

    def validate(self, attrs):
        password1 = attrs.pop('password1')
        password2 = attrs.pop('password2')
        username = attrs.get('username')
        email = attrs.get('email')
        if CustomUser.objects.filter(username=username).exists():
            raise serializers.ValidationError('Username already exists')
        if CustomUser.objects.filter(email=email).exists():
            raise serializers.ValidationError('Email already exists')
        if password1 != password2:
            raise serializers.ValidationError('Passwords do not match!')
        attrs['password'] = password1
        return attrs


class LoginSerializer(serializers.Serializer):
    username = serializers.CharField()
    password = serializers.CharField()


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = CustomUser
        fields = ['id', 'username', 'email']