# views.py

from django.shortcuts import render
from .forms import WeatherForm 
import requests
from bs4 import BeautifulSoup
from django.http import JsonResponse
import joblib
import pandas as pd

# Load the trained model
model = joblib.load('pesticide_model.pkl')

def get_weather(request):
    if request.method == 'POST':
        form = WeatherForm(request.POST)
        if form.is_valid():
            location = form.cleaned_data['location']
            plant = form.cleaned_data['plant']
            weather_data = fetch_weather_data(location)
            if 'error' in weather_data:
                return JsonResponse(weather_data, status=400)
            else:
                return render(request, 'weather_result.html', {'weather_data': weather_data})
    else:
        form = WeatherForm()
    return render(request, 'get_weather.html', {'form': form})

def fetch_weather_data(location):
    try:
        # Perform a browser search to get the weather data
        search_url = f'https://www.google.com/search?q=weather+{location}'
        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
        }
        response = requests.get(search_url, headers=headers)

        if response.status_code == 200:
            soup = BeautifulSoup(response.text, 'html.parser')
            weather_data = {}

            # Extract weather information from the search result page
            weather_data['location'] = location
            weather_data['temperature'] = int(soup.find('span', {'id': 'wob_tm'}).text)
            weather_data['condition'] = soup.find('span', {'id': 'wob_dc'}).text
            weather_data['precipitation'] = soup.find('span', {'id': 'wob_pp'}).text
            weather_data['humidity'] = int(soup.find('span', {'id': 'wob_hm'}).text.replace('%', ''))
            weather_data['wind'] = soup.find('span', {'id': 'wob_ws'}).text

            # Prepare the input data for the model
            input_data = pd.DataFrame([{
                'temperature': weather_data['temperature'],
                'humidity': weather_data['humidity']
            }])

            # Check for NaN values in the input data
            if input_data.isna().any().any():
                return {'error': 'Weather data contains NaN values'}

            # Make prediction using the trained model
            pesticide_combined = model.predict(input_data)[0]

            # Split the combined suggestion and name
            pesticide_suggestion, pesticide_name = pesticide_combined.split(" (")
            pesticide_name = pesticide_name.rstrip(')')  # Remove the trailing parenthesis

            weather_data['pesticide_suggestion'] = pesticide_suggestion
            weather_data['pesticide_name'] = pesticide_name

            return weather_data
        else:
            return {'error': 'Could not fetch weather data'}
    except Exception as e:
        return {'error': str(e)}

