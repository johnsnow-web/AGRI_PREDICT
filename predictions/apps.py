import requests
from django.http import JsonResponse

def get_weather(request, location):
    # URL for the Open-Meteo API
    url = f'https://api.open-meteo.com/v1/forecast?latitude={latitude}&longitude={longitude}&daily=temperature_2m_max,temperature_2m_min,precipitation_sum&timezone=auto'

    # Geocoding to convert location to latitude and longitude (using a free service)
    geocoding_url = f'https://nominatim.openstreetmap.org/search?q={location}&format=json&limit=1'
    geocoding_response = requests.get(geocoding_url)
    if geocoding_response.status_code == 200 and geocoding_response.json():
        geocoding_data = geocoding_response.json()[0]
        latitude = geocoding_data['lat']
        longitude = geocoding_data['lon']
    else:
        return JsonResponse({'error': 'Could not fetch location data'}, status=500)

    response = requests.get(url)
    if response.status_code == 200:
        data = response.json()
        return JsonResponse(data)
    else:
        return JsonResponse({'error': 'Could not fetch weather data'}, status=500)
