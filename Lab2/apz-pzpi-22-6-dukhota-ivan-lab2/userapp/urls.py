from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import *

router = DefaultRouter()
router.register(r'users', UserViewSet)
router.register(r'students', StudentViewSet)
router.register(r'parents', ParentViewSet)
router.register(r'teachers', TeacherViewSet)
router.register(r'create-student', StudentCreateViewSet, basename='create-student')
router.register(r'create-parent', ParentCreateViewSet, basename='create-parent')
router.register(r'create-teacher', TeacherCreateViewSet, basename='create-teacher')

urlpatterns = [
    path('', include(router.urls)),
]
