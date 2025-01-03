import logging
from confluent_kafka import Consumer

logging.basicConfig(level=logging.INFO)

class KafkaConsumer:
    def __init__(self, bootstrap_servers, group_id, topics):
        self.consumer = Consumer({
            'bootstrap.servers': bootstrap_servers,
            'group.id': group_id,
            'auto.offset.reset': 'earliest',
        })
        self.consumer.subscribe(topics)

    def consume_message(self, callback, timeout=1.0):
        while True:
            msg = self.consumer.poll(timeout)
            if msg:
                logging.info(f"Message consumed: {msg.value().decode('utf-8')}")
                callback(msg)

    def close(self):
        self.consumer.close()
