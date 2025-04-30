from rest_framework import serializers
from .models import User
from .models import PassportInfo
from django.contrib.auth.hashers import make_password

class RegisterSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['username', 'password', 'first_name', 'last_name', 'date_of_birth', 'email_address', 'gender']
        extra_kwargs = {
            'password': {'write_only': True}
        }

    def create(self, validated_data):
        validated_data['password'] = make_password(validated_data['password'])  # 비밀번호 암호화
        return super().create(validated_data)

class PassportInfoSerializer(serializers.ModelSerializer):
    class Meta:
        model = PassportInfo
        fields = [
            'number', 'name', 'gender', 'issuance_date', 'issuance_location',
            'expiry_date', 'nationality', 'birth_place', 'date_of_birth'
        ]