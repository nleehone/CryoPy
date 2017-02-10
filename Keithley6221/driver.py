from Keithley6221.config import *
import visa
import time
import sys
sys.path.append('../')
from drivers import Keithley6221Driver
from component import *


class Driver(Driver):
    """
    Commands:
    """

    def __init__(self, driver_port):
        super().__init__(driver_port)
        rm = visa.ResourceManager()
        self.Keithley6221 = Keithley6221Driver(rm.open_resource('ASRL4::INSTR'))
        print(self.Keithley6221.identify())
        self.get_commands = {
            'get_compliance': self.get_compliance,
            'get_filter_state': self.get_filter_state,
            'get_pre_math_data': self.get_pre_math_data,
            'get_post_math_data': self.get_post_math_data,
            'identify': self.identify,
            'query': self.query,
        }

        self.set_commands = {
            'set_data_elements': self.set_data_elements,
            'set_compliance': self.set_compliance,
            'set_filter_state': self.set_filter_state,
        }
        
    def query(self, pars):
        return self.Keithley6221.multi_query(pars)
        
    def write(self, pars):
        self.Keithley6221.write(pars)

    def get_compliance(self, pars):
        return self.Keithley6221.get_compliance()

    def get_filter_state(self, pars):
        return self.Keithley6221.get_filter_state()

    def get_pre_math_data(self, pars):
        return self.Keithley6221.get_pre_math_data()

    def get_post_math_data(self, pars):
        return self.Keithley6221.get_post_math_data()

    def identify(self, pars):
        return self.Keithley6221.identify()

    def set_data_elements(self, pars):
        self.Keithley6221.set_data_elements(pars)

    def set_compliance(self, pars):
        self.Keithley6221.set_compliance(pars)

    def set_filter_state(self, pars):
        self.Keithley6221.set_filter_state(pars)


if __name__ == '__main__':
    Driver(driver_port).run()
