from django.shortcuts import render
from rest_framework import viewsets, status
from rest_framework.response import Response
from rest_framework.views import APIView
from .serializers import HeartRateSerializers, EcgReportSerializers
from .models import HeartRate, EcgReport

import pika
import json
import argparse
import load as Load
import train as Train
import predict as Predict
import consumer
import pika
import json
import os
import django
import uuid

os.environ.setdefault("DJANGO_SETTINGS_MODULE",
                      "RealTimeEcgMicroserivce.settings")
django.setup()

connection = pika.BlockingConnection(pika.ConnectionParameters('localhost'))


class HeartRateViewSet(viewsets.ViewSet):
    load = Load()
    train = Train()
    predict = Predict()
    parserTrain = argparse.ArgumentParser()
    parserPredict = argparse.ArgumentParser()

    # api/HeartRateData
    def HeartRateData(self, request):
        heartRate = HeartRate.objects.all()
        serializer = HeartRateSerializers(heartRate, many=True)

        try:
            preproc = load.Preproc(*load.load_dataset(serializer.data))

            parser = argparse.ArgumentParser()
            parser.add_argument("config_file", help="path to config file")
            parser.add_argument(
                "--experiment", "-e", help="tag with experiment name", default="default")

            args = parser.parse_args()
            params = json.load(preproc)
            train.train(args, params)

            parser = argparse.ArgumentParser()
            parser.add_argument("data_json", help="path to data json")
            parser.add_argument("model_path", help="path to model")

            args = parser.parse_args()
            probs = predict.predict(args.data_json, args.model_path)

            ecgReport = EcgReport(probs)
            serializer = EcgReportSerializers(ecgReport, many=True)

            connection = pika.BlockingConnection(
                pika.ConnectionParameters(host='localhost'))
            channel = connection.channel()
            channel.queue_declare(queue='ecg_queue')
            channel.basic_publish(
                exchange='data', routing_key='ecg_queue', body=serializer.data)
            channel.basic_ack(delivery_tag=method.delivery_tag)
            channel.basic_qos(prefetch_count=1)
            channel.basic_consume(
                queue='ecg_queue', on_message_callback=on_request)
            channel.start_consuming()
            connection.close()

        except Exception as error:
            return Response(error)
