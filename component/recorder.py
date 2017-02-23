from component.component import Component
import sys
import json
sys.path.append('../')


class Recorder(Component):
    def __init__(self, prefix):
        super().__init__("{}.{}".format(prefix, "recorder"))

    def __enter__(self):
        super().__enter__()

        self.acquirer_channel = self.connection.channel()
        result = self.acquirer_channel.queue_declare(exclusive=True)
        queue_name = result.method.queue

        acquirer_exchange = "{}.{}.pub".format(self.prefix, "acquirer")
        self.acquirer_channel.queue_bind(exchange=acquirer_exchange, queue=queue_name)

        self.acquirer_channel.basic_consume(self.got_data, queue=queue_name, no_ack=True)

    def got_data(self, channel, method, properties, body):
        print(body)