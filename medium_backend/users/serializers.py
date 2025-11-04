from django.contrib.auth.password_validation import validate_password
from rest_framework import serializers

from .models import User


class UserSerializer(serializers.ModelSerializer):
    password = serializers.CharField(
        write_only=True, required=True, validators=[validate_password]
    )
    confirm_password = serializers.CharField(write_only=True, required=True)

    class Meta:
        model = User
        fields = (
            "email",
            "username",
            "first_name",
            "last_name",
            "dob",
            "gender",
            "password",
            "confirm_password",
        )
        extra_kwargs = {
            "first_name": {"required": False},
            "last_name": {"required": False},
            "dob": {"required": False},
            "gender": {"required": False},
        }

    def password_confirmation(self, validate_data):
        if attrs["password"] != attrs["confirm_password"]:
            raise serializers.ValidationError("Password must be same")
        return attrs

    def create(self, validated_data):
        # Remove password2 because the User model doesn't have it
        validated_data.pop("confirm_password")
        # Create the user using Django's create_user method (handles password hashing)
        user = User.objects.create_user(**validated_data)
        return user


class CustomUserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ["id", "username", "email", "is_active"]
