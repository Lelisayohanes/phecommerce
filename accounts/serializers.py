from .models import CustomUser
from rest_framework import serializers
from django.contrib.auth import authenticate

class CustomUserSerializer(serializers.ModelSerializer):
    """description"""
    class Meta:
        """description"""
        model = CustomUser
        fields = ("id","username","email")

class UserRegistrationSerializer(serializers.ModelSerializer):
    password_one = serializers.CharField(write_only=True)
    password_two = serializers.CharField(write_only=True)

    class Meta:
        model = CustomUser
        fields = ("id", "username", "email", "password_one", "password_two")

    def validate(self, attrs):
        if attrs['password_one'] != attrs['password_two']:
            raise serializers.ValidationError("Passwords do not match")

        password = attrs.get("password_one", "")
        if len(password) < 8:
            raise serializers.ValidationError("Passwords must be at least 8 characters!")
        return attrs

    def create(self, validated_data):
        password = validated_data.pop("password_one")
        validated_data.pop("password_two")
        return CustomUser.objects.create_user(password=password, **validated_data)

class UserLoginSerializer(serializers.Serializer):
    email = serializers.CharField()
    password = serializers.CharField(write_only = True)

    def validate(self, data):
        user = authenticate(**data)
        if user and user.is_active:
            return user
        raise serializers.ValidationError("Incorrect credentials")