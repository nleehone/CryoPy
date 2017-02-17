from component.component import Component
import sys
import json
sys.path.append('../')


class Driver(Component):
    """Single point of communication with the instrument

    Having a common point of communication prevents multiple parts of the system from trying to access the hardware
    at the same time.

    It is up to the user to make sure that only one instance of the Driver is ever running.
    """
    def __init__(self, prefix):
        super().__init__("{}.{}".format(prefix, "driver"))

    def get(self, command, pars):
        try:
            return self.get_commands[command](pars)
        except Exception as e:
            print(e)

    def set(self, command, pars):
        try:
            return self.set_commands[command](pars)
        except Exception as e:
            print(e)

    def on_command(self, channel, method_frame, properties, body):
        command = json.loads(body)
        if command['METHOD'] == 'SET':
            self.set(command['CMD'], command['PARS'])
            value = {}
        elif command['METHOD'] == 'GET':
            value = self.get(command['CMD'], command['PARS'])
        else:
            raise ValueError("METHOD must be either GET or SET")
        channel.basic_publish('', routing_key=properties.reply_to, body=json.dumps(value))
