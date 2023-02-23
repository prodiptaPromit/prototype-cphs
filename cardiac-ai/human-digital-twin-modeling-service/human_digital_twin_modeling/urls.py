from django.urls import path
from .views import DigitalTwinViewSet

urlpatterns = [
    path('HumanDigitalTwinModeling', DigitalTwinViewSet.as_view({
        'post': 'create'
    })),
]
