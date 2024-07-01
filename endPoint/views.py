from django.http import JsonResponse
import requests

def hello(request):
    visitor_name = request.GET.get('visitor_name', 'Guest')
    client_ip = request.META.get('REMOTE_ADDR', '127.0.0.1')

    # Get the location information based on the IP
    location = "Unknown"
    lat, lon = None, None
    try:
        ip_info_response = requests.get(f'https://ipinfo.io/{client_ip}/json')
        if ip_info_response.status_code == 200:
            ip_info_data = ip_info_response.json()
            location = ip_info_data.get('city', 'Unknown')
            loc = ip_info_data.get('loc', '')
            if loc:
                lat, lon = loc.split(',')
    except Exception as e:
        pass

    # Get the weather information based on the location
    temperature = "unknown"
    if lat and lon:
        weather_api_key = 'YOUR_OPENWEATHERMAP_API_KEY'
        weather_url = f'https://api.openweathermap.org/data/2.5/weather?lat={lat}&lon={lon}&units=metric&appid={weather_api_key}'
        try:
            weather_response = requests.get(weather_url)
            if weather_response.status_code == 200:
                weather_data = weather_response.json()
                temperature = weather_data['main']['temp']
        except Exception as e:
            pass

    greeting = f"Hello, {visitor_name}!, the temperature is {temperature} degrees Celsius in {location}"

    return JsonResponse({
        'client_ip': client_ip,
        'location': location,
        'greeting': greeting,
    })
