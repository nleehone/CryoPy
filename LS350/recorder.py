import zmq


class Recorder(object):
    def __init__(self, command_port, datastore_port):
        self.context = zmq.Context()

        self.data_socket = self.context.socket(zmq.REQ)
        self.data_socket.connect('tcp://localhost:{}'.format(datastore_port))

        self.command_socket = self.context.socket(zmq.REP)
        self.command_socket.bind('tcp://*:{}'.format(command_port))

    def run(self):
        while True:
            self.data_socket.send(b"")
            message = self.data_socket.recv()
            print(message)


if __name__ == '__main__':
    Recorder(5558, 5557).run()
