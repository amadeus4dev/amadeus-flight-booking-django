from rest_framework import serializers
from .models import User, PassportInfo
from django.contrib.auth.hashers import make_password


class PassportInfoSerializer(serializers.ModelSerializer):
    class Meta:
        model = PassportInfo
        fields = [
            'number', 'name', 'gender', 'issuance_date', 'issuance_location',
            'expiry_date', 'nationality', 'birth_place', 'date_of_birth'
        ]


class RegisterSerializer(serializers.ModelSerializer):
    passport_info = PassportInfoSerializer(write_only=True)  #여권 정보 포함
    password = serializers.CharField(write_only=True)

    class Meta:
        model = User
        fields = [
            'username', 'password', 'first_name', 'last_name',
            'date_of_birth', 'email_address', 'gender',
            'passport_info'  # 필드에 추가
        ]

    def create(self, validated_data):
        passport_data = validated_data.pop('passport_info')  # 여권 데이터 분리
        password = validated_data.pop('password')

        user = User(**validated_data)
        user.set_password(password)  # 비밀번호 암호화
        user.save()

        PassportInfo.objects.create(user=user, **passport_data)  # 여권 정보 저장

        return user