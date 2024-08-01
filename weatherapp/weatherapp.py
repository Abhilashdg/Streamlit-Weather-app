import streamlit as st
import requests
import pandas as pd
from datetime import datetime

st.title('Weather Forecast App')

if 'weather_data' not in st.session_state:
    st.session_state.weather_data = pd.DataFrame(columns=['City', 'Time', 'Description', 'Temperature', 'Humidity', 'Wind Speed'])

city = st.text_input('Enter city name')


if city:
    api_key = '7a613f8d17019e6dda5e12954cfeb3b1'
    url = f'http://api.openweathermap.org/data/2.5/weather?q={city}&appid={api_key}'
    response = requests.get(url)
    data = response.json()

    if response.status_code == 401:
        st.error("Invalid API key. Please check your API key and try again.")
    elif response.status_code != 200:
        st.error(data.get('message', 'Error fetching data.'))
    else:
   
        city_name = data['name']
        weather_description = data['weather'][0]['description']
        temperature_celsius = data['main']['temp'] - 273.15
        humidity = data['main']['humidity']
        wind_speed = data['wind']['speed']

      
        current_time = datetime.now()
       
        new_data = pd.DataFrame({
            'City': [city_name],
            'Time': [current_time],
            'Description': [weather_description],
            'Temperature': [temperature_celsius],
            'Humidity': [humidity],
            'Wind Speed': [wind_speed]
        })
      
        st.session_state.weather_data = pd.concat([st.session_state.weather_data, new_data], ignore_index=True)
     
        st.write(st.session_state.weather_data)
   
        temp_chart = st.session_state.weather_data.pivot(index='Time', columns='City', values='Temperature')
        st.line_chart(temp_chart)

if st.button("Clear Data"):
    st.session_state.weather_data = pd.DataFrame(columns=['City', 'Time', 'Description', 'Temperature', 'Humidity', 'Wind Speed'])
    st.success("All data cleared. You can start a new search.")
