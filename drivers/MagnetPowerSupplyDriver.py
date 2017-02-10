import pyvisa
from .driver import Driver


class MagnetPowerSupplyDriver(Driver):
    def __init__(self, resource):
        super().__init__(resource)

        try:
            # Try to setup the device for serial operation
            resource.baud_rate = 19200
            resource.data_bits = 8
            resource.parity = pyvisa.constants.Parity.none
            resource.stop_bits = pyvisa.constants.StopBits.one
            resource.read_termination = resource.LF
        except AttributeError:
            pass
