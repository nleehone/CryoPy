import zmq
import time
import sys
sys.path.append('../')
import json

from component import *


class LS350Acquirer(Acquirer):
    def __init__(self):
        super().__init__("LS350")
        self.driver_connection = pika.BlockingConnection(pika.ConnectionParameters('localhost'))
        self.driver_channel = self.driver_connection.channel()
        self.driver_queue = "{}.{}".format(self.prefix, "driver")
        #self.pub_socket = self.context.socket(zmq.PUB)
        #self.pub_socket.bind('tcp://*:{}'.format(pub_port))

        #self.driver_socket = self.context.socket(zmq.REQ)
        #self.driver_socket.connect('tcp://localhost:{}'.format(driver_port))
        self.driver_channel.basic_consume(self.on_response, queue='amq.rabbitmq.reply-to', no_ack=True)
        self.response = None

    def acquire(self):
        # Get the data from the instrument driver
        #measurement_time = time.time()
        #self.publish(measurement_time)
        """data = {}
        #data['temperature'] = {}
        #data['heater_output'] = {}
        #data['heater_range'] = {}
        data['Time'] = time.time()
        self.driver_socket.send_json({'METHOD': 'GET', 'CMD': 'temperature', 'PARS': {'channel': 'A'}})
        data['TempA'] = self.driver_socket.recv_json()
        self.driver_socket.send_json({'METHOD': 'GET', 'CMD': 'temperature', 'PARS': {'channel': 'B'}})
        data['TempB'] = self.driver_socket.recv_json()
        self.driver_socket.send_json({'METHOD': 'GET', 'CMD': 'sensor', 'PARS': {'channel': 'A'}})
        data['SensA'] = self.driver_socket.recv_json()
        self.driver_socket.send_json({'METHOD': 'GET', 'CMD': 'sensor', 'PARS': {'channel': 'B'}})
        data['SensB'] = self.driver_socket.recv_json()
        #self.driver_socket.send_json({'METHOD': 'GET', 'CMD': 'heater_output', 'PARS': {'output': 1}})
        #data['heater_output'][1] = self.driver_socket.recv_json()
        #self.driver_socket.send_json({'METHOD': 'GET', 'CMD': 'heater_output', 'PARS': {'output': 2}})
        #data['heater_output'][2] = self.driver_socket.recv_json()
        #self.driver_socket.send_json({'METHOD': 'GET', 'CMD': 'heater_range', 'PARS': {'output': 1}})
        #data['heater_range'][1] = self.driver_socket.recv_json()
        #self.driver_socket.send_json({'METHOD': 'GET', 'CMD': 'heater_range', 'PARS': {'output': 2}})
        #data['heater_range'][2] = self.driver_socket.recv_json()
        #self.pub_socket.send_json(data)
        #self.driver_socket.send_json({'METHOD': 'GET', 'CMD': 'all', 'PARS': ''})
        #data = self.driver_socket.recv_json()
        self.pub_socket.send_multipart([b'LS350', json.dumps(data).encode('utf-8')])

        time.sleep(0.1)"""
        
    def process_command(self, body):
        measurement_time = time.time()
        self.driver_channel.basic_publish(exchange='',
                                          routing_key=self.driver_queue,
                                          body=json.dumps({'METHOD': 'GET', 'CMD': 'get_temperature', 'PARS': {'channel': 'A'}}),
                                          properties=pika.BasicProperties(reply_to='amq.rabbitmq.reply-to'))
        resp = ""
        while self.response is None:
            self.driver_connection.process_data_events()
            resp = self.response
            self.response = None
        return json.dumps(resp)

    def on_response(self, channel, method, properties, body):
        print("Got", body)
        self.response = body


if __name__ == '__main__':
    with LS350Acquirer() as acquirer:
        while True:
            pass

