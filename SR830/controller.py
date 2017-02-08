from .config import *
import zmq
import sys
sys.path.append('../')
from component import Component


class Controller(Component):
    def __init__(self, command_port, acquirer_port, driver_port):
        super().__init__(command_port)

        self.acquirer_socket = self.context.socket(zmq.SUB)
        self.acquirer_socket.connect('tcp://localhost:{}'.format(acquirer_port))
        self.acquirer_socket.setsockopt_string(zmq.SUBSCRIBE, '')

        self.driver_socket = self.context.socket(zmq.REQ)
        self.driver_socket.connect('tcp://localhost:{}'.format(driver_port))

    def run(self):
        while True:
            cmd = self.command_socket.recv_json()
            self.driver_socket.send_json(cmd)
            val = self.driver_socket.recv_json()
            self.command_socket.send_json(val)


if __name__ == '__main__':
    Controller(controller_port, acquirer_pub_port, driver_port).run()
