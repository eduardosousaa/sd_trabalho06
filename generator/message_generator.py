#!/usr/bin/env python3
import os
import time
import random
import pika

RABBIT_HOST = os.getenv('RABBIT_HOST', 'rabbitmq')
EXCHANGE = 'images'
IMAGES_DIR = 'images'
PUBLISH_RATE = float(os.getenv('PUBLISH_RATE', '5.0'))

def wait_for_rabbit():
    while True:
        try:
            conn = pika.BlockingConnection(pika.ConnectionParameters(RABBIT_HOST))
            print("▶ Conectado ao RabbitMQ")
            return conn
        except pika.exceptions.AMQPConnectionError:
            print("⏳ RabbitMQ não pronto, aguardando 1s...")
            time.sleep(1)

def load_images():
    images = {'face': [], 'team': []}
    for typ in images:
        folder = os.path.join(IMAGES_DIR, typ)
        if os.path.isdir(folder):
            for fn in os.listdir(folder):
                path = os.path.join(folder, fn)
                if os.path.isfile(path):
                    images[typ].append(fn)
    return images

def main():
    conn = wait_for_rabbit()
    ch   = conn.channel()
    ch.exchange_declare(exchange=EXCHANGE, exchange_type='topic', durable=True)

    images = load_images()
    if not any(images.values()):
        print("⚠️  Nenhuma imagem encontrada em images/face ou images/team")
        return

    interval = 1.0 / PUBLISH_RATE
    try:
        while True:
            key = random.choice([k for k,v in images.items() if v])
            fn  = random.choice(images[key])
            ch.basic_publish(
                exchange=EXCHANGE,
                routing_key=key,
                body=fn.encode()
            )
            print(f"✉ Published {key} → {fn}")
            time.sleep(interval)
    except KeyboardInterrupt:
        print("\n👋 Parando generator...")
    finally:
        conn.close()

if __name__ == '__main__':
    main()
