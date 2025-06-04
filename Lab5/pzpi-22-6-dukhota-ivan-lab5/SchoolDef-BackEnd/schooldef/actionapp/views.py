from rest_framework import viewsets
from .models import Incident, Attendance, Notification
from .serializers import IncidentSerializer, AttendanceSerializer, NotificationSerializer
from userapp.permissions import IsAdmin
from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
import random
from .models import Incident
from iotapp.models import Sensor, Camera
from rest_framework.decorators import api_view
from rest_framework import status

class IncidentViewSet(viewsets.ModelViewSet):
    queryset = Incident.objects.all()
    serializer_class = IncidentSerializer
    permission_classes = [IsAdmin]

class AttendanceViewSet(viewsets.ModelViewSet):
    queryset = Attendance.objects.all()
    serializer_class = AttendanceSerializer
    permission_classes = [IsAdmin]

class NotificationViewSet(viewsets.ModelViewSet):
    queryset = Notification.objects.all()
    serializer_class = NotificationSerializer
    permission_classes = [IsAdmin]


class EmergencyView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        incident_types = [choice[0] for choice in Incident.INCIDENT_TYPES]
        severities = [i for i in range(1, 6)]

        sensors = Sensor.objects.all()
        cameras = Camera.objects.all()

        random_sensor = random.choice(sensors) if sensors.exists() else None
        random_camera = random.choice(cameras) if cameras.exists() else None

        incident = Incident.objects.create(
            type=random.choice(incident_types),
            description=f'Екстренне повідомленя від користувача #{random.randint(1000, 9999)}',
            severity=random.choice(severities),
            sensor=random_sensor,
            camera=random_camera,
            reported=random.choice([True, False])
        )

        return Response({
            'message': 'Інцидент створено та служби сповіщено.',
            'incident_id': incident.id,
            'type': incident.type,
            'severity': incident.severity,
            'sensor_id': incident.sensor.id if incident.sensor else None,
            'camera_id': incident.camera.id if incident.camera else None,
            'reported': incident.reported
        })



@api_view(['GET'])
def get_latest_notification(request):
    notification = Notification.objects.order_by('-date').first()
    if notification:
        data = {
            'id': notification.id,
            'type': notification.type,
            'description': notification.description,
            'date': notification.date,
        }
        return Response([data])
    else:
        return Response([], status=status.HTTP_204_NO_CONTENT)