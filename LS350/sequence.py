import pika
from threading import Thread
import time
import json

prefix = "LS350"
SERVER_QUEUE = "{}.{}".format(prefix, "acquirer")
response = None

def on_recv_resp(channel, method, properties, body):
    global response
    response = body.decode('utf-8')

connection = pika.BlockingConnection(pika.ConnectionParameters('localhost'))
acquirer_channel = connection.channel()
acquirer_channel.basic_consume(on_recv_resp, queue='amq.rabbitmq.reply-to', no_ack=True)

t = Thread(target=acquirer_channel.start_consuming)
t.daemon = True
t.start()


def read_channel(channel):
    global response
    acquirer_channel.basic_publish(exchange='', routing_key=SERVER_QUEUE, body='read_' + channel, properties=pika.BasicProperties(reply_to='amq.rabbitmq.reply-to'))
    
    while response is None:
        connection.process_data_events()
    
    resp = response
    response = None
    return json.loads(resp)
    
if __name__ == '__main__':
    while True:
        t1 = time.time()
        d1 = read_channel('D')
        #a = read_channel('A')
        #b = read_channel('B')
        #c = read_channel('C')
        #d2 = read_channel('D')
        t2 = time.time()
        #print(d1, a, b, c, d2, t1, t2)
        print(d1, t1, t2)
        time.sleep(1)
        
        #write({d1, abc, d2})
