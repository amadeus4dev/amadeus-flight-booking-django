from rest_framework import serializers
from .models import ChatHistory

class ChatHistorySerializer(serializers.ModelSerializer):
    class Meta:
        model = ChatHistory
        fields = ['question', 'answer', 'timestamp']
        read_only_fields = ['timestamp']
