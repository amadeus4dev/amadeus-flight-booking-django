from django.shortcuts import render

# Create your views here.
def start_chat(request):
    return render(request, "chat/chat.html")