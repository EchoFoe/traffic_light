from django.urls import re_path

from .consumers import TgConsumer

websocket_urlpatterns = [
    re_path(r'ws/weather_bot/$', TgConsumer.as_asgi()),
]
