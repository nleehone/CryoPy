import pika
import logging
from threading import Thread


class Component(object):
    """Base class for all components

    All component have a command socket (REP=response) to allow other parts of the system to communicate with them.
    """
    def __init__(self, command_queue):
        self.setup_logger()
        self.connection = pika.BlockingConnection(pika.ConnectionParameters('localhost'))
        self.command_channel = self.connection.channel()
        self.command_channel.queue_declare(queue=command_queue, exclusive=True, auto_delete=True)
        self.command_channel.basic_consume(self.on_command, queue=command_queue)

        # Consume messages in a separate thread so we can continue doing operations on the main thread
        self.logger.info("Start consuming on queue {}".format(command_queue))
        p = Thread(target=self.command_channel.start_consuming)
        p.start()

    def setup_logger(self):
        self.logger = logging.getLogger(__name__)

        # create a file handler
        handler = logging.FileHandler("{}.log".format(__name__))
        handler.setLevel(logging.INFO)

        # create a logging format
        formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
        handler.setFormatter(formatter)

        # add the handlers to the logger
        self.logger.addHandler(handler)

    def on_command(self, channel, method_frame, properties, body):
        self.logger.info('Received command: {}'.format(body))
        channel.basic_publish('', routing_key=properties.reply_to, body='Not Implemented')


if __name__ == '__main__':
    # Test the component interacting with a client
    command_queue = 'cmd_queue'
    c = Component(command_queue)

    def reply(channel, method_frame, properties, body):
        print(body)

    c = pika.BlockingConnection(pika.ConnectionParameters('localhost'))
    ch = c.channel()
    ch.basic_consume(reply, queue='amq.rabbitmq.reply-to', no_ack=True)
    ch.basic_publish(exchange='', routing_key=command_queue, body='Test', properties=pika.BasicProperties(reply_to='amq.rabbitmq.reply-to'))

    ch.start_consuming()
