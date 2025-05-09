from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),
    path('chat/', include('chat.urls')),
    path('login/', include('users.urls_front')),
    
    path('', include('demo.urls')),
    path('api/', include('users.urls')),
    path('api/', include('chatbot.urls')),
    path('api/', include('booking.urls')),
]
