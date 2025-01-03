import logging

logging.basicConfig(level=logging.INFO)

from confluent_kafka import Producer

class KafkaProducer:
    def __init__(self, bootstrap_servers, client_id):
        self.producer = Producer({
            'bootstrap.servers': bootstrap_servers,
            'client.id': client_id,
        })

    def produce_message(self, topic, key, value, callback=None):
        self.producer.produce(topic, key=key, value=value, callback=callback)

    def flush(self):
        self.producer.flush()
