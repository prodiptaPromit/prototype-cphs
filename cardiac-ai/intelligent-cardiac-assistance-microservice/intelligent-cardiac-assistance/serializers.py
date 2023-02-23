from rest_framework import serializers
from .models import EcgReport


class EcgReportSerlizer(serializers.ModelSerializer):
    class Meta:
        model = EcgReport
        fields = '__all__'
