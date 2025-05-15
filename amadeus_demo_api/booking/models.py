from django.db import models
from users.models import User

class FlightSearchRecord(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    origin = models.CharField(max_length=3)
    destination = models.CharField(max_length=3)
    departure_date = models.DateField()
    adults = models.IntegerField()
    created_at = models.DateTimeField(auto_now_add=True)


class FlightOfferCandidate(models.Model):
    search = models.ForeignKey(FlightSearchRecord, on_delete=models.CASCADE, related_name='offers')
    offer_id = models.CharField(max_length=50)  # Amadeus flight offer ID
    offer_json = models.JSONField()             # Amadeus 응답 전체 저장
    #요약 저장
    airline = models.CharField(max_length=10)        # validatingAirlineCodes[0]
    departure_airport = models.CharField(max_length=3)
    arrival_airport = models.CharField(max_length=3)
    departure_time = models.DateTimeField()
    arrival_time = models.DateTimeField()
    price = models.CharField(max_length=20)          # 예: "1204.51 USD"
    number_of_stops = models.IntegerField()

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

