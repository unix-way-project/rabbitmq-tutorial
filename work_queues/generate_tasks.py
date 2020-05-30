#!/usr/bin/env python
import pika
import sys
import json
import random

def main():
    credentials = pika.PlainCredentials('mquser', 'mquser')
    parameters = pika.ConnectionParameters('rabbitmq-lb', 5672, '/app', credentials)
    connection = pika.BlockingConnection(parameters)

    channel = connection.channel()

    channel.exchange_declare(exchange='workers', exchange_type='direct')

    channel.queue_declare(queue='worker_queue1', durable=True)

    channel.queue_bind(exchange='workers', queue="worker_queue1")

    index = 0
    while True:
        index = index + 1
        if index > 1000:
            break

        message = {
            "id": index,
            "arg_first": random.randint(1, 100),
            "arg_second": random.randint(1, 100)
        }

        channel.basic_publish(
            exchange = 'workers',
            routing_key = 'worker_queue1',
            body = json.dumps(message),
            properties = pika.BasicProperties(
                delivery_mode = 2,  # make message persistent
            ))
        print(" [x] Sent %r" % message)

    connection.close()

main()
