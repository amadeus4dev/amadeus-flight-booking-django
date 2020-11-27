from django.urls import path

from . import views

urlpatterns = [
    path('', views.demo, name='home'),
    path('origin_airport_search/', views.origin_airport_search, name='origin_airport_search'),
    path('destination_airport_search/', views.destination_airport_search, name='destination_airport_search'),
    path('book_flight/<str:flight>/', views.book_flight, name='book_flight')
]
