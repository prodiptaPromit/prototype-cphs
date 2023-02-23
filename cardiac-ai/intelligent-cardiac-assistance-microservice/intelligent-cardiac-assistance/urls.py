from django.urls import path
from .models import EcgReport
from .views import EcgReportViewSet, ArrhythmiaDetectionViewSet

urlpatterns = [
    path('ecgReports', EcgReportViewSet.as_view({
        'get': 'data'
    })),
    path('arrhythmiaDetection', ArrhythmiaDetectionViewSet.as_view({
        'post': 'data'
    })),
]
