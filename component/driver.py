from component.component import Component
import sys
sys.path.append('../')


class Driver(Component):
    """Single point of communication with the instrument

    Having a common point of communication prevents multiple parts of the system from trying to access the hardware
    at the same time. This is enforced by the ZMQ command socket, which only receives one message at a time.

    It is up to the user to make sure that only one instance of the Driver is ever running.
    """
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

    def run(self):
        while True:
            command = self.command_socket.recv_json()
            if command['METHOD'] == 'SET':
                self.set(command['CMD'], command['PARS'])
                value = {}
            elif command['METHOD'] == 'GET':
                value = self.get(command['CMD'], command['PARS'])
            self.command_socket.send_json(value)
