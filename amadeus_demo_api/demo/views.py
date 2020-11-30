import json
import ast
from amadeus import Client, ResponseError, Location
from django.shortcuts import render
from django.contrib import messages
from .flight import Flight
from .booking import Booking
from django.http import HttpResponse

amadeus = Client()


def demo(request):
    # Retrieve data from the UI form
    origin = request.POST.get("Origin")
    destination = request.POST.get("Destination")
    departureDate = request.POST.get("Departuredate")
    returnDate = request.POST.get("Returndate")

    # Prepare url parameters for search
    kwargs = {
        "originLocationCode": request.POST.get("Origin"),
        "destinationLocationCode": request.POST.get("Destination"),
        "departureDate": request.POST.get("Departuredate"),
        "adults": 1,
    }

    # For a round trip, we use AI Trip Purpose Prediction
    #  to predict if it is a leisure or business trip
    tripPurpose = ""
    if returnDate:
        kwargs["returnDate"] = returnDate
        try:
            trip_purpose_response = amadeus.travel.predictions.trip_purpose.get(
                originLocationCode=origin,
                destinationLocationCode=destination,
                departureDate=departureDate,
                returnDate=returnDate,
            ).data
            tripPurpose = trip_purpose_response["result"]
        except ResponseError as error:
            messages.add_message(request, messages.ERROR, error)
            return render(request, "demo/demo_form.html", {})

    # Perform flight search based on previous inputs
    if origin and destination and departureDate:
        try:
            search_flights = amadeus.shopping.flight_offers_search.get(**kwargs)
        except ResponseError as error:
            messages.add_message(request, messages.ERROR, error)
            return render(request, "demo/demo_form.html", {})
        search_flights_returned = []
        for flight in search_flights.data:
            offer = Flight(flight).construct_flights()
            search_flights_returned.append(offer)
            response = zip(search_flights_returned, search_flights.data)

        return render(
            request,
            "demo/results.html",
            {
                "response": response,
                "origin": origin,
                "destination": destination,
                "departureDate": departureDate,
                "returnDate": returnDate,
                "tripPurpose": tripPurpose,
            },
        )
    return render(request, "demo/demo_form.html", {})


# Auto-complete using Airport & City Search API for origin
def origin_airport_search(request):
    if request.is_ajax():
        try:
            data = amadeus.reference_data.locations.get(
                keyword=request.GET.get("term", None), subType=Location.ANY
            ).data
        except ResponseError as error:
            messages.add_message(request, messages.ERROR, error)
    return HttpResponse(get_city_airport_list(data), "application/json")


# Auto-complete using Airport & City Search API for destination
def destination_airport_search(request):
    if request.is_ajax():
        try:
            data = amadeus.reference_data.locations.get(
                keyword=request.GET.get("term", None), subType=Location.ANY
            ).data
        except ResponseError as error:
            messages.add_message(request, messages.ERROR, error)
    return HttpResponse(get_city_airport_list(data), "application/json")


def get_city_airport_list(data):
    result = []
    for i, val in enumerate(data):
        result.append(data[i]["iataCode"] + ", " + data[i]["name"])
    result = list(dict.fromkeys(result))

    return json.dumps(result)


# Perform Flight Price and Booking
def book_flight(request, flight):
    # Create a fake traveler profile for booking
    traveler = {
        "id": "1",
        "dateOfBirth": "1982-01-16",
        "name": {"firstName": "JORGE", "lastName": "GONZALES"},
        "gender": "MALE",
        "contact": {
            "emailAddress": "jorge.gonzales833@telefonica.es",
            "phones": [
                {
                    "deviceType": "MOBILE",
                    "countryCallingCode": "34",
                    "number": "480080076",
                }
            ],
        },
        "documents": [
            {
                "documentType": "PASSPORT",
                "birthPlace": "Madrid",
                "issuanceLocation": "Madrid",
                "issuanceDate": "2015-04-14",
                "number": "00000000",
                "expiryDate": "2025-04-14",
                "issuanceCountry": "ES",
                "validityCountry": "ES",
                "nationality": "ES",
                "holder": True,
            }
        ],
    }
    # Use Flight Offers Price to confirm price and availability
    try:
        flight_price_confirmed = amadeus.shopping.flight_offers.pricing.post(
            ast.literal_eval(flight)
        ).data["flightOffers"]
    except ResponseError as error:
        messages.add_message(request, messages.ERROR, error.response.body)
        return render(request, "demo/book_flight.html", {})

    # Use Flight Create Orders to perform the booking
    try:
        order = amadeus.booking.flight_orders.post(
            flight_price_confirmed, traveler
        ).data
    except ResponseError as error:
        messages.add_message(request, messages.ERROR, error.response.body)
        return render(request, "demo/book_flight.html", {})

    passenger_name_record = []
    booking = Booking(order).construct_booking()
    passenger_name_record.append(booking)

    return render(request, "demo/book_flight.html", {"response": passenger_name_record})
