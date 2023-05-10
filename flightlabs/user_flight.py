import requests

ACCESS_KEY = 'eyJ0eXAiOiJKV1QiLCJhbGciOiJSUzI1NiJ9.eyJhdWQiOiI0IiwianRpIjoiNzAwNjdkODE3M2RkNjBhZDJhMzRmOTA0YWJlYWYzMmMxMWI5NTc4NDVhNjZlNTY2YmEwYzNmNDU5ZjMwMDJiZGZjOTQ4NWU0OGY3M2E3YTEiLCJpYXQiOjE2ODM0NDkxNzYsIm5iZiI6MTY4MzQ0OTE3NiwiZXhwIjoxNzE1MDcxNTc2LCJzdWIiOiIyMDkwNyIsInNjb3BlcyI6W119.kWCdY3rMHWxZEkpGK6L79ACOZtFx4gxxcpCt4cetBU4v4I8MZscD6y3-JMz3KfnAavAFxhBDRDn4-6dpEudvlQ'

def flight_options():
    params = {
        'access_key': ACCESS_KEY,
        'adults': 1,
        'origin': 'PDX',
        'destination': 'GEG',
        'departureDate': '2023-06-20'
    }

    api_result = requests.get('https://app.goflightlabs.com/flights', params)

    api_response = api_result.json()
    print(api_response)

def future_flights(origin, destination, date):
    
    try:
        params = {
            'access_key': ACCESS_KEY,
            'adults': 1,
            'origin': origin,
            'destination': destination,
            'departureDate': date
        }
        api_result = requests.get('https://app.goflightlabs.com/search-all-flights', params)
        api_response = api_result.json()

        flight_options = {}
        count = 0
        for i in api_response["data"]["results"]:
            if i["legs"][0]["stopCount"] == 0:
                flight_option = {
                        'origin': i["legs"][0]["segments"][0]["origin"]["flightPlaceId"],
                        'destination': i["legs"][0]["segments"][0]["destination"]["flightPlaceId"],
                        'flightNumber': i["legs"][0]["segments"][0]["flightNumber"],
                        'departureTime': i["legs"][0]["segments"][0]["departure"],
                        'arrivalTime': i["legs"][0]["segments"][0]["arrival"],
                        'airline': i["legs"][0]["segments"][0]["marketingCarrier"]["name"],
                        'airline_id': i["legs"][0]["segments"][0]["marketingCarrier"]["alternate_di"]
                }
                flight_options[count] = flight_option
                count = count + 1
            else:
                print("StopCount:", i["legs"][0]["stopCount"])
        print(flight_options)
    except:
        print("invalid entry")


def best_flight(origin, destination, date):
    ACCESS_KEY = 'eyJ0eXAiOiJKV1QiLCJhbGciOiJSUzI1NiJ9.eyJhdWQiOiI0IiwianRpIjoiNzAwNjdkODE3M2RkNjBhZDJhMzRmOTA0YWJlYWYzMmMxMWI5NTc4NDVhNjZlNTY2YmEwYzNmNDU5ZjMwMDJiZGZjOTQ4NWU0OGY3M2E3YTEiLCJpYXQiOjE2ODM0NDkxNzYsIm5iZiI6MTY4MzQ0OTE3NiwiZXhwIjoxNzE1MDcxNTc2LCJzdWIiOiIyMDkwNyIsInNjb3BlcyI6W119.kWCdY3rMHWxZEkpGK6L79ACOZtFx4gxxcpCt4cetBU4v4I8MZscD6y3-JMz3KfnAavAFxhBDRDn4-6dpEudvlQ'

    params = {
        'access_key': ACCESS_KEY,
        'adults': 1,
        'origin': origin,
        'destination': destination,
        'departureDate': date
    }
    api_result = requests.get('https://app.goflightlabs.com/search-best-flights', params)
    api_response = api_result.json()

    print(api_response)

    for i in api_response["data"]["buckets"][0]:
        origin = i["items"][0]["legs"][0]["origin"]["id"]
        dest = i["items"][0]["legs"][0]["destination"]["id"]

        departure_time = i["items"][0]["legs"][0]["departure"]
        arrival_time = i["items"][0]["legs"][0]["departure"]

        stop_count = i["items"][0]["legs"][0]["stopCount"]

        flight_num = i["items"][0]["legs"][0]["segments"]["flightNumber"]

        carrier_name = i["items"][0]["legs"][0]["segments"]["operatingCarrier"]["name"]
        carrier_id = i["items"][0]["legs"][0]["segments"]["operatingCarrier"]["alternateId"]
    # origin = api_response["data"]["buckets"][0]["items"][0]["legs"][0]["origin"]["id"]
    # dest = api_response["data"]["buckets"][0]["items"][0]["legs"][0]["destination"]["id"]

    # departure_time = api_response["data"]["buckets"][0]["items"][0]["legs"][0]["departure"]
    # arrival_time = api_response["data"]["buckets"][0]["items"][0]["legs"][0]["departure"]

    # stop_count = api_response["data"]["buckets"][0]["items"][0]["legs"][0]["stopCount"]

    # flight_num = api_response["data"]["buckets"][0]["items"][0]["legs"][0]["segments"]["flightNumber"]

    # carrier_name = api_response["data"]["buckets"][0]["items"][0]["legs"][0]["segments"]["operatingCarrier"]["name"]
    # carrier_id = api_response["data"]["buckets"][0]["items"][0]["legs"][0]["segments"]["operatingCarrier"]["alternateId"]

        flight_option = {
            'origin': origin,
            'destination': dest,
            'flight_number': flight_num,
            'departure_time': departure_time,
            'arrival_time': arrival_time,
            'airline': carrier_name,
            'airline_id': carrier_id,
            'stop_count': stop_count
        }

        print(flight_option)

def future_flights_any(origin, destination, date):
    params = {
        'access_key': ACCESS_KEY,
        'adults': 1,
        'origin': origin,
        'destination': destination,
        'departureDate': date
    }
    api_result = requests.get('https://app.goflightlabs.com/search-all-flights', params)
    api_response = api_result.json()

    flight_options = {}
    count = 0
    for i in api_response["data"]["results"]:
        flight_option = {
                'origin': i["legs"][0]["segments"][0]["origin"]["flightPlaceId"],
                'destination': i["legs"][0]["segments"][0]["destination"]["flightPlaceId"],
                'flightNumber': i["legs"][0]["segments"][0]["flightNumber"],
                'departureTime': i["legs"][0]["segments"][0]["departure"],
                'arrivalTime': i["legs"][0]["segments"][0]["arrival"],
                'airline': i["legs"][0]["segments"][0]["marketingCarrier"]["name"],
                'airline_id': i["legs"][0]["segments"][0]["marketingCarrier"]["alternate_di"]
        }
        flight_options[count] = flight_option
        count = count + 1

    print(flight_options)


if __name__ == "__main__":
    future_flights('PDX','JFK','2023-06-12')