from CounterfactualExplanations.serializers import CounterfactualExplanationSerlizer
from CounterfactualExplanations.models import CounterfactualExplanation
import pika
import json
import os
import django

os.environ.setdefault("DJANGO_SETTINGS_MODULE",
                      "CounterfactualExplanationMicroserivce.settings")
django.setup()


params = pika.ConnectionParameters('localhost')

connection = pika.BlockingConnection(params)

channel = connection.channel()

channel.queue_declare(queue='io_queue')


def on_request(ch, method, props, body):
    body = json.loads(body)
    if method.routing_key == "io_queue" and body == "TrainedModel":
        ch.basic_publish(exchange='',
                         routing_key=props.reply_to,
                         properties=pika.BasicProperties(
                             correlation_id=props.correlation_id),
                         body=json.dumps(serializer.data))
        ch.basic_ack(delivery_tag=method.delivery_tag)
    elif method.routing_key == "io_queue" and body["Id"]:
        ch.basic_publish(exchange='',
                         routing_key=props.reply_to,
                         properties=pika.BasicProperties(
                             correlation_id=props.correlation_id),
                         body=finaldata)
        ch.basic_ack(delivery_tag=method.delivery_tag)


channel.basic_qos(prefetch_count=1)
channel.basic_consume(queue='io_queue', on_message_callback=on_request)
channel.start_consuming()

channel.queue_declare(queue='cfe_queue')


def on_request(ch, method, props, body):
    method.routing_key = "cfe_queue"
    body = json.loads("CounterfactualExplanations")

    counterfactualExplanation = CounterfactualExplanation.objects.all()
    serializer = CounterfactualExplanationSerlizer(
        counterfactualExplanation, many=True)

    ch.basic_publish(exchange='data',
                     routing_key="cfe_queue",
                     properties=pika.BasicProperties(
                         correlation_id=props.correlation_id),
                     body=json.dumps(serializer.data))
    ch.basic_ack(delivery_tag=method.delivery_tag)


channel.basic_qos(prefetch_count=1)
channel.basic_consume(queue='cfe_queue', on_message_callback=on_request)
channel.start_consuming()

channel.close()
