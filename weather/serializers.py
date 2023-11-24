from rest_framework import serializers


class WeatherSerializer(serializers.Serializer):
    temperature = serializers.FloatField()
    pressure = serializers.FloatField()
    wind_speed = serializers.FloatField()

    class Meta:
        fields = ['temperature', 'pressure', 'wind_speed']
