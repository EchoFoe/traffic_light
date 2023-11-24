from django.urls import path
from .views import *

urlpatterns = [
    path('weather/', WeatherAPIView.as_view(), name='weather-api'),
]
