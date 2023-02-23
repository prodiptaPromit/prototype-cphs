
from django.urls import path
from .models import HeartRate
from .views import HeartRateViewSet

urlpatterns = [
    path('HeartRateData', HeartRateViewSet.as_view({
        'get': 'list'
    })),
]
