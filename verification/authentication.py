from django.contrib.auth import authenticate
from rest_framework import serializers
from rest_framework.authentication import BaseAuthentication
from rest_framework import exceptions

from django.contrib.auth import get_user_model

from rest_framework_simplejwt.tokens import RefreshToken


class LoginSerializer(serializers.Serializer):
    phone_number = serializers.CharField()

    def validate(self, data):
        user = authenticate(**data)
        if user and user.is_active:
            return user
        raise serializers.ValidationError("Incorrect credentials")


def create_token(user):
    refresh_token = RefreshToken().for_user(user)
    access_token = refresh_token.access_token
    data = {'access_token': access_token,
            'refresh_token': refresh_token}

    return data


class CustomTokenAuthentication(BaseAuthentication):
    def authenticate(self, request):
        UserModel = get_user_model()
        token = request.headers.get('Authorization')
        if not token:
            return None

        try:
            user = UserModel.objects.get(token=token)
        except UserModel.DoesNotExist:
            raise exceptions.AuthenticationFailed('Invalid token')

        return (user, None)
