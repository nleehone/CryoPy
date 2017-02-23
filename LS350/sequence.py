import pika
from threading import Thread
import time
import json
import h5py
import numpy as np

prefix = "LS350"
SERVER_QUEUE = "{}.{}".format(prefix, "acquirer")
response = None

file_name = 'test.hdf5'
file = h5py.File(file_name, 'w')
file.attrs['file_name'] = file_name
file.attrs['file_creation_time'] = time.strftime("%a, %d %b %Y %X +0000", time.gmtime())
file.attrs['operator'] = 'Nicholas'
file.attrs['sample'] = 'Test sample'
file.attrs['comment'] = 'Comment'

raw_data = file.create_group('raw_data')
count = 0

newtype = np.dtype([('Temp A', float),
                    ('Temp B', float),
                    ('Temp C', float),
                    ('Temp D', float),
                    ('Sens A', float),
                    ('Sens B', float),
                    ('Sens C', float),
                    ('Sens D', float),
                    ])

t_ds = raw_data.create_dataset('temperature', (0,1), maxshape=(None, len(newtype)), dtype=newtype)
t_ds.attrs['instrument'] = 'LS350'

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


def write(data):
    global count
    #rdgA, rdgB, rdgC, rdgD, sensA, sensB, sensC, sensD = data
    t_ds.resize(count+1, axis=0)
    t_ds[count] = tuple(data)
    count += 1

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
        
        write(d1)
