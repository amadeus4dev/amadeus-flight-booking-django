from django.urls import path
from .views import (
    FlightSearchView, FlightPriceView, FlightCreateOrderView,
    FlightOrderRetrieveView, FlightOrderCancelView
)

urlpatterns = [
    path('booking/search/', FlightSearchView.as_view(), name='flight-search'),
    path('booking/price/', FlightPriceView.as_view(), name='flight-price'),
    path('booking/create/', FlightCreateOrderView.as_view(), name='flight-create-order'),
    path('booking/orders/<str:flight_order_id>/', FlightOrderRetrieveView.as_view(), name='flight-order-retrieve'),
    path('booking/orders/<str:flight_order_id>/cancel/', FlightOrderCancelView.as_view(), name='flight-order-cancel'),
]
