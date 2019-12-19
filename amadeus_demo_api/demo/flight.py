from datetime import datetime, timedelta


class Flight:
    def __init__(self, flight):
        self.flight = flight

    def construct_flights(self):
        offer = {}
        index = 0
        offer['price'] = self.flight['price']['total']
        offer['id'] = self.flight['id']

        for f in self.flight['itineraries']:
            # Keys starting from 0 correspond to Outbound flights and the keys starting from 1 tp Return flights
            if len(self.flight['itineraries'][index]['segments']) == 2:  # one stop flight
                offer[str(index) + 'firstFlightDepartureAirport'] = self.flight['itineraries'][index]['segments'][0]['departure']['iataCode']
                offer[str(index) + 'firstFlightAirlineLogo'] = get_airline_logo(self.flight['itineraries'][index]['segments'][0]['carrierCode'])
                offer[str(index) + 'firstFlightAirline'] = self.flight['itineraries'][index]['segments'][0]['carrierCode']
                offer[str(index) + 'firstFlightDepartureDate'] = get_hour(self.flight['itineraries'][index]['segments'][0]['departure']['at'])
                offer[str(index) + 'firstFlightArrivalAirport'] = self.flight['itineraries'][index]['segments'][0]['arrival']['iataCode']
                offer[str(index) + 'firstFlightArrivalDate'] = get_hour(self.flight['itineraries'][index]['segments'][0]['arrival']['at'])
                offer[str(index) + 'firstFlightArrivalDuration'] = self.flight['itineraries'][index]['segments'][0]['duration']
                offer[str(index) + 'secondFlightDepartureAirport'] = self.flight['itineraries'][index]['segments'][1]['departure']['iataCode']
                offer[str(index) + 'secondFlightDepartureDate'] = get_hour(self.flight['itineraries'][index]['segments'][1]['departure']['at'])
                offer[str(index) + 'secondFlightAirlineLogo'] = get_airline_logo(self.flight['itineraries'][index]['segments'][1]['carrierCode'])
                offer[str(index) + 'secondFlightAirline'] = self.flight['itineraries'][index]['segments'][1]['carrierCode']
                offer[str(index) + 'secondFlightArrivalAirport'] = self.flight['itineraries'][index]['segments'][1]['arrival']['iataCode']
                offer[str(index) + 'secondFlightArrivalDate'] = get_hour(self.flight['itineraries'][index]['segments'][1]['arrival']['at'])
                offer[str(index) + 'secondFlightArrivalDuration'] = self.flight['itineraries'][index]['segments'][1]['duration']
                offer[str(index) + 'FlightTotalDuration'] = self.flight['itineraries'][index]['duration']


            elif len(self.flight['itineraries'][0]['segments']) == 1:  # direct flight
                offer[str(index) + 'firstFlightDepartureAirport'] = self.flight['itineraries'][index]['segments'][0]['departure']['iataCode']
                offer[str(index) + 'firstFlightAirlineLogo'] = get_airline_logo(self.flight['itineraries'][index]['segments'][0]['carrierCode'])
                offer[str(index) + 'firstFlightAirline'] = self.flight['itineraries'][index]['segments'][0]['carrierCode']
                offer[str(index) + 'firstFlightDepartureDate'] = get_hour(self.flight['itineraries'][index]['segments'][0]['departure']['at'])
                offer[str(index) + 'firstFlightArrivalAirport'] = self.flight['itineraries'][index]['segments'][0]['arrival']['iataCode']
                offer[str(index) + 'firstFlightArrivalDate'] = get_hour(self.flight['itineraries'][index]['segments'][0]['arrival']['at'])
                offer[str(index) + 'firstFlightArrivalDuration'] = self.flight['itineraries'][index]['segments'][0]['duration']
                offer[str(index) + 'FlightTotalDuration'] = self.flight['itineraries'][index]['duration']

            index += 1
        return offer

'''


def get_stoptime(arrival_stop_time, departure_stop_time):
    arrival = datetime.strptime(arrival_stop_time[0:19], "%Y-%m-%dT%H:%M:%S")
    departure = datetime.strptime(departure_stop_time[0:19], "%Y-%m-%dT%H:%M:%S")
    stoptime = str(timedelta(seconds=(departure - arrival).seconds))
    if stoptime[1] == ':':
        stoptime = '0' + stoptime
    return stoptime[0:5]

'''
def get_airline_logo(carrier_code):
    return "https://s1.apideeplink.com/images/airlines/" + carrier_code + ".png"

def get_hour(date_time):
    return datetime.strptime(date_time[0:19], "%Y-%m-%dT%H:%M:%S").strftime("%H:%M")

def get_duration(duration):
    res = datetime.strptime(duration, "%wDT%HH%MM")
    return res.strftime("%H:%M")