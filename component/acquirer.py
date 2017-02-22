import json
from threading import Thread
from .component import Component


class Acquirer(Component):
    def __init__(self, prefix):
        super().__init__("{}.{}".format(prefix, "acquirer"))
        self.prefix = prefix

    def __enter__(self):
        super().__enter__()
        self.publisher_channel = self.connection.channel()
        self.publisher_exchange = "{}.{}.pub".format(self.prefix, "acquirer")
        self.publisher_channel.exchange_declare(exchange=self.publisher_exchange, type="fanout")

        self.logger.info("Starting the publisher Thread")
        self.publisher_thread = Thread(target=self.run_publisher)
        self.publisher_thread.daemon = True
        self.publisher_thread.start()

    def run_publisher(self):
        while True:
            self.acquire()
        #try:
        #    self.logger.info("Start consuming on publisher channel")
        #    self.publisher_channel.start_consuming()
        #except KeyboardInterrupt:
        #    self.logger.info("Stop consuming on publisher channel")
        #    self.publisher_channel.stop_consuming()

    def publish(self, body):
        message = json.dumps(body)
        self.logger.info('Publishing: {}'.format(message))
        self.publisher_channel.basic_publish(exchange=self.publisher_exchange, routing_key='', body=message)

    def acquire(self):
        raise NotImplementedError