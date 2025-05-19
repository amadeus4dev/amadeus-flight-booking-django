import requests
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from rest_framework.permissions import AllowAny
from rest_framework_simplejwt.authentication import JWTAuthentication
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_exempt
from .models import ChatHistory
from .serializers import ChatHistorySerializer
from .models import ChatbotFlightActionLog
from booking.dispatch import *
from django.test.client import RequestFactory
class ChatHistoryView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        chat_records = ChatHistory.objects.filter(user=request.user).order_by('timestamp')
        chat_history_list = []

        for record in chat_records:
            chat_history_list.append(record.question)
            chat_history_list.append(record.answer)
        #serializer = ChatHistorySerializer(chat_records, many=True)
        return Response({"chat_history": chat_history_list}, status=status.HTTP_200_OK)
@method_decorator(csrf_exempt, name='dispatch')    
class AskChatbotView(APIView):
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]

    def post(self, request):
        print("request.user:", request.user)
        print("auth:", request.auth)
        print("Authorization header:", request.META.get('HTTP_AUTHORIZATION'))
        question = request.data.get('question')
        if not question:
            return Response({"error": "질문이 필요합니다."}, status=400)

        user = request.user
        chat_records = ChatHistory.objects.filter(user=user).order_by('timestamp')
        chat_history_list = [q for record in chat_records for q in (record.question, record.answer)]
        chat_history_list.append(question)

        payload = {
            "chat_history": chat_history_list
        }
        print("checkmsgg")
        try:
            ai_response = requests.post(
                "http://172.31.25.19:8080/question",
                json=payload,
                timeout=5
            )
            ai_data = ai_response.json()
        except Exception as e:
            return Response({"error": "AI 서버 연결 실패", "detail": str(e)}, status=500)

        # 질문 기록 먼저 저장
        ChatHistory.objects.create(user=user, question=question, answer=str(ai_data))

        # dispatcher로 넘기기
        # request.data를 ai_data로 덮기 위해 새 요청 생성
        factory = RequestFactory()
        new_request = factory.post(
            "/booking/dispatch/",  # (뷰 내부에서만 씀)
            data=ai_data,
            content_type='application/json'
        )
        new_request.user = request.user

        # as_view()는 Django의 CBV 디스패처
        return AmadeusIntentDispatcherView.as_view()(new_request)

# class ChatMessageView(APIView):
#     permission_classes = [IsAuthenticated]

#     def post(self, request):
#         serializer = ChatHistorySerializer(data=request.data)
#         if serializer.is_valid():
#             ChatHistory.objects.create(
#                 user=request.user,
#                 **serializer.validated_data
#             )
#             return Response({"message": "Chat saved successfully."}, status=status.HTTP_201_CREATED)
#         return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)




# class ChatbotResponseHandlerView(APIView):
#     permission_classes = [IsAuthenticated]

#     def post(self, request):
#         chatbot_response = request.data  # 챗봇이 준 JSON

#         action_type = chatbot_response.get("type")
#         success = chatbot_response.get("success", False)

#         # 공통 데이터 추출
#         origin_code = chatbot_response.get("originLocationCode")
#         destination_code = chatbot_response.get("destinationLocationCode")
#         departure_date = chatbot_response.get("departureDate")
#         adults = chatbot_response.get("adults")
#         traveler_name = chatbot_response.get("name")
#         date_of_birth = chatbot_response.get("dateOfBirth")
#         gender = chatbot_response.get("gender")

#         # 저장
#         ChatbotFlightActionLog.objects.create(
#             user=request.user,
#             action_type=action_type,
#             success=success,
#             origin_location_code=origin_code,
#             destination_location_code=destination_code,
#             departure_date=departure_date,
#             adults=adults,
#             traveler_name=traveler_name,
#             date_of_birth=date_of_birth,
#             gender=gender,
#             raw_chatbot_response=chatbot_response
#         )

#         return Response({"message": "Chatbot response saved."}, status=201)
