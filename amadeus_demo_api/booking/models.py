from django.db import models
from users.models import User

class FlightSearchRecord(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    origin = models.CharField(max_length=3)
    destination = models.CharField(max_length=3)
    departure_date = models.DateField()
    adults = models.IntegerField()
    created_at = models.DateTimeField(auto_now_add=True)

class FlightOrder(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    flight_order_id = models.CharField(max_length=255, unique=True)
    status = models.CharField(max_length=50)  # 예: CONFIRMED, CANCELLED
    full_response = models.JSONField()
    created_at = models.DateTimeField(auto_now_add=True)
    create_payload = models.JSONField(null=True, blank=True)  # 내가 보낸 요청 payload 추가


class FlightCancelLog(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    flight_order = models.ForeignKey(FlightOrder, on_delete=models.CASCADE)
    cancel_request_payload = models.JSONField()
    cancel_response_payload = models.JSONField()
    created_at = models.DateTimeField(auto_now_add=True)

class FlightOrderRetrieveLog(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    flight_order = models.ForeignKey(FlightOrder, on_delete=models.CASCADE)
    retrieve_response_payload = models.JSONField()
    created_at = models.DateTimeField(auto_now_add=True)