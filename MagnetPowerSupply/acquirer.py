from component import Component
from MagnetPowerSupply.config import *
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

        self.driver_socket.send_json({'METHOD': 'GET', 'CMD': 'set_data_elements', 'PARS': ['ALL']})
        self.driver_socket.recv_json()

    def run(self):
        while True:
            # Get the data from the instrument driver
            self.driver_socket.send_json({'METHOD': 'GET', 'CMD': 'get_pre_math_data', 'PARS': ''})
            data = self.driver_socket.recv_json()

            print(data)
            res = {
                'Reading': data[0],
                'Time': data[1],
                'Units': data[2],
                'Reading Number': data[3],
                'Source Level': data[4],
                'Compliance': data[5],
                'Avg Voltage': data[6],
            }
            print(res)
            self.pub_socket.send_multipart(b'Keithley6221', json.dumps(res).encode('utf-8'))
            #x, y = map(float, data)
            #res = {'Lock-In X': x,
            #       'Lock-In Y': y,
            #       'Valid': not (status & 4),
            #       'Status': status,
            #       'Event_status': event_status,
            #       'Time': measurement_time
            #       }
            #print(time.time(), res)
            #self.pub_socket.send_multipart([b'lock-in', json.dumps(res).encode('utf-8')])

            time.sleep(1)


if __name__ == '__main__':
    Acquirer(acquirer_port, acquirer_pub_port, driver_port).run()
