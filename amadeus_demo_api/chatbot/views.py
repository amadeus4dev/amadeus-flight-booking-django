from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from .models import ChatHistory
from .serializers import ChatHistorySerializer
from .models import ChatbotFlightActionLog

class ChatMessageView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        serializer = ChatHistorySerializer(data=request.data)
        if serializer.is_valid():
            ChatHistory.objects.create(
                user=request.user,
                **serializer.validated_data
            )
            return Response({"message": "Chat saved successfully."}, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)




class ChatbotResponseHandlerView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        chatbot_response = request.data  # 챗봇이 준 JSON

        action_type = chatbot_response.get("type")
        success = chatbot_response.get("success", False)

        # 공통 데이터 추출
        origin_code = chatbot_response.get("originLocationCode")
        destination_code = chatbot_response.get("destinationLocationCode")
        departure_date = chatbot_response.get("departureDate")
        adults = chatbot_response.get("adults")
        traveler_name = chatbot_response.get("name")
        date_of_birth = chatbot_response.get("dateOfBirth")
        gender = chatbot_response.get("gender")

        # 저장
        ChatbotFlightActionLog.objects.create(
            user=request.user,
            action_type=action_type,
            success=success,
            origin_location_code=origin_code,
            destination_location_code=destination_code,
            departure_date=departure_date,
            adults=adults,
            traveler_name=traveler_name,
            date_of_birth=date_of_birth,
            gender=gender,
            raw_chatbot_response=chatbot_response
        )

        return Response({"message": "Chatbot response saved."}, status=201)