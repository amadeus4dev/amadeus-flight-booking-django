import json
import ast
import os
import requests
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
    departure_date = request.POST.get("Departuredate")
    return_date = request.POST.get("Returndate")

    # Prepare url parameters for search
    kwargs = {
        "originLocationCode": origin,
        "destinationLocationCode": destination,
        "departureDate": departure_date,
        "adults": 1,
    }

    # For a round trip, we use AI Trip Purpose Prediction
    # to predict if it is a leisure or business trip
    tripPurpose = ""
    if return_date:
        # Adds the parameter returnDate for the Flight Offers Search API call
        kwargs["returnDate"] = return_date
        kwargs_trip_purpose = {
            "originLocationCode": origin,
            "destinationLocationCode": destination,
            "departureDate": departure_date,
            "returnDate": return_date,
            "max": 1
        }
        try:
            # Calls Trip Purpose Prediction API
            trip_purpose_response = amadeus.travel.predictions.trip_purpose.get(
                **kwargs_trip_purpose
            ).data
            tripPurpose = trip_purpose_response["result"]
        except ResponseError as error:
            messages.add_message(
                request, messages.ERROR, error.response.result["errors"][0]["detail"]
            )
            return render(request, "demo/home.html", {})

    # Perform flight search based on previous inputs
    if origin and destination and departure_date:
        try:
            search_flights = amadeus.shopping.flight_offers_search.get(**kwargs)
        except ResponseError as error:
            messages.add_message(
                request, messages.ERROR, error.response.result["errors"][0]["detail"]
            )
            return render(request, "demo/home.html", {})
        try:
            if os.environ.get('RISKLINE_ACCESS_TOKEN'): 
                trip_assessment = ''
                possible_travel_disruptions = ''
                annual_events = ''
                visa_rules = ''
                vaccinations = ''
                insurance_documents = ''
                

                destination_country = search_flights.result['dictionaries'].get('locations').get(destination).get('countryCode')
                orgin_country = search_flights.result['dictionaries'].get('locations').get(origin).get('countryCode')
                url = "https://api.riskline.com/ext/v1/travel-search"

                payload = json.dumps({
                "nationality": orgin_country,
                "origin": orgin_country,
                "destination": destination_country,
                "dates": {
                    "from": departure_date,
                    "to": return_date
                }
                })
                headers = {
                    'Authorization': 'Bearer ' + os.environ.get('RISKLINE_ACCESS_TOKEN'),
                    'Content-Type': 'application/json'
                }

                response = requests.request("POST", url, headers=headers, data=payload)
                print(response.json)
                trip_assessment = response.json()['overall_trip_assessment']['answer']
                possible_travel_disruptions = response.json()['possible_travel_disruptions']['advisories'][0]['title']
                if 'annual_events' in response.json()['possible_travel_disruptions']:
                    annual_events_list = response.json()['possible_travel_disruptions']['annual_events']
                    if annual_events_list:
                        if 'date' in annual_events_list[0]:
                            annual_events = annual_events_list[0]['date'] + ', ' + annual_events_list[0]['name']
                if 'documents_required' in response.json() and 'entry' in response.json()['documents_required']:
                    entry_info = response.json()['documents_required']['entry']
                    if 'visa_rules' in entry_info:
                            visa_rules_list = entry_info['visa_rules']
                            if visa_rules_list:
                                visa_rules = visa_rules_list[0]['text']
                    if 'vaccinations' in entry_info:
                        vaccinations_list = entry_info['vaccinations']
                        if vaccinations_list:
                            vaccinations = vaccinations_list[0]['name'] + ' ' + vaccinations_list[0]['description']
                    if 'insurance_documents' in entry_info:
                            insurance_documents_list = entry_info['insurance_documents']
                            if insurance_documents_list:
                                insurance_documents = insurance_documents_list[0]['text']

        except (ResponseError, KeyError, AttributeError) as error:
            messages.add_message(
                request, messages.ERROR, 'No results found'
            )
            return render(request, "demo/home.html", {})
        search_flights_returned = []
        response = ""
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
                "departureDate": departure_date,
                "returnDate": return_date,
                "tripPurpose": tripPurpose,
                "destination_country": destination_country,
                "trip_assessment": trip_assessment,
                "possible_travel_disruptions": possible_travel_disruptions,
                "annual_events": annual_events,
                "visa_rules": visa_rules,
                "insurance_documents": insurance_documents,
                "vaccinations": vaccinations
            },
        )
    return render(request, "demo/home.html", {})


def book_flight(request, flight):
    # Create a dummy traveler profile for booking
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
    except (ResponseError, KeyError, AttributeError) as error:
        messages.add_message(request, messages.ERROR, error.response.body)
        return render(request, "demo/book_flight.html", {})

    # Use Flight Create Orders to perform the booking
    try:
        order = amadeus.booking.flight_orders.post(
            flight_price_confirmed, traveler
        ).data
    except (ResponseError, KeyError, AttributeError) as error:
        messages.add_message(
            request, messages.ERROR, error.response.result["errors"][0]["detail"]
        )
        return render(request, "demo/book_flight.html", {})

    passenger_name_record = []
    booking = Booking(order).construct_booking()
    passenger_name_record.append(booking)

    return render(request, "demo/book_flight.html", {"response": passenger_name_record})


def origin_airport_search(request):
    if request.is_ajax():
        try:
            data = amadeus.reference_data.locations.get(
                keyword=request.GET.get("term", None), subType=Location.ANY
            ).data
        except (ResponseError, KeyError, AttributeError) as error:
            messages.add_message(
                request, messages.ERROR, error.response.result["errors"][0]["detail"]
            )
    return HttpResponse(get_city_airport_list(data), "application/json")


def destination_airport_search(request):
    if request.is_ajax():
        try:
            data = amadeus.reference_data.locations.get(
                keyword=request.GET.get("term", None), subType=Location.ANY
            ).data
        except (ResponseError, KeyError, AttributeError) as error:
            messages.add_message(
                request, messages.ERROR, error.response.result["errors"][0]["detail"]
            )
    return HttpResponse(get_city_airport_list(data), "application/json")


def get_city_airport_list(data):
    result = []
    for i, val in enumerate(data):
        result.append(data[i]["iataCode"] + ", " + data[i]["name"])
    result = list(dict.fromkeys(result))
    return json.dumps(result)
