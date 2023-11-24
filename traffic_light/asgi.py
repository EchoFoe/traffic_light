# import os
#
# from django.core.asgi import get_asgi_application
#
# os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'traffic_light.settings')
#
# application = get_asgi_application()

import os
from django.core.asgi import get_asgi_application
from channels.routing import ProtocolTypeRouter, URLRouter
from channels.auth import AuthMiddlewareStack
from django.urls import path

from weather.consumers import TgConsumer

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'traffic_light.settings')

application = ProtocolTypeRouter({
    "http": get_asgi_application(),
    "websocket": AuthMiddlewareStack(
        URLRouter(
            [
                path("ws/weather_bot/", TgConsumer.as_asgi()),
            ]
        )
    ),
})
