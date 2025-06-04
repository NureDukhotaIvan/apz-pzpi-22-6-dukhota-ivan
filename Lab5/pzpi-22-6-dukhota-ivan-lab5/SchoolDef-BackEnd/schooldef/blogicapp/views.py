from django.http import HttpResponse
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
from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import A4
from reportlab.lib.units import cm
from reportlab.lib.styles import getSampleStyleSheet
from reportlab.platypus import Paragraph, SimpleDocTemplate, Spacer, Table, TableStyle
from reportlab.lib import colors



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

        return Response({
            "total_sensors": total_sensors,
            "active_sensors": active_sensors,
            "sensor_coverage": round(sensor_coverage, 2),

            "total_cameras": total_cameras,
            "active_cameras": active_cameras,
            "camera_coverage": round(camera_coverage, 2),

            "total_incidents": total_incidents,
            "incident_frequency": round(incident_frequency, 2),

            "average_severity": round(avg_severity, 2),
            "normalized_severity": round(normalized_severity, 2),

            "SEI_index": round(SEI, 2)
        })


class IncidentStatisticsView(APIView):
    permission_classes = [IsAuthenticated]

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
        


class IncidentReportPDFView(APIView):
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


        response = HttpResponse(content_type='application/pdf')
        response['Content-Disposition'] = 'attachment; filename="incident_report.pdf"'
        
        doc = SimpleDocTemplate(response, pagesize=A4, rightMargin=2*cm, leftMargin=2*cm, topMargin=2*cm, bottomMargin=2*cm)
        elements = []
        styles = getSampleStyleSheet()

        elements.append(Paragraph("Incident Report", styles['Title']))
        elements.append(Spacer(1, 12))

        elements.append(Paragraph(f"Total number of incidents: <b>{total}</b>", styles['Normal']))
        elements.append(Paragraph(f"Average number of incidents per day: <b>{round(avg_count, 2)}</b>", styles['Normal']))
        elements.append(Spacer(1, 12))

        elements.append(Paragraph("Incident Categories:", styles['Heading2']))
        category_data = [["Type", "Amount"]]
        for item in categories:
            category_data.append([item['type'], item['count']])

        category_table = Table(category_data, colWidths=[8*cm, 4*cm])
        category_table.setStyle(TableStyle([
            ('BACKGROUND', (0, 0), (-1, 0), colors.grey),
            ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
            ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
            ('GRID', (0, 0), (-1, -1), 1, colors.black),
            ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
        ]))
        elements.append(category_table)
        elements.append(Spacer(1, 12))

        elements.append(Paragraph("Severity Levels:", styles['Heading2']))
        severity_data = [
            ["Min", "Max", "Avg"],
            [min_severity, max_severity, round(avg_severity, 2)]
        ]
        severity_table = Table(severity_data, colWidths=[4*cm]*3)
        severity_table.setStyle(TableStyle([
            ('BACKGROUND', (0, 0), (-1, 0), colors.lightgrey),
            ('GRID', (0, 0), (-1, -1), 1, colors.black),
            ('ALIGN', (0, 0), (-1, -1), 'CENTER')
        ]))
        elements.append(severity_table)

        doc.build(elements)
        return response