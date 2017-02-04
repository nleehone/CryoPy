import visa
import time
import numpy as np
import zmq
import sys
sys.path.append('../')
from drivers import LS350
from component import *


class Driver(Component):
    """Single point of communication with the instrument

    Having a common point of communication prevents multiple parts of the system from trying to access the hardware
    at the same time. This is enforced by the ZMQ command socket, which only receives one message at a time.

    It is up to the user to make sure that only one instance of the Driver is ever running.
    """
    def __init__(self, driver_port):
        super().__init__(driver_port)
        rm = visa.ResourceManager()
        self.LS350 = LS350(rm.open_resource('ASRL6::INSTR'))

    def set_temperature_setpoint(self, params):
        try:
            self.LS350.set_temperature_setpoint(params['channel'], params['setpoint'])
        except KeyError as e:
            print(e)

    def get_temperature(self, params):
        temp = self.LS350.get_temperature(params['channel'])
        return {'channel': params['channel'], 'temperature': temp}

    def get_sens(self):
        return self.LS350.get_sensor('A')

    def set(self, command, params):
        try:
            {
                'temperature_setpoint': self.set_temperature_setpoint
             }[command](params)
        except Exception as e:
            print(e)

    def get_idn(self, params):
        return self.LS350.identification_query()

    def get(self, command, params):
        try:
            return {
                'identify': self.get_idn,
                'temperature': self.get_temperature,
                #'sensor': self.get_sensor,
                'sens': self.get_sens
            }[command](params)
        except Exception as e:
            print(e)

    def run(self):
        while True:
            command = self.command_socket.recv_json()
            time.sleep(0.05)
            if command['METHOD'] == 'SET':
                self.set(command['CMD'], command['PARS'])
                value = {}
            elif command['METHOD'] == 'GET':
                value = self.get(command['CMD'], command['PARS'])
            self.command_socket.send_json(value)


if __name__ == '__main__':
    #if len(sys.argv) < 2:
    #    print("Cannot initialize the Driver without a port: python driver.py <port>")
    #    exit()

    #Driver(sys.argv[1]).run()
    Driver(5554).run()

