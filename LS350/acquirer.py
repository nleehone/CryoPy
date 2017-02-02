import zmq
import time


class Acquirer(object):
    def __init__(self, command_port, pub_port, driver_port):
        self.context = zmq.Context()

        self.pub_socket = self.context.socket(zmq.PUB)
        self.pub_socket.bind('tcp://*:{}'.format(pub_port))

        self.driver_socket = self.context.socket(zmq.REQ)
        self.driver_socket.connect('tcp://localhost:{}'.format(driver_port))

        self.command_socket = self.context.socket(zmq.REP)
        self.command_socket.bind('tcp://*:{}'.format(command_port))

    def run(self):
        while True:
            # Get the data from the instrument driver
            self.driver_socket.send_json({'METHOD': 'GET', 'CMD': 'temperature', 'PARS': {'channel': 'A'}})
            temp = self.driver_socket.recv_json()

            # Publish the data for other components to use
            self.pub_socket.send_json(temp)

            time.sleep(0.01)


if __name__ == '__main__':
    Acquirer(5555, 5556, 5554).run()

