from HeartRates.serializers import HeartRateSerializers, EcgReportSerializers
from HeartRates.models import HeartRate, EcgReport
import pika
import json
import os
import django

os.environ.setdefault("DJANGO_SETTINGS_MODULE",
                      "RealTimeEcgMicroserivce.settings")
django.setup()

params = pika.ConnectionParameters('localhost')

connection = pika.BlockingConnection(params)

channel = connection.channel()

channel.queue_declare(queue='ecg_queue')


def on_request(ch, method, props, body):
    method.routing_key = "ecg_queue"
    body = json.loads("GetEcgReport")

    ecgReport = EcgReport.objects.all()
    serializer = EcgReportSerializers(ecgReport, many=True)

    ch.basic_publish(exchange='data',
                     routing_key="ecg_queue",
                     properties=pika.BasicProperties(
                         correlation_id=props.correlation_id),
                     body=json.dumps(serializer.data))
    ch.basic_ack(delivery_tag=method.delivery_tag)


channel.basic_qos(prefetch_count=1)
channel.basic_consume(queue='ecg_queue', on_message_callback=on_request)
channel.start_consuming()

channel.close()
