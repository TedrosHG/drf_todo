from rest_framework import serializers
from authentication.models import User


class RegisterSerializer(serializers.ModelSerializer):
    password = serializers.CharField(
        write_only = True, max_length = 128, min_length = 8
    )

    class Meta:
        model = User
        fields = ['username', 'email', 'password']

    def create(self, validated_data):
        return User.objects.create_user(**validated_data)

class LoginSerializer(serializers.ModelSerializer):
    password = serializers.CharField(
        write_only = True, max_length = 128, min_length = 8
    )

    class Meta:
        model = User
        fields = ['email', 'password', 'token']
        read_only_field = ['token']

