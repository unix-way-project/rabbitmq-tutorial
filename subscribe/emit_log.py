#!/usr/bin/env python
import pika
import sys
import json
import random
import time

def main():
    credentials = pika.PlainCredentials('mqadmin', 'mqadmin')
    parameters = pika.ConnectionParameters('rabbitmq-lb', 5672, '/', credentials)
    connection = pika.BlockingConnection(parameters)

    channel = connection.channel()

    channel.exchange_declare(exchange='logs', exchange_type='fanout')

    while True:
        message = {
            "event": random.randint(1, 1000000)
        }

        channel.basic_publish(exchange='logs', routing_key='', body=json.dumps(message))
        print(" [x] Sent %r" % message)

        time.sleep(1)

    connection.close()

main()
