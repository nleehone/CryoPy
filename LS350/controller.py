import zmq


class Controller(object):
    def __init__(self, command_port, acquirer_port, driver_port):
        self.context = zmq.Context()

        self.command_socket = self.context.socket(zmq.REP)
        self.command_socket.bind('tcp://*:{}'.format(command_port))

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
            print(val)
            #T = self.command_socket.recv_json()['Set T']
            #self.driver_socket.send_json({'cmd': 'set', 'T': T})
            #print("Sent")
            #self.driver_socket.recv_json()
            #print("Sent1")
            self.command_socket.send_json(val)


if __name__ == '__main__':
    Controller(5559, 5556, 5554).run()
