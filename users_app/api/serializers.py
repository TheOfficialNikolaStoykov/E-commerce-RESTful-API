from django.contrib.auth.models import User
from rest_framework import serializers

from users_app.models import *


class ProfileViewSerializer(serializers.ModelSerializer):
    
    class Meta:
        model = Profile
        fields = "__all__"
        
class ProfileUpdateSerializer(serializers.ModelSerializer):
    
    class Meta:
        model = Profile
        fields = ["first_name", "last_name", "phone_number", 
                  "address_line_1", "address_line_2", "city", "state", "postal_code", "country"]

class ProfileRegistrationSerializer(serializers.ModelSerializer):
    username = serializers.CharField(max_length=150, required=True)
    email = serializers.EmailField(required=True)
    password = serializers.CharField(write_only=True, required=True)


    class Meta:
        model = Profile
        fields = ["username", "email", "password", "first_name", "last_name", "phone_number",
                  "address_line_1", "address_line_2", "city", "state", "postal_code", "country"]

    def validate_username(self, value):
        if User.objects.filter(username=value).exists():
            raise serializers.ValidationError("Username already exists!")
        return value

    def validate_email(self, value):
        if User.objects.filter(email=value).exists():
            raise serializers.ValidationError("Email already exists!")
        return value

    def save(self, **kwargs):
        user = User(
            username=self.validated_data["username"],
            email=self.validated_data["email"]
        )
        password = self.validated_data["password"]
        user.set_password(password)
        user.save()

        profile = Profile(
            user=user,
            first_name=self.validated_data["first_name"],
            last_name=self.validated_data["last_name"],
            phone_number=self.validated_data["phone_number"],
            address_line_1=self.validated_data["address_line_1"],
            address_line_2=self.validated_data.get("address_line_2", ""),
            city=self.validated_data["city"],
            state=self.validated_data["state"],
            postal_code=self.validated_data["postal_code"],
            country=self.validated_data["country"]
        )
        profile.save()

        return user