import visa
import time
import sys
sys.path.append('../')
from drivers import LS350
from component import *


class LS350Driver(Driver):
    """Single point of communication with the instrument

    Having a common point of communication prevents multiple parts of the system from trying to access the hardware
    at the same time. This is enforced by the ZMQ command socket, which only receives one message at a time.

    It is up to the user to make sure that only one instance of the Driver is ever running.

    Driver commands:
    GET: temperature {channel} -> {channel, temperature}
    GET: identity {} -> {identity}
    GET: heater_output {output} -> {output, percent}
    GET: heater_range {output} -> {output, range}

    SET: temperature_setpoint {channel} -> {}
    """
    def __init__(self):
        super().__init__("LS350")
        rm = visa.ResourceManager()
        self.instrument = LS350(rm.open_resource('ASRL9::INSTR'))
        print(self.instrument.identify())

        self.get_commands = {
            'get_temperature': self.CMD_GET_temperature,
            'get_heater_output': self.CMD_GET_heater_output,
            'get_heater_range': self.CMD_GET_heater_range,
            'get_sens': self.CMD_GET_sens,
            'get_idn': self.CMD_GET_idn,
            'get_all': self.CMD_GET_all,
            'get_all_temperatures': self.CMD_GET_all_temperatures,
            'get_sensor': self.CMD_GET_sensor
        }

        self.set_commands = {
            'set_temperature_setpoint': self.CMD_SET_temperature_setpoint,
            'set_heater_range': self.CMD_SET_heater_range,
        }

    def CMD_SET_temperature_setpoint(self, params):
        try:
            self.instrument.set_temperature_setpoint(params['channel'], params['setpoint'])
        except KeyError as e:
            print(e)
            
    def CMD_SET_heater_range(self, params):
        try:
            self.instrument.set_heater_range(params['output'], params['range'])
        except KeyError as e:
            print(e)

    def CMD_GET_temperature(self, params):
        temp = self.instrument.get_temperature(params['channel'])
        return float(temp)

    def CMD_GET_heater_output(self, params):
        percent = self.instrument.get_heater_output(params['output'])
        return {'output': params['output'], 'percent': percent}

    def CMD_GET_heater_range(self, params):
        range = self.instrument.get_heater_range(params['output'])
        return {'output': params['output'], 'range': range}

    def CMD_GET_sens(self):
        return self.instrument.get_sensor('A')

    def CMD_GET_idn(self, params):
        return {'identity': self.instrument.identification_query()}
              
    def CMD_GET_all_temperatures(self, params):
        return self.instrument.get_all_temperature()
  
    def CMD_GET_all(self, params):
        return {'temperature': self.instrument.get_all_temperature(),
                'heater': self.instrument.get_all_heater()}

    def CMD_GET_sensor(self, params):
        return self.instrument.get_sensor(params['channel'])


if __name__ == '__main__':
    with LS350Driver() as driver:
        while True:
            pass
