import zmq
from threading import Thread

from component import Component


class DataStore(Component):
    def __init__(self, command_port, acquirer_port):
        super().__init__(command_port)
        self.acquirer_socket = self.context.socket(zmq.SUB)
        self.acquirer_socket.connect('tcp://localhost:{}'.format(acquirer_port))
        self.acquirer_socket.setsockopt_string(zmq.SUBSCRIBE, '')

        Thread(target=self.run_command).start()

    def run(self):
        while True:
            message = self.acquirer_socket.recv()
            print(message)

    def run_command(self):
        while True:
            message = self.command_socket.recv()
            print(message)
            self.command_socket.send(b"")


if __name__ == '__main__':
    DataStore(5557, 5556).run()
