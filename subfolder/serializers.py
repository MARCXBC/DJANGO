from rest_framework import serializers
from .models import User

class UserSerializer(serializers.ModelSerializer):

    class Meta:
        model = User
        fields = "__all__"

    def validate(self, data):

        return data 

class RegisterSerializer(serializers.ModelSerializer):

    password = serializers.CharField(write_only=True)

    class Meta:
        model = User
        fields = [
            "first_name",
            "last_name",
            "password",
            "email"
        ]

    def create(self, validated_data):
        
        user = User.objects.create_user(
            first_name = validated_data["first_name"],
            last_name = validated_data["last_name"],
            email = validated_data["email"],
            password = validated_data["password"],
        )

        return user
    

class ChangePasswordSerializer(serializers.Serializer):

    old_password = serializers.CharField(required=True)

    new_password = serializers.CharField(required=True)