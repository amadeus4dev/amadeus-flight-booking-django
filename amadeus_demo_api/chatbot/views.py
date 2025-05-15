import requests
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from .models import ChatHistory
from .serializers import ChatHistorySerializer
from .models import ChatbotFlightActionLog

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
    
class AskChatbotView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        question = request.data.get('question')
        if not question:
            return Response({"error": "질문이 필요합니다."}, status=400)

        user = request.user

        chat_records = ChatHistory.objects.filter(user=request.user).order_by('timestamp')
        chat_history_list = []

        for record in chat_records:
            chat_history_list.append(record.question)
            chat_history_list.append(record.answer)
        # 기존 대화 기록 가져오기
        # chat_records = ChatHistory.objects.filter(user=user).order_by('timestamp')
        # chat_history_data = [{"question": r.question, "answer": r.answer} for r in chat_records]

        # 마지막 질문 추가
        chat_history_list.append(question)

        # AI 서버로 전달할 payload
        payload = {
            #"user_id": user.id,
            "chat_history": chat_history_list
        }
        return Response(payload, status=200)
        # AI 서버에 POST 요청 보내기
        try:
            ai_response = requests.post(
                "http://",
                json=payload,
                timeout=5
            )
            ai_data = ai_response.json()
        except Exception as e:
            return Response({"error": "AI 서버 연결 실패", "detail": str(e)}, status=500)

        # 응답 저장
        answer = ai_data.get("answer", "죄송합니다. 답변을 찾지 못했습니다.")
        ChatHistory.objects.create(user=user, question=question, answer=answer)

        # 사용자에게 응답 반환
        return Response({
            "question": question,
            "answer": answer
        })



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