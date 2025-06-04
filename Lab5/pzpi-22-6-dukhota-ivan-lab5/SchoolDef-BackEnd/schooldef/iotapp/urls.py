from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import SensorViewSet, CameraViewSet

router = DefaultRouter()
router.register(r'sensors', SensorViewSet)
router.register(r'cameras', CameraViewSet)

urlpatterns = [
    path('', include(router.urls)),
]