from rest_framework import serializers
from rest_framework_jwt.settings import api_settings
from django.contrib.auth.backends import ModelBackend
from django.contrib.auth import authenticate
from django.contrib.auth.models import update_last_login
from django.contrib.auth import get_user_model
from .models import *

# JWT 사용을 위한 설정
JWT_PAYLOAD_HANDLER = api_settings.JWT_PAYLOAD_HANDLER
JWT_ENCODE_HANDLER = api_settings.JWT_ENCODE_HANDLER

User = get_user_model()

# 회원가입.
class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['userid', 'email', 'password']

    def create(self, validated_data):
        user = User.objects.create(
            email=validated_data['email'],
            userid=validated_data['userid'],
            password=validated_data['password'],
        )
        #user.set_password(validated_data['password'])
        user.save()
        return user


class LoginBackend(ModelBackend): # 준환님 readme.md 참고. 이거 안하면 계속 userid=None 나옴..
    def authenticate(self, request, userid=None, password=None, **kwargs):
        try:
            user = User.objects.get(userid=userid)
            #if user.check_password(password):
            if user.password == password:
                return user
            return None

        except User.DoesNotExist:
            return None


# 로그인
class UserLoginSerializer(serializers.ModelSerializer):
    userid = serializers.CharField(max_length=50)
    password = serializers.CharField(max_length=150, write_only=True)
    token = serializers.CharField(max_length=255, read_only=True)

    class Meta:
        model = User
        fields = ['userid', 'password', 'token']

    def validate(self, data):
        userid = data.get("userid", None)
        password = data.get("password", None)
        user = authenticate(userid=userid, password=password)

        if user is None:
            return {'userid': 'None'} # password가 안맞아도 해당 에러.
        try:
            payload = JWT_PAYLOAD_HANDLER(user)
            jwt_token = JWT_ENCODE_HANDLER(payload)
            update_last_login(None, user)

        except User.DoesNotExist:
            raise serializers.ValidationError(
                'User does not exist'
            )
        return {
            'userid': user.userid,
            'token': jwt_token
        }


class CandidateSerializer(serializers.ModelSerializer):
    voters = UserSerializer(many=True, read_only=True)
    class Meta:
        model = Candidate
        fields = ['name', 'votes', 'voters']



