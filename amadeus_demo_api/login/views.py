from django.contrib.auth import authenticate
from django.shortcuts import render
from django.views import View
from users.services import get_jwt_for_user

from rest_framework_simplejwt.tokens import RefreshToken

class GetJWTTokenView(View):
    def get(self, request):
        username = 'test'
        password = '1234'

        user = authenticate(username=username, password=password)
        if user is not None:
            token_data = get_jwt_for_user(user)
            print(token_data)
            token = token_data.get('access', '토큰 없음')
            request.session['jwt_token'] = token #세션 저장
        else:
            token = '로그인 실패'

        return render(request, 'login/tmp.html', {'token': token})