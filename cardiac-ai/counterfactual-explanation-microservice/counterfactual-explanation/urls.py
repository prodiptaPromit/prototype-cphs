
# from django.contrib import admin
from django.urls import path
from .models import CounterfactualExplanation
from .views import CounterfactualExplanationViewSet

urlpatterns = [
    path('counterfactualExplanations', CounterfactualExplanationViewSet.as_view({
        'get': 'CounterfactualExplanations',
    }))
]
