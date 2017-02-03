import zmq


class Component(object):
    """Base class for all components

    All component have a command socket (REP=response) to allow other parts of the system to communicate with them.
    """
    def __init__(self, port):
        self.context = zmq.Context()
        self.command_socket = self.context.socket(zmq.REP)
        self.command_socket.bind('tcp://*:{}'.format(port))
