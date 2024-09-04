from datetime import datetime
import os
import json
import pika
import logging
import logging_loki

class Forwarder():
    def __init__(self, loki_host, loki_port, rabbit_host, rabbit_port, rabbit_username, rabbit_password, rabbit_event_queue, application_name):
        handler = logging_loki.LokiHandler(
            url=f'http://{loki_host}:{loki_port}/loki/api/v1/push',
            tags={
                'application': application_name
            },
            version='1',
        )
        self.logger = logging.getLogger('loki')
        self.logger.addHandler(handler)

        credentials=pika.PlainCredentials(rabbit_username, rabbit_password)
        connection = pika.BlockingConnection(pika.ConnectionParameters(rabbit_host, port=rabbit_port, credentials=credentials))
        self.channel = connection.channel()

        self.channel.basic_consume(queue=rabbit_event_queue, on_message_callback=self.callback)

    def start(self):
        self.channel.start_consuming()

    def callback(self, ch, method, properties, body):
        print(method)
        self.logger.error(f'Logged at {datetime.fromtimestamp(properties.timestamp)}: action {method.routing_key}. Details: {properties.headers}', extra={
            'tags': {
                'exchange': method.exchange,
                'action': method.routing_key,
            }
        })
        ch.basic_ack(delivery_tag = method.delivery_tag)

if __name__ == '__main__':
    forwarder = Forwarder(
        loki_host=os.getenv('FORWARDER_LOKI_HOST', 'localhost'),
        loki_port=os.getenv('FORWARDER_LOKI_PORT', '3100'),
        rabbit_host=os.getenv('FORWARDER_RABBIT_HOST', 'localhost'),
        rabbit_port=os.getenv('FORWARDER_RABBIT_PORT', '5672'),
        rabbit_username=os.getenv('FORWARDER_RABBIT_USERNAME', 'admin'),
        rabbit_password=os.getenv('FORWARDER_RABBIT_PASSWORD', 'admin'),
        rabbit_event_queue=os.getenv('FORWARDER_RABBIT_QUEUE', 'event_queue'),
        application_name=os.getenv('FORWARDER_APPLICATION_NAME', 'rabbitmq-loki-forwarder')
    )
    forwarder.start()