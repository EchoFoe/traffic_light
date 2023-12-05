from django.conf import settings
from django.test import TestCase, override_settings
from django.core.management import call_command
from unittest.mock import patch

from rest_framework import status
from rest_framework.test import APIRequestFactory

from .views import WeatherAPIView
from .management.commands.tg_weather_bot import Command


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


class TelegramBotTest(TestCase):
    """
        Класс-хелпер для тестирования телеграм бота.

        Реализует в себе следующий функционал:
        - test_handle_command: имититация методов start_polling и idle. Проверяет handle и ожидаемое сообщение в консоли
    """
    def setUp(self):
        self.mes = Command.message

    @patch('telegram.ext.Updater.start_polling')
    @patch('telegram.ext.Updater.idle')
    def test_handle_command(self, mock_start_polling, mock_idle):
        with patch('builtins.print') as mock_print:
            call_command('tg_weather_bot')

        mock_print.assert_called_with(f'{self.mes}')
        mock_start_polling.assert_called_once()
        mock_idle.assert_called_once()
