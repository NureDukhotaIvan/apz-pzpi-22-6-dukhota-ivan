from rest_framework import viewsets
from .models import Sensor, Camera
from .serializers import SensorSerializer, CameraSerializer
from userapp.permissions import IsAdmin

class SensorViewSet(viewsets.ModelViewSet):
    queryset = Sensor.objects.all()
    serializer_class = SensorSerializer
    permission_classes = [IsAdmin]

class CameraViewSet(viewsets.ModelViewSet):
    queryset = Camera.objects.all()
    serializer_class = CameraSerializer
    permission_classes = [IsAdmin]