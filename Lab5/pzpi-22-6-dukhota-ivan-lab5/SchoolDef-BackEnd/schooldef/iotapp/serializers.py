from rest_framework import serializers
from .models import Sensor, Camera

class SensorSerializer(serializers.ModelSerializer):
    class Meta:
        model = Sensor
        fields = '__all__'

class CameraSerializer(serializers.ModelSerializer):
    class Meta:
        model = Camera
        fields = '__all__'
