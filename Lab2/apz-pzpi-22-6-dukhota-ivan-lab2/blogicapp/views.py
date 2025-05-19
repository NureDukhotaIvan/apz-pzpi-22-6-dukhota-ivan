from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from actionapp import models
from userapp.permissions import IsAdmin
from userapp.models import Student
from iotapp.models import Sensor, Camera
from actionapp.models import Incident, Attendance
from datetime import date, timedelta
from django.db.models import Avg, Min, Max, Count
from django.utils.timezone import now
import datetime, os, subprocess
from django.conf import settings


class SecurityEffectivenessView(APIView):
    permission_classes = [IsAuthenticated, IsAdmin]

    def get(self, request):
        total_sensors = Sensor.objects.count()
        active_sensors = Sensor.objects.filter(status='active').count()
        total_cameras = Camera.objects.count()
        active_cameras = Camera.objects.filter(status='active').count()
        total_incidents = Incident.objects.count()
        avg_severity = Incident.objects.aggregate(avg=Avg('severity'))['avg'] or 0
        total_students = Student.objects.count()
        today = date.today()
        week_ago = today - timedelta(days=7)
        attendance = Attendance.objects.filter(date__range=(week_ago, today))
        total_attendance = attendance.count()
        present_count = attendance.filter(status='present').count()
        sensor_coverage = active_sensors / total_sensors if total_sensors else 0
        camera_coverage = active_cameras / total_cameras if total_cameras else 0
        incident_frequency = total_incidents / 30
        avg_attendance = present_count / total_attendance if total_attendance else 0
        normalized_severity = avg_severity / 10
        SEI = (
            0.25 * sensor_coverage +
            0.25 * camera_coverage +
            0.20 * (1 - incident_frequency) +
            0.20 * avg_attendance +
            0.10 * (1 - normalized_severity)
        )
        return Response({"SEI_index": round(SEI, 2)})

class IncidentStatisticsView(APIView):
    permission_classes = [IsAuthenticated, IsAdmin]

    def get(self, request):
        incidents = Incident.objects.all()
        total = incidents.count()
        categories = incidents.values('type').annotate(count=Count('id'))
        month_start = now().replace(day=1)
        month_incidents = incidents.filter(date__gte=month_start)
        avg_count = total / 30 if total else 0
        min_severity = incidents.aggregate(Min('severity'))['severity__min'] or 0
        max_severity = incidents.aggregate(Max('severity'))['severity__max'] or 0
        avg_severity = incidents.aggregate(Avg('severity'))['severity__avg'] or 0
        return Response({
            "total_incidents": total,
            "categories": list(categories),
            "avg_count_per_day": round(avg_count, 2),
            "severity": {
                "min": min_severity,
                "max": max_severity,
                "avg": round(avg_severity, 2)
            }
        })

class BackupDatabaseView(APIView):
    permission_classes = [IsAuthenticated, IsAdmin]

    def post(self, request):
        timestamp = datetime.datetime.now().strftime('%Y%m%d_%H%M%S')
        file_path = rf'D:\\SchoolDef-backup\\backup_{timestamp}.sql'
        try:
            os.environ['PGPASSWORD'] = settings.DATABASES['default']['PASSWORD']
            subprocess.run([
                'pg_dump',
                '-U', settings.DATABASES['default']['USER'],
                '-h', settings.DATABASES['default'].get('HOST', 'localhost'),
                '-F', 'c',
                settings.DATABASES['default']['NAME'],
                '-f', file_path
            ], check=True)
            return Response({"status": "success", "file": file_path})
        except Exception as e:
            return Response({"status": "error", "message": str(e)}, status=500)