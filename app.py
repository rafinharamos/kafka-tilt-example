import threading
import logging
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel

from lib_kafka.producer import KafkaProducer
from lib_kafka.consumer import KafkaConsumer

logging.basicConfig(
    level=logging.INFO,  
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s", 
    handlers=[logging.StreamHandler()]  
)

logger = logging.getLogger(__name__)

app = FastAPI()

BOOTSTRAP_SERVERS = "kafka:9092"
TOPIC_NAME = "test-topic"
CLIENT_ID = "testClient"

# Initialize the Producer
producer = KafkaProducer(bootstrap_servers=BOOTSTRAP_SERVERS, client_id=CLIENT_ID)

class Message(BaseModel):
    key: str
    value: str

@app.get("/")
def healt():
    logger.info("healt ok")
    return {"poc": "Working"}


@app.post("/produce/")
async def produce_message(message: Message):
    try:
        producer.produce_message(TOPIC_NAME, key=message.key, value=message.value)
        return {"status": f"Message sent successfully: {message.value}"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

# Initialize the Consumer in a diferent thread 
def start_consumer():
    def process_message(value: str):
        print(f"Received message: {value.value().decode('utf-8')}")

    consumer = KafkaConsumer(
        bootstrap_servers=BOOTSTRAP_SERVERS,
        group_id="example-group",
        topics=[TOPIC_NAME],
    )
    consumer.consume_message(process_message)

threading.Thread(target=start_consumer, daemon=True).start()