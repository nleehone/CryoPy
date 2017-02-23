import pika
from threading import Thread

prefix = "LS350"
SERVER_QUEUE = "{}.{}".format(prefix, "acquirer")


def on_recv_resp(channel, method, properties, body):
    print(body)

connection = pika.BlockingConnection(pika.ConnectionParameters('localhost'))
acquirer_channel = connection.channel()
acquirer_channel.basic_consume(on_recv_resp, queue='amq.rabbitmq.reply-to', no_ack=True)

t = Thread(target=acquirer_channel.start_consuming)
t.daemon = True
t.start()


def read_channel(channel):
    acquirer_channel.basic_publish(exchange='', routing_key=SERVER_QUEUE, body='read_' + channel, properties=pika.BasicProperties(reply_to='amq.rabbitmq.reply-to'))

if __name__ == '__main__':
    while True:
        d1 = read_channel('D')
        a = read_channel('A')
        b = read_channel('B')
        c = read_channel('C')
        d2 = read_channel('D')
        print(d1, a, b, c, d2)
        #write({d1, abc, d2})
