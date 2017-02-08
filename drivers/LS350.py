import pyvisa
from enum import Enum
from .driver import Driver


class Temperature(Enum):
    K = 1
    C = 2


class LS350(Driver):
    def __init__(self, resource):
        super().__init__(resource)

        try:
            # Try to setup the device for serial operation
            resource.baud_rate = 57600
            resource.data_bits = 7
            resource.parity = pyvisa.constants.Parity.odd
        except AttributeError:
            pass

    def check_channel(self, channel):
        if channel not in ['A', 'B', 'C', 'D']:
            raise ValueError('The channel letter must be specified. Valid values are ["A", "B", "C", "D"].')

    def clear_interface(self):
        """
        *CLS

        Clears the bits in the Status Byte Register, Standard Event Status Register, and Operation Event Register, and
        terminates all pending operations. Clears the interface, but not the controller. The related controller command
        is *RST.
        """
        self.resource.write("*CLS")

    def identification_query(self):
        """
        *IDN?

        Get the identification information for this instrument

        Returned:
        <manufacturer>,<model>,<instrument serial>/<option serial>,<firmware version>[term]

        Format: s[4],s[8],s[7]/s[7],n.n
        <manufacturer> Manufacturer ID
        <model> Instrument model number
        <instrument serial> Instrument serial number
        <option card serial> Option card serial number
        <firmware version> Instrument firmware version

        Example
        LSCI,MODEL350,1234567/1234567,1.0
        """
        val = self.resource.query("*IDN?")
        return val

    def reset_instrument(self):
        """
        *RST

        Sets controller parameters to power-up settings.
        """
        self.resource.write("*RST")

    def get_heater_output(self, output):
        """
        HTR? <output> (for output 1, 2)
        AOUT? <output> (for outputs 3, 4)
        """
        if output in [1, 2]:
            return float(self.resource.query("HTR? {}".format(output)))
        elif output in [3, 4]:
            return float(self.resource.query("AOUT? {}".format(output)))
        # Output not valid: return a negative number
        return -1

    def get_heater_range(self, output):
        """
        RANGE? <output>
        """
        return int(self.resource.query("RANGE? {}".format(output)))

    def set_heater_range(self, output, range):
        """
        RANGE <output>,<range>
        """
        self.resource.write("RANGE {},{}".format(output, range))

    def get_temperature(self, channel, units=Temperature.K, sensor=False):
        """
        Get the temperature of a single channel.

        units: The temperature units (either K, or C)
        sensor (bool): Also return the sensor value in sensor units?
        """
        self.check_channel(channel)

        if units == Temperature.K:
            command = "KRDG? {channel};"
        else:
            command = "CRDG? {channel};"

        if sensor:
            command += "SRDG? {channel};"

        return self.resource.query(command.format(channel=channel))

    def get_temperatures(self, channels, units=Temperature.K, sensor=False):
        """
        Get the temperature of multiple channels

        units: The temperature units (either K, or C)
        sensor (bool): Also return the sensor value in sensor units?
        """
        command = ""

        for channel in channels:
            self.check_channel(channel)

            if units == Temperature.K:
                command += "KRDG? {channel};"
            else:
                command += "CRDG? {channel};"

            if sensor:
                command += "SRDG? {channel};"
            command = command.format(channel)

        return self.resource.query(command)

    def get_sensor(self, channel):
        """
        Get the sensor value of a channel
        """
        self.check_channel(channel)
        return self.resource.query("SRDG? {channel}".format(channel=channel))

    def get_sensors(self, channels):
        """
        Get the sensor value of multiple channels
        """
        command = ''
        for channel in channels:
            self.check_channel(channel)
            command += "SRDG? {channel};".format(channel=channel)
        return self.resource.query(command)

    def set_temperature_setpoint(self, channel, T):
        channel = {'A': 1, 'B': 2, 'C': 3, 'D': 4}[channel]
        command = "SETP {channel},{value}".format(channel=channel, value=T)
        self.resource.write(command)
        
    def get_all_temperature(self):
        command = "RDGST?A;RDGST?B;RDGST?C;RDGST?D;" + \
                    "KRDG?A;KRDG?B;KRDG?C;KRDG?D;" + \
                    "SRDG?A;SRDG?B;SRDG?C;SRDG?D;" + \
                    "SETP?1;SETP?2;SETP?3;SETP?4"
                    
        return self.resource.query(command)
        
    def get_all_heater(self):
        command = "HTRST?1;HTRST?2;" + \
                    "RANGE?1;RANGE?2;RANGE?3;RANGE?4;" + \
                    "HTR?1;HTR?2;AOUT?3;AOUT?4;" + \
                    "MOUT?1;MOUT?2;MOUT?3;MOUT?4;" + \
                    "PID?1;PID?2;PID?3;PID?4"
                    
        return self.resource.query(command)