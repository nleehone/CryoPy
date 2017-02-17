import json
from .component import Component


class Acquirer(Component):
    def __init__(self, prefix):
        super().__init__("{}.{}".format(prefix, "acquirer"))
        self.pub_channel = self.connection.channel()
        self.pub_exchange = "{}.{}.pub".format(prefix, "acquirer")
        self.pub_channel.exchange_declare(exchange=self.pub_exchange, type="fanout")

    def publish(self, body):
        message = json.dumps(body)
        self.pub_channel.basic_publish(exchange=self.pub_exchange, routing_key='', body=message)