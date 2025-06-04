from django.db import models

class Sensor(models.Model):
    SENSOR_TYPES = [
        ('fire', 'Fire'),
        ('intrusion', 'Intrusion'),
        ('smoke', 'Smoke'),
        ('gas', 'Gas'),
        ('temperature', 'Temperature')
    ]
    LOCATIONS = [
        ('Math class', 'Math class'),
        ('Second Entrance', 'Second Entrance'),
        ('Security room', 'Security room'),
        ('Shelter', 'Shelter'),
        ('PE class', 'PE class'),
        ('Canteen', 'Canteen'),
        ('Main Hall', 'Main Hall'),
        ('Main Entrance', 'Main Entrance'),
        ('Concert Hall', 'Concert Hall')
    ]
    type = models.CharField(max_length=20, choices=SENSOR_TYPES)
    location = models.CharField(max_length=100, choices=LOCATIONS)
    status = models.CharField(max_length=20, choices=[('active', 'active'), ('disabled', 'disabled')])
    danger_percentage = models.FloatField()

class Camera(models.Model):
    LOCATIONS = Sensor.LOCATIONS
    location = models.CharField(max_length=100, choices=LOCATIONS)
    status = models.CharField(max_length=20, choices=[('active', 'active'), ('disabled', 'disabled')])