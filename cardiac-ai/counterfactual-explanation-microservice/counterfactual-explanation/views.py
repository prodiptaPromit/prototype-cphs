from django.shortcuts import render
from rest_framework import viewsets, status
from rest_framework.response import Response
from rest_framework.views import APIView
from .serializers import CounterfactualExplanationSerlizer
from .models import CounterfactualExplanation
import pika
import json

connection = pika.BlockingConnection(pika.ConnectionParameters('localhost'))


class CounterfactualExplanationViewSet(viewsets.ViewSet):

    # api/counterfactualExplanation
    def CounterfactualExplanation(self, request):
        counterfactualExplanations = CounterfactualExplanation.objects.all()
        serializer = CounterfactualExplanationSerlizer(
            counterfactualExplanations, many=True)

        return Response(serializer.data)
