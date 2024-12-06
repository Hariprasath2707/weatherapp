from django.shortcuts import render
from django.contrib import messages
import requests
import datetime
import os

def home(request):
    city = request.POST.get('city', 'chennai')  # Default city is 'indore'

    # OpenWeather API
    weather_api_key = os.getenv('OPENWEATHER_API_KEY', '3b4fa0f5a71010c03f830608f75a1b03')
    weather_url = f'https://api.openweathermap.org/data/2.5/weather'
    weather_params = {'q': city, 'appid': weather_api_key, 'units': 'metric'}

    # Unsplash API
    unsplash_access_key = os.getenv('UNSPLASH_ACCESS_KEY', 'BZbHWr77h6A6W7kmtMQa52qt8m3ZvgbyJnC_R4gYy1U')
    unsplash_url = f'https://api.unsplash.com/search/photos'
    unsplash_params = {'query': city + ' cityscape', 'client_id': unsplash_access_key, 'per_page': 1}

    try:
        # Fetch weather data
        weather_response = requests.get(weather_url, params=weather_params)
        weather_response.raise_for_status()
        weather_data = weather_response.json()

        description = weather_data['weather'][0]['description']
        icon = weather_data['weather'][0]['icon']
        temp = weather_data['main']['temp']
        day = datetime.date.today()

        # Fetch Unsplash image
        unsplash_response = requests.get(unsplash_url, params=unsplash_params)
        unsplash_response.raise_for_status()
        unsplash_data = unsplash_response.json()
        image_url = unsplash_data['results'][0]['urls']['regular'] if 'results' in unsplash_data and unsplash_data['results'] else 'https://via.placeholder.com/1600x900?text=City+Image+Not+Available'

    except requests.exceptions.RequestException as e:
        # Handle API errors
        print(f"Error: {e}")
        description = 'clear sky'
        icon = '01d'
        temp = 25
        day = datetime.date.today()
        city = 'indore'
        image_url = 'https://via.placeholder.com/1600x900?text=City+Image+Not+Available'
        messages.error(request, 'Unable to fetch city or weather information.')

    return render(request, 'weatherapp/index.html', {
        'description': description,
        'icon': icon,
        'temp': temp,
        'day': day,
        'city': city,
        'image_url': image_url,
    })
