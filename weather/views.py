import requests
from django.core.cache import cache
from django.utils import timezone
from django.conf import settings
from rest_framework import status
from rest_framework.views import APIView
from rest_framework.response import Response

from telegram import Update, ReplyKeyboardMarkup
from telegram.ext import Updater, CommandHandler, MessageHandler, Filters, CallbackContext

from .utils import get_yandex_geocode_data
from .serializers import WeatherSerializer

weather_api_key = settings.WEATHER_API_KEY
geocode_api_key = settings.GEOCODE_API_KEY
ya_geocode_maps_url = settings.YA_GEOCODE_MAPS_URL
weather_api_url = settings.WEATHER_API_URL
telegram_bot_token = settings.TELEGRAM_BOT_TOKEN
telegram_bot_name = settings.TELEGRAM_BOT_NAME


class RequestHelper:
    """
        Класс, формирующий фиктивный запрос для бота.
    """

    def __init__(self, query_params):
        self.query_params = query_params


class WeatherAPIView(APIView):
    """
        Класс, реализующий АПИ.

        Реализует в себе следующий функционал:
        - get: HTTP запрос, возвращающий данные о погоде в гоородском сегменте.
    """

    def get(self, request):
        # Название города
        city_name = request.query_params.get('city', '').lower()

        # Проверка на город
        if not city_name:
            return Response({'error': 'Название города обязательное требование!'}, status=status.HTTP_400_BAD_REQUEST)

        # Закешируем город
        cached_weather_data = cache.get(city_name)
        if cached_weather_data:
            serializer = WeatherSerializer(data=cached_weather_data)
            serializer.is_valid()
            return Response(serializer.data)

        # Получение координат по названию города
        geocode_data = get_yandex_geocode_data(geocode_api_key, city_name)

        if not geocode_data:
            return Response(
                {'error': f'Невозможно получить геоданные для {city_name}'},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )

        # Формирование параметров для корректного запроса к АПИ Яндекс погода
        params = {'lang': 'ru_RU', 'lat': geocode_data['latitude'], 'lon': geocode_data['longitude']}
        headers = {'X-Yandex-API-Key': weather_api_key}

        try:
            # Запрос к АПИ Яндекс погода
            response = requests.get(weather_api_url, params=params, headers=headers)
            response.raise_for_status()
            data = response.json()
            # Извлечение данных о погоде
            weather_data = {
                'temperature': data['temp'],
                'pressure': data['pressure_mm'],
                'wind_speed': data['wind_speed'],
            }
            # Сериализация данных о погоде
            serializer = WeatherSerializer(data=weather_data)
            serializer.is_valid(raise_exception=True)

            # Установка кеша по названию горожда (30 минут) для исключения повторных запросов
            if city_name in cache and (timezone.now() - cache.get('last_updated_time')).seconds < 30 * 60:
                cache.set(city_name, serializer.data, 60 * 30)

            return Response(serializer.data)
        except requests.RequestException as e:
            error_message = {'error': f'Ошибка при получении данных о погоде: {str(e)}'}
            return Response(error_message, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


def start(update: Update, context: CallbackContext):
    keyboard = [['Узнать прогноз погоды']]
    reply_markup = ReplyKeyboardMarkup(keyboard, resize_keyboard=True, one_time_keyboard=True)
    update.message.reply_text(
        f'Добро пожаловать в {telegram_bot_name}! Нажмите кнопку, чтобы узнать прогноз погоды.',
        reply_markup=reply_markup
    )


def weather_button(update: Update, context: CallbackContext):
    update.message.reply_text('Пожалуйста, введите название города, чтобы получить прогноз погоды.')


def weather_message(update: Update, context: CallbackContext):
    city_name = update.message.text.strip()
    # Формирование фиктивного объекта запроса
    request = RequestHelper({'city': city_name})
    weather_api = WeatherAPIView()
    response = weather_api.get(request)

    # Формирование сообщения для тг-бота
    mes = (
        f"Погода в {city_name.capitalize()}:\n"
        f"Температура: {response.data['temperature']}°C\n"
        f"Давление: {response.data['pressure']} мм. рт. ст.\n"
        f"Скорость ветра: {response.data['wind_speed']} м/с"
    )

    update.message.reply_text(mes)


# Исключаю проверку бота, так как ТЗ
if not settings.TESTING:
    updater = Updater(token=telegram_bot_token, use_context=True)
    bot = updater.bot
    updater.dispatcher.add_handler(CommandHandler('start', start))
    updater.dispatcher.add_handler(MessageHandler(Filters.regex('^Узнать прогноз погоды$'), weather_button))
    updater.dispatcher.add_handler(MessageHandler(Filters.text & ~Filters.command, weather_message))
    updater.bot.deleteWebhook()
    updater.start_polling()
    updater.idle()
