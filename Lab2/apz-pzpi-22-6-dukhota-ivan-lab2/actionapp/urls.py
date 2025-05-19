from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import IncidentViewSet, AttendanceViewSet, NotificationViewSet

router = DefaultRouter()
router.register(r'incidents', IncidentViewSet)
router.register(r'attendance', AttendanceViewSet)
router.register(r'notifications', NotificationViewSet)

urlpatterns = [
    path('', include(router.urls)),
]