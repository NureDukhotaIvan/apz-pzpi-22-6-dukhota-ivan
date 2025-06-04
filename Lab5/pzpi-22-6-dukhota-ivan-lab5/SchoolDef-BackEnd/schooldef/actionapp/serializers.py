from rest_framework import serializers
from .models import Incident, Attendance, Notification

class IncidentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Incident
        fields = '__all__'

class AttendanceSerializer(serializers.ModelSerializer):
    class Meta:
        model = Attendance
        fields = '__all__'

class NotificationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Notification
        fields = '__all__'


