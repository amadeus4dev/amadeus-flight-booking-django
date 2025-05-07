from django.urls import path
from .views import GetJWTTokenView

urlpatterns = [
    path('', GetJWTTokenView.as_view(), name='get-jwt-token'),
]
