from django.core.management.base import BaseCommand
from django.conf import settings

from telegram import Update, ReplyKeyboardMarkup
from telegram.ext import Updater, CommandHandler, MessageHandler, Filters, CallbackContext

from weather.views import RequestHelper, WeatherAPIView

telegram_bot_name = settings.TELEGRAM_BOT_NAME
telegram_bot_token = settings.TELEGRAM_BOT_TOKEN


class Command(BaseCommand):
    message = f'Запущен бот {telegram_bot_name}'

    def handle(self, *args, **options):
        try:
            print(self.message)

            updater = Updater(token=telegram_bot_token, use_context=True)
            bot = updater.bot
            updater.dispatcher.add_handler(CommandHandler('start', start))
            updater.dispatcher.add_handler(MessageHandler(Filters.regex('^Узнать прогноз погоды$'), weather_button))
            updater.dispatcher.add_handler(MessageHandler(Filters.text & ~Filters.command, weather_message))
            updater.bot.deleteWebhook()
            updater.start_polling()
            updater.idle()
        except Exception as e:
            print(f"Ошибка: {e}")


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
