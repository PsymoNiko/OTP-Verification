from random import randint
import redis

from rest_framework.response import Response
from rest_framework import status
from rest_framework.views import APIView
from rest_framework import viewsets, permissions, generics

from django.contrib.auth import authenticate
from django.shortcuts import get_object_or_404

from . import serializers
from .tasks import send_OTP

from .models import RegisterUser, UserPost
from . import authentication
from .permissions import IsOwnerOrReadOnly

from rest_framework_simplejwt.tokens import RefreshToken

from rest_framework.generics import CreateAPIView

from django.contrib.auth.models import User

redis_connection = redis.Redis(host="localhost", port=6379, db=0, decode_responses=True)


def random_code():
    otp_generator = str(randint(100000, 999999))
    return otp_generator


class User(APIView):
    serializer = serializers.GenerateOTPSerializer

    def post(self, request, *args, **kwargs):
        serializer = self.serializer(data=request.data)

        serializer.is_valid(raise_exception=True)
        phone_number = serializer.validated_data.get('phone_number')
        phone_number = serializer.phone_validation(phone_number)

        otp = random_code()
        redis_connection.set(phone_number, otp, ex=120)
        send_OTP.apply_async(args=[phone_number, otp])
        return Response({'Result': f'Your OTP code is {otp}'}, status=status.HTTP_200_OK)


class VerifyView(generics.CreateAPIView):
    serializer_class = serializers.OTPVerification
    permission_classes = (permissions.AllowAny,)

    def post(self, request, *args, **kwargs):

        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)
        otp_confirmation = serializer.validated_data.get("otp")
        otp_confirmation = serializer.verify_otp(otp=otp_confirmation)

        phone_number = serializer.validated_data["phone_number"]

        code = redis_connection.get(phone_number)

        try:
            if str(code) == str(otp_confirmation):

                phone_number = "+98" + phone_number[1:]

                user, created = RegisterUser.objects.get_or_create(phone_number=phone_number, username=phone_number)
                data = authentication.create_token(user)
                access_token = data['access_token']
                refresh_token = data['refresh_token']

                if created:
                    info = "Your verification is done"
                    message = "User created successfully"
                else:
                    info = "You have already registered"
                    message = "User already exists"

                response = Response({"info": info,
                                     "message": message,
                                     "access": str(access_token),
                                     "refresh": str(refresh_token)})
                response.set_cookie(key="access_token", value=access_token, httponly=True)
                return response
            else:
                return Response({"ERROR": "It's wrong"}, status=status.HTTP_406_NOT_ACCEPTABLE)
        finally:
            if str(code) == str(otp_confirmation):
                redis_connection.delete(phone_number)


class UserAuth(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def post(self, request, *args, **kwargs):
        return Response({'message': 'welcome to home.'}, status=status.HTTP_200_OK)


class UserCreateView(APIView):
    permission_classes = [IsOwnerOrReadOnly]

    def post(self, request, *args, **kwargs):
        serializer = serializers.UserPostSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        serializer.save(owner=request.user)
        return Response(serializer.data, status=status.HTTP_201_CREATED)



class UserGetView(APIView):
    permission_classes = [IsOwnerOrReadOnly]

    def get(self, request, *args, **kwargs):
        owner = UserPost.objects.all()
        serializer = serializers.UserPostSerializer(instance=owner, many=True)

        return Response(serializer.data, status=status.HTTP_200_OK)


class UserUpdateView(APIView):
    permission_classes = [permissions.IsAuthenticated, IsOwnerOrReadOnly]

    def put(self, request, slug, *args, **kwargs):
        owner = UserPost.objects.get(slug=slug)
        self.check_object_permissions(request, owner)

        serializer = serializers.UserPostSerializer(instance=owner, data=request.data, partial=True)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data, status=status.HTTP_200_OK)


class UserdeleteView(APIView):
    permission_classes = [permissions.IsAuthenticated, IsOwnerOrReadOnly]

    def delete(self, request, slug, *args, **kwargs):
        owner = get_object_or_404(UserPost, slug=slug)
        self.check_object_permissions(request, owner)
        owner.delete()
        return Response({'message': 'deleted'}, status=status.HTTP_204_NO_CONTENT)
