#!/usr/bin/env python3
import os
import time
import pika

RABBIT_HOST = os.getenv('RABBIT_HOST', 'rabbitmq')
EXCHANGE = 'images'
QUEUE = 'queue_team'
ROUTING_KEY = 'team'

def wait_for_rabbit():
    while True:
        try:
            conn = pika.BlockingConnection(pika.ConnectionParameters(RABBIT_HOST))
            print("▶ [TEAM] Conectado ao RabbitMQ")
            return conn
        except pika.exceptions.AMQPConnectionError:
            print("⏳ [TEAM] RabbitMQ não pronto, aguardando 1s...")
            time.sleep(1)

def main():
    conn = wait_for_rabbit()
    ch = conn.channel()
    ch.exchange_declare(exchange=EXCHANGE, exchange_type='topic', durable=True)
    ch.queue_declare(queue=QUEUE, durable=True)
    ch.queue_bind(exchange=EXCHANGE, queue=QUEUE, routing_key=ROUTING_KEY)

    print("⚽ Consumer TEAM aguardando mensagens…")
    def callback(ch, method, props, body):
        print(f"📥 [TEAM] {body.decode()}")
        ch.basic_ack(delivery_tag=method.delivery_tag)

    ch.basic_qos(prefetch_count=1)
    ch.basic_consume(queue=QUEUE, on_message_callback=callback)
    ch.start_consuming()

if __name__ == '__main__':
    main()
