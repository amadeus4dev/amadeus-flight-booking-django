import json
from amadeus import Client, ResponseError, Location
from django.shortcuts import render
from django.contrib import messages
from .flight import Flight
from django.http import HttpResponse

amadeus = Client(
    client_id='',
    client_secret='',
    log_level='debug',
    hostname=''
)


def demo(request):
    origin = request.POST.get('Origin')
    destination = request.POST.get('Destination')
    departureDate = request.POST.get('Departuredate')
    returnDate = request.POST.get('Returndate')
    adults = request.POST.get('Adults')

    kwargs = {'originLocationCode': request.POST.get('Origin'), 'destinationLocationCode': request.POST.get('Destination'),
              'departureDate': request.POST.get('Departuredate')}
    if adults:
        kwargs['adults'] = adults
    else:
        kwargs['adults'] = 1
    tripPurpose = ''
    if returnDate:
        kwargs['returnDate'] = returnDate
        try:
            trip_purpose_response = amadeus.travel.predictions.trip_purpose.get(originLocationCode=origin,
                                                                                destinationLocationCode=destination,
                                                                                departureDate=departureDate,
                                                                                returnDate=returnDate).data
            tripPurpose = trip_purpose_response['result']
        except ResponseError as error:
            messages.add_message(request, messages.ERROR, error)
            return render(request, 'demo/demo_form.html', {})

    if origin and destination and departureDate:
        try:
            search_flights = amadeus.shopping.flight_offers_search.get(**kwargs)
        except ResponseError as error:
            messages.add_message(request, messages.ERROR, error)
            return render(request, 'demo/demo_form.html', {})
        search_flights_returned = []
        for flight in search_flights.data:
            offer = Flight(flight).construct_flights()
            search_flights_returned.append(offer)
            response = zip(search_flights_returned, search_flights.data)

        return render(request, 'demo/results.html', {'response': response,
                                                     'origin': origin,
                                                     'destination': destination,
                                                     'departureDate': departureDate,
                                                     'returnDate': returnDate,
                                                     'tripPurpose': tripPurpose,
                                                     })
    return render(request, 'demo/demo_form.html', {})


def origin_airport_search(request):
    if request.is_ajax():
        try:
            data = amadeus.reference_data.locations.get(keyword=request.GET.get('term', None), subType=Location.ANY).data
        except ResponseError as error:
            messages.add_message(request, messages.ERROR, error)
    return HttpResponse(get_city_airport_list(data), 'application/json')


def destination_airport_search(request):
    if request.is_ajax():
        try:
            data = amadeus.reference_data.locations.get(keyword=request.GET.get('term', None), subType=Location.ANY).data
        except ResponseError as error:
            messages.add_message(request, messages.ERROR, error)
    return HttpResponse(get_city_airport_list(data), 'application/json')


def get_city_airport_list(data):
    result = []
    for i, val in enumerate(data):
        result.append(data[i]['iataCode']+', '+data[i]['name'])
    result = list(dict.fromkeys(result))
    
    return json.dumps(result)


def book_flight(request, flight):
    try:
        offers_price_results = amadeus.shopping.flight_offers.pricing.post(flight)
    except ResponseError as error:
        messages.add_message(request, messages.ERROR, error)
        return render(request, 'demo/book_flight.html', {'flight': '['+flight+']'})
    return render(request, 'demo/book_flight.html', {'flight': offers_price_results})
