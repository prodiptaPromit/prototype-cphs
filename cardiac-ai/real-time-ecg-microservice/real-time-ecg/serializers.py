from rest_framework import serializers
from .models import HeartRate, EcgReport


class HeartRateSerializers(serializers.ModelSerializer):
    class Meta:
        model = HeartRate
        fields = '__all__'


class EcgReportSerializers(serializers.ModelSerializer):
    class Meta:
        model = EcgReport
        fields = '__all__'
