import pika


class RpcClient(object):
    def __init__(self, command_queue):
        self.connection = pika.BlockingConnection(pika.ConnectionParameters('localhost'))
        self.command_channel = self.connection.channel()
