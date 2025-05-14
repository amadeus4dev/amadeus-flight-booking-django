from rest_framework import generics
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework import status
from django.views import View
from django.shortcuts import render
from rest_framework.views import APIView
from .models import User, PassportInfo
from .serializers import RegisterSerializer, PassportInfoSerializer
from rest_framework_simplejwt.views import TokenObtainPairView
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
import json
from django.contrib.auth import authenticate
from django.http import JsonResponse


class RegisterView(generics.CreateAPIView):
    queryset = User.objects.all()
    serializer_class = RegisterSerializer

class PassportInfoView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        serializer = PassportInfoSerializer(data=request.data)
        if serializer.is_valid():
            PassportInfo.objects.create(
                user=request.user,
                **serializer.validated_data
            )
            return Response({"message": "Passport information saved successfully."}, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class PassportInfoListView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        passports = PassportInfo.objects.filter(user=request.user)
        serializer = PassportInfoSerializer(passports, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)


class CustomTokenObtainPairSerializer(TokenObtainPairSerializer):
    @classmethod
    def get_token(cls, user):
        token = super().get_token(user)
        
        # 토큰에 추가 정보 담을 수 있어
        token['username'] = user.username
        token['email'] = user.email_address
        return token


class LoginAPI(APIView):
    def post(self, request):
        try:
            data = json.loads(request.body)
            username = data.get('username')
            password = data.get('password')
        except json.JSONDecodeError:
            return JsonResponse({'error': 'Invalid JSON'}, status=400)

        # 사용자 인증
        user_obj = authenticate(request, username=username, password=password)
        if user_obj is not None:
            # JWT 토큰 생성
            refresh = CustomTokenObtainPairSerializer.get_token(user_obj)
            access_token = str(refresh.access_token)

            return JsonResponse({'access': access_token}, status=200)
        else:
            print("user not match")
            print(username)
            print(password)
            return JsonResponse({'error': 'Invalid credentials'}, status=400)


class CustomTokenObtainPairView(TokenObtainPairView):
    serializer_class = CustomTokenObtainPairSerializer

# 프론트엔드 (로그인 화면 렌더링)
class LoginView(View):
    def get(self, request):
        return render(request, 'users/login.html')
    

class UserMeView(APIView):#유저 정보보
    permission_classes = [IsAuthenticated]

    def get(self, request):
        serializer = RegisterSerializer(request.user)
        return Response(serializer.data)