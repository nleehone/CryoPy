import pika

prefix = "LS350"
SERVER_QUEUE = "{}.{}".format(prefix, "acquirer")


def on_recv_resp(channel, method, properties, body):
    print(body)

connection = pika.BlockingConnection(pika.ConnectionParameters('localhost'))
acquirer_channel = connection.channel()
acquirer_channel.basic_consume(on_recv_resp, queue='amq.rabbitmq.reply-to', no_ack=True)
acquirer_channel.basic_publish(exchange='', routing_key=SERVER_QUEUE, body='Marco', properties=pika.BasicProperties(reply_to='amq.rabbitmq.reply-to'))
acquirer_channel.start_consuming()

#if __name__ == '__main__':
