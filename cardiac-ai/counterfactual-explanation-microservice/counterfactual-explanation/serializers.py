from rest_framework import serializers
from .models import CounterfactualExplanation


class CounterfactualExplanationSerlizer(serializers.ModelSerializer):
    class Meta:
        model = CounterfactualExplanation
        fields = '__all__'
