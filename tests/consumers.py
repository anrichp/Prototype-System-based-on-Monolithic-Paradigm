from kafka import KafkaConsumer
import json

def con():
    consumer = KafkaConsumer('temperature',bootstrap_servers=['localhost:9092'])

    for msg in consumer:
        val = json.loads(msg.value)
        print(val["temperature:"])