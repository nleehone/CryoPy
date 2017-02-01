import zmq
from threading import Thread


class DataStore(object):
    def __init__(self, command_port, acquirer_port):
        self.context = zmq.Context()

        self.acquirer_socket = self.context.socket(zmq.SUB)
        self.acquirer_socket.connect('tcp://localhost:{}'.format(acquirer_port))
        self.acquirer_socket.setsockopt_string(zmq.SUBSCRIBE, '')

        self.command_socket = self.context.socket(zmq.REP)
        self.command_socket.bind('tcp://*:{}'.format(command_port))

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
