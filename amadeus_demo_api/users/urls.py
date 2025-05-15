from django.urls import path
from .views import *

urlpatterns = [
    path('register/', RegisterView.as_view(), name='register'),#회원가입 + 여권정보 동시에에
    path('passport/add/', PassportInfoView.as_view(), name='passport_info'),#여권 등록록
    #path('passport/add/', PassportInfoview.as_view(), name='passport_add'),#여권 정보 수정
    path('passport/list/', PassportInfoListView.as_view(), name='passport-list'),#여권 정보 확인
    path('login/', LoginAPI.as_view(), name='token_obtain_pair'),#로그인인
    path('me/',UserMeView.as_view(), name='user_me'),#내 정보 확인
]