import json
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .amadeus import AmadeusService
from .models import FlightOrder,FlightCancelLog, FlightOrderRetrieveLog,FlightOfferCandidate, FlightSearchRecord
from users.models import PassportInfo
from users.models import User
from rest_framework.permissions import IsAuthenticated
import requests
from .amadeus import AMADEUS_API_BASE_URL
import urllib.parse

class FlightSearchView(APIView):
    permission_classes = [IsAuthenticated]
    def post(self, request):
        # Step 1: Flight Search 호출
        search_url = f"{AMADEUS_API_BASE_URL}/v2/shopping/flight-offers"

        search_payload = {
            "currencyCode": "USD",
            "originLocationCode": request.data.get("originLocationCode"),
            "destinationLocationCode": request.data.get("destinationLocationCode"),
            "departureDate": request.data.get("departureDate"),
            "adults": request.data.get("adults", 1)
        }

        search_response = requests.get(
            search_url,
            headers=AmadeusService.get_headers(),
            params=search_payload
        )

        if search_response.status_code != 200:
            AmadeusService.reset_token()
            return Response({"error": "Flight search failed."}, status=search_response.status_code)

        search_result = search_response.json()

        # Step 2: FlightOffers만 추출해서 Pricing용 Payload 변환
        try:
            top_5_offers = search_result.get("data", [])[:5]
            search_record = FlightSearchRecord.objects.create(
                user=request.user,
                origin=search_payload["originLocationCode"],
                destination=search_payload["destinationLocationCode"],
                departure_date=search_payload["departureDate"],
                adults=search_payload["adults"]
            )

            for offer in top_5_offers:
                segments = offer["itineraries"][0]["segments"]
                first_seg = segments[0]
                last_seg = segments[-1]
                FlightOfferCandidate.objects.create(
                    search=search_record,
                    offer_id=offer["id"],
                    offer_json=offer,#여기부터 요약 정보
                    airline=offer["validatingAirlineCodes"][0],
                    departure_airport=first_seg["departure"]["iataCode"],
                    arrival_airport=last_seg["arrival"]["iataCode"],
                    departure_time=first_seg["departure"]["at"],
                    arrival_time=last_seg["arrival"]["at"],
                    price=f'{offer["price"]["grandTotal"]} {offer["price"]["currency"]}',
                    number_of_stops=len(segments) - 1
                )
            pricing_payload = {
                "data": {
                    "type": "flight-offers-pricing",
                    "flightOffers": top_5_offers
                }
            }
            summery_payload = {
                    "search_id": search_record.id,
                    "flightOffers": [
                        {
                            "id": offer["id"],
                            "departure_airport": first_seg["departure"]["iataCode"],
                            "arrival_airport": last_seg["arrival"]["iataCode"],
                            "departure_time": first_seg["departure"]["at"],
                            "arrival_time": last_seg["arrival"]["at"],
                            "price": f'{offer["price"]["grandTotal"]} {offer["price"]["currency"]}',
                            "airline": offer["validatingAirlineCodes"][0],
                            "number_of_stops": len(segments) - 1
                        }
                        for offer in top_5_offers
                    ]
            }

        except KeyError:
            return Response({"error": "Search result missing flightOffers."}, status=400)

        #return Response(pricing_payload, status=200)
        return Response(summery_payload, status=200)
    
class FlightPriceView(APIView):
    def post(self, request):
        url = f"{AMADEUS_API_BASE_URL}/v1/shopping/flight-offers/pricing"

        payload = {
            "data": {
                "type": "flight-offers-pricing",
                "flightOffers": request.data.get("flightOffers")
            }
        }

        response = requests.post(url, headers=AmadeusService.get_headers(), json=payload)
        if response.status_code == 200:
            return Response(response.json(), status=200)
        else:
            AmadeusService.reset_token()
            return Response({"error": "Flight pricing failed."}, status=response.status_code)



