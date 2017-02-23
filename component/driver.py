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
        except Exception:
            self.logger.error('Invalid CMD: {}'.format(command), exc_info=True)

    def set(self, command, pars):
        try:
            return self.set_commands[command](pars)
        except Exception:
            self.logger.error('Invalid CMD: {}'.format(command), exc_info=True)

    def process_command(self, body):
        command = json.loads(body.decode('utf-8'))
        print(command)
        if command['METHOD'] == 'SET':
            self.set(command['CMD'], command['PARS'])
            reply = ""
        elif command['METHOD'] == 'GET':
            reply = self.get(command['CMD'], command['PARS'])
            print(reply, type(reply))
        else:
            reply = "Invalid METHOD: METHOD must be either GET or SET"
            self.logger.warning(reply)
        rep = json.dumps(reply)
        print(rep)
        return rep
