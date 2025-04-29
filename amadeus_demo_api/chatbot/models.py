from django.db import models
from users.models import User

class ChatHistory(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    question = models.TextField()
    answer = models.TextField()
    timestamp = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return f"{self.user.username} - {self.timestamp}"
    

from django.db import models
from users.models import User

class ChatbotFlightActionLog(models.Model):
    ACTION_TYPES = [
        ('search', 'Search'),
        ('booking', 'Booking'),
        ('cancel', 'Cancel'),
    ]

    user = models.ForeignKey(User, on_delete=models.CASCADE)  # 누가 요청했는지
    action_type = models.CharField(max_length=10, choices=ACTION_TYPES)  # search, booking, cancel
    success = models.BooleanField(default=False)  # 필요한 정보 다 갖췄는지
    origin_location_code = models.CharField(max_length=10, null=True, blank=True)
    destination_location_code = models.CharField(max_length=10, null=True, blank=True)
    departure_date = models.DateField(null=True, blank=True)
    adults = models.IntegerField(null=True, blank=True)
    traveler_name = models.JSONField(null=True, blank=True)  # {"firstName": "JORGE", "lastName": "GONZALES"}
    date_of_birth = models.DateField(null=True, blank=True)
    gender = models.CharField(max_length=10, null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)  # 요청 시각
    raw_chatbot_response = models.JSONField()  # 챗봇이 준 원본 JSON 전체 저장