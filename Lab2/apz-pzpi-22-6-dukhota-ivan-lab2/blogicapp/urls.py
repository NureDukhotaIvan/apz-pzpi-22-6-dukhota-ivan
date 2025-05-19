from django.urls import path
from .views import SecurityEffectivenessView, IncidentStatisticsView, BackupDatabaseView

urlpatterns = [
    path('sei/', SecurityEffectivenessView.as_view(), name='security-effectiveness'),
    path('incident-stats/', IncidentStatisticsView.as_view(), name='incident-stats'),
    path('backup/', BackupDatabaseView.as_view(), name='backup'),
]