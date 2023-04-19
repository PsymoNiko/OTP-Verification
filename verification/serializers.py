from rest_framework import serializers

from .models import UserPost


class GenerateOTPSerializer(serializers.Serializer):
    phone_number = serializers.CharField(max_length=13, min_length=11, required=True)

    def phone_validation(self, phone_number: str) -> str:

        if phone_number[0] == '0' and phone_number[1] == '9' and \
                str(phone_number).isnumeric() == True:
            return phone_number
        elif str(phone_number).startswith("+98") and str(phone_number[1:]).isnumeric() == True:
            return phone_number
        else:
            raise serializers.ValidationError('your phone-number contains 11 digits and starts with ZERO and 9'
                                              'or starts with +98 and contains 13 digits')


class OTPVerification(GenerateOTPSerializer):
    otp = serializers.CharField(max_length=6)

    def verify_otp(self, otp: str) -> str:
        if str(otp).isnumeric() is True and len(otp) == 6:
            return otp
        else:
            return ValueError('Your OTP code is wrong')


class UserPostSerializer(serializers.ModelSerializer):
    title = serializers.CharField(max_length=225)
    text = serializers.CharField(max_length=250)
    owner_name = serializers.SerializerMethodField()

    class Meta:
        model = UserPost
        # fields = '__all__'
        fields = ['title', 'text', 'owner', 'owner_name', 'created_at', 'modified_at', 'is_deleted', 'slug']
        read_only_fields = ['owner', 'slug', 'created_at', 'modified_at', 'owner_name']

    def get_owner_name(self, obj):
        return obj.owner.username

    """ this is for when have slug repetitious"""

    def create(self, validated_data):
        if UserPost.objects.filter(title=validated_data['title']).exists():
            raise serializers.ValidationError("This title was existed")
        return UserPost.objects.create(**validated_data)
