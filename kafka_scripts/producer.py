import json
import requests
from time import sleep
from kafka import KafkaProducer

try:
    producer = KafkaProducer(
                bootstrap_servers='localhost:29092',
                value_serializer=lambda v: json.dumps(v).encode('utf-8'),
                api_version=(0, 10, 1))
    for j in range(50):
        response=requests.get('http://api.open-notify.org/iss-now.json')
        data=json.loads(response.content.decode('utf-8'))
        producer.send('project_topic', value=data)
        sleep(5)
        producer.flush()
    producer.close()
except Exception as e:
    print(f"Error al enviar mensajes: {e}")
