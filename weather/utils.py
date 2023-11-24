import requests
from django.conf import settings

ya_geocode_maps_url = settings.YA_GEOCODE_MAPS_URL


def get_yandex_geocode_data(ya_geocode_api_key, city_name):
    """
        Функция, получающая координаты по названию города.
    """

    params = {
        'apikey': ya_geocode_api_key,
        'format': 'json',
        'geocode': city_name,
    }

    response = requests.get(ya_geocode_maps_url, params=params)
    data = response.json()

    try:
        point = data['response']['GeoObjectCollection']['featureMember'][0]['GeoObject']['Point']['pos']
        longitude, latitude = map(float, point.split())
        return {'latitude': latitude, 'longitude': longitude}
    except (KeyError, IndexError):
        return None
