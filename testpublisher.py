import pika
import json
connection = pika.BlockingConnection(
    pika.ConnectionParameters(host='localhost'))
channel = connection.channel()

channel.queue_declare(queue='ms_exchange')

dictionary = {
    "unit_id": "A1",
    "timestamp": "2023-06-02 08:37:23",
    "direction": "out"
}

json_string = json.dumps(dictionary)

channel.basic_publish(exchange='', routing_key='ms_exchange', body=json_string)
print(" [x] Message Sent")
connection.close()