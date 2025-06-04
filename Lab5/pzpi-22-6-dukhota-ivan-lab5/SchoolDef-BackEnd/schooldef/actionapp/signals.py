from django.db.models.signals import post_save
from django.dispatch import receiver
from .models import Incident, Attendance, Notification

@receiver(post_save, sender=Incident)
def create_notification_for_incident(sender, instance, created, **kwargs):
    if created:
        Notification.objects.create(
            type='incident',
            description=f"Новий інцидент: {instance.type} Важкість інциденту: ({instance.severity})"
        )

@receiver(post_save, sender=Attendance)
def create_notification_for_attendance(sender, instance, created, **kwargs):
    if created:
        Notification.objects.create(
            type='attendance',
            description=f"Відвідуваність: {instance.student.first_name} {instance.student.last_name} — {instance.status} ({instance.date})"
        )