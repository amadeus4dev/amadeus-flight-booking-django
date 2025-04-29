from django.urls import path
from .views import RegisterView,PassportInfoView, PassportInfoListView, CustomTokenObtainPairView

urlpatterns = [
    path('register/', RegisterView.as_view(), name='register'),
    path('passport/', PassportInfoView.as_view(), name='passport_info'),
    path('passport/list/', PassportInfoListView.as_view(), name='passport-list'),
    path('login/', CustomTokenObtainPairView.as_view(), name='token_obtain_pair'),
]