from django.shortcuts import render
from decouple import config
import requests
from pprint import pprint

from weather_api.forms import CityForm
from .models import City
from django.contrib import messages

# Create your views here.


def index(request):
    form = CityForm(request.POST or None)
    cities = City.objects.all()
    url = config('BASE_URL')
    # 'https//:api.openweathermap.org/data/2.5/weather?q={}&appid={1472d45692e32647ab60932e589a2145}'.format(value)
    # city = 'Berlin'
    # print(type(content))
    if form.is_valid():
        n_city = form.cleaned_data["name"]
        if not City.objects.filter(name=n_city).exists():
            r = requests.get(url.format(n_city))
            if r.status_code == 200:
                form.save()
            else:
                messages.warning(request, "There is no city like that")
        else:
            messages.warning(request, "This city is already exist")

    city_data = []
    for city in cities:
        print(city)
        r = requests.get(url.format(city))
        content = r.json()
        pprint(content)
        data = {
            "city": city.name,
            "temperature": content["main"]["temp"],
            "description": content["weather"][0]["description"],
            "icon": content["weather"][0]["icon"]
        }
        city_data.append(data)
    print(city_data)
    context = {
        "form": form,
        "city_data": city_data
    }
    return render(request, "weather_api/index.html", context)
