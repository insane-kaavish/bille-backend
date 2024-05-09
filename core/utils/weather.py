import requests
# from ..models import *
from datetime import datetime
import dotenv
import os

dotenv.load_dotenv()

WEATHER_API_URL = os.getenv('WEATHER_API_URL')
WEATHER_API_KEY = os.getenv('WEATHER_API_KEY')

def get_current_weather_data():
    url = f'{WEATHER_API_URL}/current.json?key={WEATHER_API_KEY}&q=Karachi&aqi=no'
    # Make a call to the weather API
    response = requests.get(url)

    # Process the response data
    if response.status_code == 200:
        weather_data = response.json()
        # Do something with the weather data
        temp = weather_data['current']['temp_c']
        condition = weather_data['current']['condition'].get('text', '')
        icon = weather_data['current']['condition'].get('icon', '')
        humidity = weather_data['current'].get('humidity', None)
        return {
            'temp': temp,
            'condition': condition,
            'icon': icon,
            'humidity': humidity
        }
    else:
        return {
            'error': 'Failed to get weather data'
        }
    
def get_weather_data(date):
    url = f'{WEATHER_API_URL}/history.json?key={WEATHER_API_KEY}&q=Karachi&dt={date}'
    # Make a call to the weather API
    response = requests.get(url)

    # Process the response data
    if response.status_code == 200:
        weather_data = response.json()
        # Do something with the weather data
        temp = weather_data['forecast']['forecastday'][0]['day']['avgtemp_c']
        condition = weather_data['forecast']['forecastday'][0]['day']['condition']['text']
        icon = weather_data['forecast']['forecastday'][0]['day']['condition']['icon']
        humidity = weather_data['forecast']['forecastday'][0]['day']['avghumidity']
        return {
            'temp': temp,
            'condition': condition,
            'icon': icon,
            'humidity': humidity
        }
    else:
        return {
            'error': 'Failed to get weather data'
        }

def get_weekly_weather():
    url = f'{WEATHER_API_URL}/forecast.json?key={WEATHER_API_KEY}&q=Karachi&days=7&aqi=no&alerts=no'
    # Make a call to the weather API
    response = requests.get(url)
    
    # Process the response data
    if response.status_code == 200:
        weather_data = response.json()
        # Do something with the weather data
        forecast = []
        for day in weather_data['forecast']['forecastday']:
            date = day['date']
            temp = day['day']['avgtemp_c']
            condition = day['day']['condition'].get('text', '')
            icon = day['day']['condition'].get('icon', '')
            humidity = day['day'].get('avghumidity', None)
            forecast.append({
                'date': date,
                'temp': temp,
                'condition': condition,
                'icon': icon,
                'humidity': humidity
            })
        return forecast
    else:
        return {
            'error': 'Failed to get weather data'
        }

def get_weekly_weather_inference(weather_forecast):
    # Initialize counters for various weather conditions
    pleasant_days = 0
    hot_days = 0
    humid_days = 0

    for day in weather_forecast:
        temp = day['temp']
        condition = day['condition']
        humidity = day['humidity']

        # Check for pleasant weather (temperature between 20-30 degrees Celsius)
        if temp >= 20 and temp <= 30:
            pleasant_days += 1

        # Check for hot weather (temperature above 30 degrees Celsius)
        if temp > 30:
            hot_days += 1

        # Check for humid weather (humidity above 60%)
        if humidity > 60:
            humid_days += 1

    inference = "Based on the upcoming week's forecast: "
    if pleasant_days > hot_days and pleasant_days > humid_days:
        inference += "The weather is expected to be mostly pleasant."
    elif hot_days > pleasant_days and hot_days > humid_days:
        inference += "The weather is expected to be mostly hot."
    elif humid_days > pleasant_days and humid_days > hot_days:
        inference += "The weather is expected to be mostly humid."
    else:
        inference += "The weather conditions are varied."

    return {
        'title': 'Weekly Weather Prediction',
        'inference': inference
    }

# Compare today's weather with last year's weather
def compare_weather():
    today = datetime.now()
    today_date = today.strftime('%Y-%m-%d')
    last_year = today.year - 1
    last_year_date = f'{last_year}-{today.month}-{today.day}'
    today_weather = get_weather_data(today_date)
    last_year_weather = get_weather_data(last_year_date)
    
    if 'error' in today_weather:
        return today_weather
    elif 'error' in last_year_weather:
        return last_year_weather
    else:
        inference = "Comparing today's weather with the same date last year: "
        if today_weather['temp'] < last_year_weather['temp']:
            inference += "The weather today is cooler than last year."
        elif today_weather['temp'] > last_year_weather['temp']:
            inference += "The weather today is hotter than last year."
        else:
            inference += "The weather today is similar to last year."

        if today_weather['humidity'] > last_year_weather['humidity']:
            inference += " The humidity today is higher than last year."
        elif today_weather['humidity'] < last_year_weather['humidity']:
            inference += " The humidity today is lower than last year."
        else:
            inference += " The humidity today is similar to last year."

        return {
            'title': 'Weather Comparison',
            'inference': inference
        }
