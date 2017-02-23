import pika
import json
import logging
from threading import Thread
import os 
dir_path = os.path.dirname(os.path.realpath(__file__))


class Component(object):
    """Base class for all components

    All component have a command socket (REP=response) to allow other parts of the system to communicate with them.
    """
    def __init__(self, command_queue):
        self.setup_logger()
        self.command_queue = command_queue

    def __enter__(self):
        self.logger.info("Entered context manager")

        self.connection = pika.BlockingConnection(pika.ConnectionParameters('localhost'))
        self.command_channel = self.connection.channel()
        self.command_channel.queue_declare(queue=self.command_queue, exclusive=True, auto_delete=True)
        self.command_channel.basic_consume(self.on_command, queue=self.command_queue)

        # Consume messages in a separate thread so we can continue doing operations on the main thread
        self.logger.info("Starting the command Thread")
        self.command_thread = Thread(target=self.run_command)
        self.command_thread.daemon = True
        self.command_thread.start()

        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.logger.info("Shutting down at end of context manager")
        self.connection.close()

    def run_command(self):
        try:
            self.logger.info("Start consuming on command channel")
            self.command_channel.start_consuming()
        except KeyboardInterrupt:
            self.logger.info("Stop consuming on command channel")
            self.command_channel.stop_consuming()

    def setup_logger(self):
        self.logger = logging.getLogger(type(self).__name__)
        self.logger.setLevel(logging.INFO)

        # create a file handler
        print("{}/{}.log".format(dir_path, __name__))
        handler = logging.FileHandler("{}\{}.log".format(dir_path, __name__))
        handler.setLevel(logging.INFO)

        # create a logging format
        formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
        handler.setFormatter(formatter)

        # add the handlers to the logger
        self.logger.addHandler(handler)

    def on_command(self, channel, method_frame, properties, body):
        self.logger.info('Received command: {}'.format(body))
        reply = self.process_command(body)
        self.logger.info('Sending reply: {}'.format(reply))
        self.command_channel.basic_publish('', routing_key=properties.reply_to, body=reply)

    def process_command(self, body):
        return json.dumps("Not Implemented")


if __name__ == '__main__':
    # Test the component interacting with a client
    command_queue = 'cmd_queue'
    with Component(command_queue) as comp:

        def reply(channel, method_frame, properties, body):
            print("Reply is:", body)

        c = pika.BlockingConnection(pika.ConnectionParameters('localhost'))
        ch = c.channel()
        ch.basic_consume(reply, queue='amq.rabbitmq.reply-to', no_ack=True)
        print("Sending Test command")
        ch.basic_publish(exchange='', routing_key=command_queue, body=json.dumps('Test'), properties=pika.BasicProperties(reply_to='amq.rabbitmq.reply-to'))
        print("Expecting 'Not Implemented' reply")

        try:
            ch.start_consuming()
        except KeyboardInterrupt:
            ch.stop_consuming()

        c.close()
