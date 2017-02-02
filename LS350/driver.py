import visa
import numpy as np
import instrument_example.instrument as instr
import zmq
import sys
from drivers import LS350


class Driver(object):
    def __init__(self, driver_port):
        self.context = zmq.Context()
        rm = visa.ResourceManager()
        self.LS350 = LS350(rm.open_resource('ASRL6::INSTR'))

        self.driver_socket = self.context.socket(zmq.REP)
        self.driver_socket.bind('tcp://*:{}'.format(driver_port))

    def set_temperature(self, T):
        #instrument = instr.Instrument()
        #instrument.set_temperature(T)
        pass

    def get_temperature(self):
        #instrument = instr.Instrument()
        #return instrument.get_temperature() + 10.0*(np.random.rand()*2.0 - 1.0)
        temp = self.LS350.get_temperature('A')
        print(temp)
        return temp

    def get_sens(self):
        return self.LS350.get_sensor('A')

    def set(self, command):
        {''}[command]()

    def identify(self, params):
        return self.LS350.identification_query()

    def get(self, command, params):
        return {
            'Identitfy': self.identify,
            'Temperature A': self.get_temperature,
            'Sens': self.get_sens
        }[command](params)

    def run(self):
        while True:
            command = self.driver_socket.recv_json()
            # Command:
            # {method: set/get, cmd: ()}
            if command['method'] == 'set':
                self.set(command['cmd'])
                self.set_temperature(command['T'])
                self.driver_socket.send_json({})
            elif command['method'] == 'get':
                value = self.get(command['cmd'], command['pars'])
                self.driver_socket.send_json({'T': self.get_temperature()})


if __name__ == '__main__':
    #if len(sys.argv) < 2:
    #    print("Cannot initialize the Driver without a port: python driver.py <port>")
    #    exit()

    #Driver(sys.argv[1]).run()
    Driver(5554).run()

