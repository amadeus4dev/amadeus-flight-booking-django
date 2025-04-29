from rest_framework import generics
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework import status
from rest_framework.views import APIView
from .models import User, PassportInfo
from .serializers import RegisterSerializer, PassportInfoSerializer
from rest_framework_simplejwt.views import TokenObtainPairView
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer


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

from rest_framework_simplejwt.views import TokenObtainPairView
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer

class CustomTokenObtainPairSerializer(TokenObtainPairSerializer):
    @classmethod
    def get_token(cls, user):
        token = super().get_token(user)
        
        # 토큰에 추가 정보 담을 수 있어
        token['username'] = user.username
        token['email'] = user.email_address
        return token

class CustomTokenObtainPairView(TokenObtainPairView):
    serializer_class = CustomTokenObtainPairSerializer
