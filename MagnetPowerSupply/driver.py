from Keithley6221.config import *
import visa
import time
import sys
sys.path.append('../')
from drivers import MagnetPowerSupplyDriver
from component import *


class Driver(Driver):
    """
    Commands:
    """

    def __init__(self, driver_port):
        super().__init__(driver_port)
        rm = visa.ResourceManager()
        self.MagnetPowerSupply = MagnetPowerSupplyDriver(rm.open_resource('ASRL4::INSTR'))
        print(self.Keithley6221.identify())
        self.get_commands = {
            'identify': self.identify,
            'query': self.query,
        }

        self.set_commands = {
            'write': self.write,
        }
        
    def query(self, pars):
        return self.MagnetPowerSupply.multi_query(pars)
        
    def write(self, pars):
        self.MagnetPowerSupply.write(pars)

    def identify(self, pars):
        return self.MagnetPowerSupply.identify()


if __name__ == '__main__':
    Driver(driver_port).run()