class FlightCreateOrderView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        url = f"{AMADEUS_API_BASE_URL}/v1/booking/flight-orders"

        flight_offers = request.data.get("flightOffers")
        if not flight_offers:
            return Response({"error": "No flightOffers provided."}, status=400)

        # Step 1: PassportInfo 가져오기
        passports = PassportInfo.objects.filter(user=request.user)
        if not passports.exists():
            return Response({"error": "No passport information found."}, status=400)

        # Step 2: travelerPricings에서 필요한 travelerId 목록 추출
        traveler_pricings = flight_offers[0].get("travelerPricings", [])
        traveler_ids = [tp["travelerId"] for tp in traveler_pricings]

        if len(traveler_ids) > passports.count():
            return Response({"error": "Not enough passport information for travelers."}, status=400)

        # Step 3: travelerId 기준으로 travelers 매칭해서 생성
        travelers = []
        for traveler_id, passport in zip(traveler_ids, passports):
            traveler_type = self.get_traveler_type(passport.date_of_birth)
            traveler = {
                "id": str(traveler_id),
                "dateOfBirth": str(passport.date_of_birth),
                "name": {
                    "firstName": passport.name.split(' ')[0].upper(),
                    "lastName": passport.name.split(' ')[-1].upper()
                },
                "gender": passport.gender.upper(),
                "contact": {
                    "emailAddress": request.user.email,
                },
                "documents": [
                    {
                        "documentType": "PASSPORT",
                        "number": passport.number,
                        "issuanceDate": str(passport.issuance_date),
                        "expiryDate": str(passport.expiry_date),
                        "issuanceCountry": passport.nationality,
                        "nationality": passport.nationality,
                        "birthPlace": passport.birth_place,
                        "holder": True
                    }
                ],
                "travelerType": traveler_type
            }
            travelers.append(traveler)

        # Step 4: contacts 자동 생성
        contacts = [
            {
                "addresseeName": {
                    "firstName": request.user.first_name.upper() if request.user.first_name else "USER",
                    "lastName": request.user.last_name.upper() if request.user.last_name else "USER"
                },
                "companyName": "REAL PROJECT",
                "purpose": "STANDARD",
                "emailAddress": request.user.email,
                "phones": [
                    {
                        "deviceType": "MOBILE",
                        "countryCallingCode": "82",
                        "number": "1012345678"
                    }
                ],
                "address": {
                    "lines": ["Seoul Example Street 1"],
                    "postalCode": "04524",
                    "cityName": "Seoul",
                    "countryCode": "KR"
                }
            }
        ]

        # Step 5: payload 조립
        payload = {
            "data": {
                "type": "flight-order",
                "flightOffers": flight_offers,
                "travelers": travelers,
                "contacts": contacts
            }
        }

        # Step 6: 예약 요청 보내기
        response = requests.post(url, headers=AmadeusService.get_headers(), json=payload)
        if response.status_code == 201:
            data = response.json()
            flight_order_id = urllib.parse.unquote(data['data']['id'])#디코딩 %d같은거
            #flight_order_id = data['data']['id']
            FlightOrder.objects.create(
                user=request.user,
                flight_order_id=flight_order_id,
                status='CONFIRMED',
                full_response=data,
                create_payload=payload
            )
            return Response(data, status=201)
        else:
            try:
                error_detail = response.json()
            except Exception:
                error_detail = {"error": "No detail available", "status_code": response.status_code}
            
            AmadeusService.reset_token()
            return Response({
                "error": "Flight booking failed.",
                "detail": error_detail,    #에러 상세 반환
                "payload": payload         # payload도 같이 반환
            }, status=response.status_code)
        
    @staticmethod
    def get_traveler_type(date_of_birth):
        from datetime import date

        today = date.today()
        age = today.year - date_of_birth.year - ((today.month, today.day) < (date_of_birth.month, date_of_birth.day))

        if age >= 12:
            return "ADULT"
        else:
            return "CHILD"

class FlightCreateOrderByIndexView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        number = request.data.get("number")  # 챗봇이 보내는 항공편 선택 번호

        if not number:
            return Response({"error": "number 필드가 필요합니다."}, status=400)

        try:
            # 최신 검색 기준으로 최대 5개 중 선택
            offers = FlightOfferCandidate.objects.filter(
                search__user=request.user
            ).order_by("-search__created_at", "created_at")[:5]

            selected_offer = offers[int(number) - 1]
            flight_offer = selected_offer.offer_json
        except (IndexError, ValueError):
            return Response({"error": f"{number}번 항공편을 찾을 수 없습니다."}, status=404)

        # 기존 예약 로직 재활용
        return FlightCreateOrderView.create_with_offer(request, flight_offer)


class FlightOrderRetrieveView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request, flight_order_id):
        url = f"{AMADEUS_API_BASE_URL}/v1/booking/flight-orders/{flight_order_id}"

        response = requests.get(url, headers=AmadeusService.get_headers())
        response_data = response.json()

        if response.status_code != 200:
            AmadeusService.reset_token()
            return Response({"error": "Flight order retrieval failed."}, status=response.status_code)

        # Step 1: errors 필드 체크
        if "errors" in response_data:
            return Response({
                "status": "failed",
                "errors": response_data["errors"]
            }, status=400)

        # Step 2: warnings 필드 체크
        warning_messages = []
        if "warnings" in response_data:
            for warning in response_data["warnings"]:
                warning_messages.append({
                    "title": warning.get("title"),
                    "detail": warning.get("detail"),
                    "relatedSegments": warning.get("source", {}).get("pointer")
                })
        flight_order = FlightOrder.objects.get(flight_order_id=flight_order_id, user=request.user)
        FlightOrderRetrieveLog.objects.create(
                user=request.user,
                flight_order=flight_order,
                retrieve_response_payload=response_data
            )
        # Step 3: 정상 데이터 반환 + warning 추가
        return Response({
            "status": "success",
            "warnings": warning_messages,
            "orderData": response_data.get("data", {})
        }, status=200)
        
class FlightOrderCancelView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request, flight_order_id):
        url = f"{AMADEUS_API_BASE_URL}/v1/booking/flight-orders/{flight_order_id}"

        response = requests.delete(url, headers=AmadeusService.get_headers())
        if response.status_code == 204:
            # 취소 성공했으면 DB 상태도 변경
            try:
                order = FlightOrder.objects.get(user=request.user, flight_order_id=flight_order_id)
                order.status = 'CANCELLED'
                order.save()
            except FlightOrder.DoesNotExist:
                pass
            FlightCancelLog.objects.create(
                user=request.user,
                flight_order=order,
                cancel_request_payload={"method": "DELETE", "url": url},
                cancel_response_payload={"status_code": 204, "message": "Cancelled"}
            )
            return Response({"message": "Flight order cancelled successfully."}, status=204)
        else:
            AmadeusService.reset_token()
            return Response({"error": "Flight order cancellation failed."}, status=response.status_code)
