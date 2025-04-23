from django.urls import path

from . import views

app_name = 'chat'

urlpatterns = [
    path('', views.start_chat, name='chatting_home')
]
