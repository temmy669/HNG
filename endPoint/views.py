from django.http import JsonResponse
import requests

def hello(request):
    visitor_name = request.GET.get('visitor_name', 'Guest')
    client_ip = request.META.get('REMOTE_ADDR', '127.0.0.1')

    location = "Unknown"
    try:
        response = requests.get(f'https://ipinfo.io/{client_ip}/json')
        if response.status_code == 200:
            data = response.json()
            location = data.get('city', 'Unknown')
    except Exception as e:
        pass

    return JsonResponse({
        'client_ip': client_ip,
        'location': location,
        'greeting': f'Hello, {visitor_name}!'
    })
