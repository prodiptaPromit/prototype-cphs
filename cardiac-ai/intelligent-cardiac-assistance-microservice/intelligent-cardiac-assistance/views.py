from django.shortcuts import render
from rest_framework import viewsets, status
from rest_framework.response import Response
from rest_framework.views import APIView
from .serializers import EcgReportSerlizer
from .models import EcgReport
from classify import Classifier
from predict import predict
from prep import prep
from train import train

import pika
import json

connection = pika.BlockingConnection(pika.ConnectionParameters('localhost'))


class ArrhythmiaDetectionViewSet(APIView):

    classifier = Classifier()
    predict = predict()
    prep = prep()
    train = train()

    # api/arrhythmiaDetection
    def post(self, request, format=None):
        ecgReport = EcgReport.objects.all()
        serializer = EcgReportSerlizer(ecgReport, many=True)

        record_name = request.data.get('mitdb/100')
        labels = classifier.load_data(record_name)
        signal = prep.ProcessEcgSignals(serializer.data)
        train.TrainModel()

        if predict.PredictArrhythmia():
            classifier.fit(signal, labels)
            predictions = classifier.predict(signal)
        else:
            predictions = "No Arrhythmia Detected."

        return Response(predictions, status=status.HTTP_200_OK)


class EcgReportViewSet(viewsets.ViewSet):

    # api/ecgReports
    def get(self, request):
        ecgReport = EcgReport.objects.all()
        serializer = EcgReportSerlizer(ecgReport, many=True)
        return Response(serializer.data)
