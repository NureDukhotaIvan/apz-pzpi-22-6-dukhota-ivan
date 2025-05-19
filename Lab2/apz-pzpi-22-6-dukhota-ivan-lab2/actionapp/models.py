from django.db import models
from userapp.models import Student, Teacher
from iotapp.models import Sensor, Camera

class Incident(models.Model):
    INCIDENT_TYPES = [('fire', 'Fire'), ('intrusion', 'Intrusion'), ('smoke', 'Smoke'), ('gas', 'Gas'), ('temperature', 'Temperature')]
    type = models.CharField(max_length=20, choices=INCIDENT_TYPES)
    description = models.TextField()
    severity = models.IntegerField(choices=[(i, str(i)) for i in range(1, 6)])
    date = models.DateTimeField(auto_now_add=True)
    sensor = models.ForeignKey(Sensor, on_delete=models.SET_NULL, null=True, blank=True)
    camera = models.ForeignKey(Camera, on_delete=models.SET_NULL, null=True, blank=True)
    reported = models.BooleanField(default=False)

class Attendance(models.Model):
    student = models.ForeignKey(Student, on_delete=models.CASCADE, null=True)
    teacher = models.ForeignKey(Teacher, on_delete=models.SET_NULL, null=True)
    date = models.DateField()
    status = models.CharField(max_length=10, choices=[('present', 'Present'), ('absent', 'Absent')])

class Notification(models.Model):
    TYPE_CHOICES = [('incident', 'Incident'), ('attendance', 'Attendance')]
    type = models.CharField(max_length=20, choices=TYPE_CHOICES)
    date = models.DateTimeField(auto_now_add=True)
    description = models.TextField()