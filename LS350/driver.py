import numpy as np
import instrument_example.instrument as instr
import zmq
import sys


class Driver(object):
    def __init__(self, driver_port):
        self.context = zmq.Context()

        self.driver_socket = self.context.socket(zmq.REP)
        self.driver_socket.bind('tcp://*:{}'.format(driver_port))

    def set_temperature(self, T):
        instrument = instr.Instrument()
        instrument.set_temperature(T)

    def get_temperature(self):
        instrument = instr.Instrument()
        return instrument.get_temperature() + 10.0*(np.random.rand()*2.0 - 1.0)

    def run(self):
        while True:
            command = self.driver_socket.recv_json()
            print(command)
            if command['cmd'] == 'set':
                self.set_temperature(command['T'])
                self.driver_socket.send_json({})
            elif command['cmd'] == 'get':
                self.driver_socket.send_json({'T': self.get_temperature()})


if __name__ == '__main__':
    #if len(sys.argv) < 2:
    #    print("Cannot initialize the Driver without a port: python driver.py <port>")
    #    exit()

    #Driver(sys.argv[1]).run()
    Driver(5554).run()

