from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import LogEntryViewSet, import_logs, detect_anomalies

router = DefaultRouter()
router.register(r'logs', LogEntryViewSet)

urlpatterns = [
    path('', include(router.urls)),
    path('logs/import/', import_logs, name='import_logs'),
    path('logs/anomalies/', detect_anomalies, name='detect_anomalies'),
]