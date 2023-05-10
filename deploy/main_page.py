import streamlit as st
import datetime
import pickle
import requests
import catboost as cb
import pandas as pd

pickle_in = open('/app/data-science-project/deploy/catboost.pkl', 'rb')
classifier = pickle.load(pickle_in)

pickle_in = open('/app/data-science-project/deploy/label_encoder.pkl', 'rb')
label_encoder = pickle.load(pickle_in)

def prediction(origin, dest, flight_num, airline_id):
    x_test = [origin, dest, flight_num, airline_id]
    encoded_values = label_encoder.transform(x_test)

    prediction = classifier.predict([encoded_values])

    return prediction

def future_flights(origin, destination, date):
    ACCESS_KEY = 'eyJ0eXAiOiJKV1QiLCJhbGciOiJSUzI1NiJ9.eyJhdWQiOiI0IiwianRpIjoiNzAwNjdkODE3M2RkNjBhZDJhMzRmOTA0YWJlYWYzMmMxMWI5NTc4NDVhNjZlNTY2YmEwYzNmNDU5ZjMwMDJiZGZjOTQ4NWU0OGY3M2E3YTEiLCJpYXQiOjE2ODM0NDkxNzYsIm5iZiI6MTY4MzQ0OTE3NiwiZXhwIjoxNzE1MDcxNTc2LCJzdWIiOiIyMDkwNyIsInNjb3BlcyI6W119.kWCdY3rMHWxZEkpGK6L79ACOZtFx4gxxcpCt4cetBU4v4I8MZscD6y3-JMz3KfnAavAFxhBDRDn4-6dpEudvlQ'
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
        # print(flight_options)
        return flight_options
    except:
        st.write("invalid entry, try again")




if __name__ == "__main__":
    st.title('Flight Predictor')

    st.text("""
        This app predicts the amount of delay time a certain flight will have.
        Real available flights can be searched via origin airport, destination, airport, and date.
        After searching for available flights, the user can pick one of the flights to predict.
        """)

    with st.container():
        st.header("Predict a flight")

        origin = st.text_input("Origin Airport  e.g. PDX")
        dest = st.text_input("Destination Airport  e.g. GEG")
        min_date = datetime.date(2023, 6, 1)
        max_date = datetime.date(2024, 6, 1)
        date = st.date_input("Travel date", value=min_date, min_value=min_date, max_value=max_date)


        button1 = st.button('See available flights')
        if st.session_state.get('button') != True:
            st.session_state['button'] = button1 

        if st.session_state['button'] == True:
            with st.spinner("Finding flights"):
                flight_options = future_flights(origin, dest, date)

            st.write(flight_options)
            
            if flight_options != {}:
                output = []
                for i in range(len(flight_options)):
                    output.append(i)

                flight_pick = st.radio("Pick a flight option:", options=output)

                if st.button('Predict'):
                    origin_input = flight_options[flight_pick]["origin"]
                    dest_input = flight_options[flight_pick]["destination"]
                    flight_num = flight_options[flight_pick]["airline"]
                    airline_id = flight_options[flight_pick]["airline_id"]

                    result = prediction(origin, dest, flight_num, airline_id)
                    st.success("The predicted delay is {} minutes".format(result[0]))
            else:
                st.write("no flights available")




