from django.urls import path
from .dispatch import AmadeusIntentDispatcherView
from .views import (
    FlightSearchView, FlightPriceView, FlightCreateOrderView,
    FlightOrderRetrieveView, FlightOrderCancelView,FlightCreateOrderByIndexView
)

urlpatterns = [
    path('booking/search/', FlightSearchView.as_view(), name='flight-search'),
    path('booking/price/', FlightPriceView.as_view(), name='flight-price'),
    path('booking/create/', FlightCreateOrderView.as_view(), name='flight-create-order'),
    path('booking/orders/<str:flight_order_id>/', FlightOrderRetrieveView.as_view(), name='flight-order-retrieve'),
    path('booking/orders/<str:flight_order_id>/cancel/', FlightOrderCancelView.as_view(), name='flight-order-cancel'),
    path('amadeus/handle/', AmadeusIntentDispatcherView.as_view(), name='amadeus-intent-dispatcher'), 
    path('booking/by-number/',FlightCreateOrderByIndexView.as_view(),name='flight-order-number'),#실제 백에서 예약호출 함수수
    
    # AI 서버 응답 처리
]
