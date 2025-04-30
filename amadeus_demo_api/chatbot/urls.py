from django.urls import path
from .views import ChatMessageView

urlpatterns = [
    path('chat/send_message/', ChatMessageView.as_view(), name='send-message'),
]
