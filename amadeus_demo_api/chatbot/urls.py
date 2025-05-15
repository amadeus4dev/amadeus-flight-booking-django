from django.urls import path
from .views import AskChatbotView, ChatHistoryView

urlpatterns = [
    path('chat/ask/', AskChatbotView.as_view(), name='send-message'),
    path('chat/history/', ChatHistoryView.as_view(), name='chat-history'),
]
