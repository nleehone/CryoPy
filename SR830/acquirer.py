from component import Component
from SR830.config import *
import zmq
import time
import sys
sys.path.append('../')
import json


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
            measurement_time = time.time()
            self.driver_socket.send_json({'METHOD': 'GET', 'CMD': 'snap_measurement', 'PARS': [1,2]})
            data = self.driver_socket.recv_json()
            self.driver_socket.send_json({'METHOD': 'GET', 'CMD': 'status', 'PARS': ''})
            status = self.driver_socket.recv_json()
            self.driver_socket.send_json({'METHOD': 'GET', 'CMD': 'standard_event_status_byte', 'PARS': ''})
            event_status = self.driver_socket.recv_json()

            print(data)
            print(not (status&4))
            x, y = map(float, data)
            res = {'x': x,
                   'y': y,
                   'valid': not (status & 4),
                   'status': status,
                   'event_status': event_status,
                   'time': measurement_time
                   }
            print(time.time(), res)
            self.pub_socket.send_multipart([b'lock-in', json.dumps(res).encode('utf-8')])

            time.sleep(1)


if __name__ == '__main__':
    Acquirer(acquirer_port, acquirer_pub_port, driver_port).run()
