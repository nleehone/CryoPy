import zmq
import time
import sys
sys.path.append('../')
import json

from component import Component


class Acquirer(Component):
    def __init__(self, command_port, pub_port, driver_port):
        super().__init__(command_port)
        self.pub_socket = self.context.socket(zmq.PUB)
        self.pub_socket.bind('tcp://*:{}'.format(pub_port))

        self.driver_socket = self.context.socket(zmq.REQ)
        self.driver_socket.connect('tcp://localhost:{}'.format(driver_port))

    def run(self):
        while True:
            # Get the data from the instrument driver
            data = {}
            #data['temperature'] = {}
            #data['heater_output'] = {}
            #data['heater_range'] = {}
            data['Time'] = time.time()
            self.driver_socket.send_json({'METHOD': 'GET', 'CMD': 'temperature', 'PARS': {'channel': 'A'}})
            data['TempA'] = self.driver_socket.recv_json()
            self.driver_socket.send_json({'METHOD': 'GET', 'CMD': 'temperature', 'PARS': {'channel': 'B'}})
            data['TempB'] = self.driver_socket.recv_json()
            self.driver_socket.send_json({'METHOD': 'GET', 'CMD': 'sensor', 'PARS': {'channel': 'A'}})
            data['TempA'] = self.driver_socket.recv_json()
            self.driver_socket.send_json({'METHOD': 'GET', 'CMD': 'sensor', 'PARS': {'channel': 'B'}})
            data['TempB'] = self.driver_socket.recv_json()
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

            time.sleep(0.1)


if __name__ == '__main__':
    Acquirer(5555, 5556, 5554).run()

