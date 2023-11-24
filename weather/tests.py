from django.conf import settings
from django.test import TestCase, override_settings
from rest_framework import status
from rest_framework.test import APIRequestFactory
from .views import WeatherAPIView


class WeatherAPITests(TestCase):
    """
        Класс-хелпер для тестирования получения данных о погоде по названию города.

        Реализует в себе следующий функционал:
        - test_get_weather_data: проверка на статус 200 и проверка получения данных о погоде в запросе по г. Москва.
    """
    def setUp(self):
        self.factory = APIRequestFactory()

    def test_get_weather_data(self):
        with override_settings(
                GEOCODE_API_KEY=settings.GEOCODE_API_KEY,
                WEATHER_API_KEY=settings.WEATHER_API_KEY,
                WEATHER_API_URL=settings.WEATHER_API_URL,
        ):
            moscow_request = self.factory.get('/weather/?city=Москва')
            weather_view = WeatherAPIView.as_view()
            weather_response = weather_view(moscow_request)

            self.assertEqual(weather_response.status_code, status.HTTP_200_OK)
            self.assertIn('temperature', weather_response.data)
            self.assertIn('pressure', weather_response.data)
            self.assertIn('wind_speed', weather_response.data)
