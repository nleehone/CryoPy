from component import Component
from SR830.config import *
import zmq
import time
import sys
sys.path.append('../')


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
            self.driver_socket.send_json({'METHOD': 'GET', 'CMD': 'snap_measurement', 'PARS': [1,2]})
            data = self.driver_socket.recv_json()
            self.driver_socket.send_json({'METHOD': 'GET', 'CMD': 'status', 'PARS': ''})
            status = self.driver_socket.recv_json()
            self.driver_socket.send_json({'METHOD': 'GET', 'CMD': 'standard_event_status_byte', 'PARS': ''})
            event_status = self.driver_socket.recv_json()
            
            res = {'data': data,
                   'status': status,
                   'event_status': event_status,
                   }
            print(time.time(), res)
            self.pub_socket.send_json(res)

            time.sleep(1)


if __name__ == '__main__':
    Acquirer(acquirer_port, acquirer_pub_port, driver_port).run()
