import pyvisa
from .driver import Driver


class Keithley6221Driver(Driver):
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

    def set_data_elements(self, elements):
        """
        FORMat:ELEMents <item list>
        Specify which elements are included in the data string returned from "Read commands"

        Valid elements:
         READing = Reading (Delta, Pulse Delta, or Differential Conductance). Overflow and NaN are returned as +9.9E37
         TSTamp = Timestamp of the measurement
         UNITs = Measurement units
         RNUMber = Reading number
         SOURce = Current source level
         COMPliance = State of compliance. If in compliance, "T" (or 1 if in double data format) is returned.
                If not in compliance "F" (or 0 if in double data format) is returned.
         AVOLtage = Average voltage (Differential Conductance)
         ALL = Include all the above elements
         DEFault = Includes READing and TSTamp only

         The elements parameter should be a list of strings
        """
        self.write("FORM:ELEM {}".format(",".join(elements)))

    def get_pre_math_data(self):
        """
        SENSe:DATA:FRESh?

        Read the latest pre-math reading. The return reading will be filtered if the averaging filter is enabled.
        Once a reading is returned, it cannot be returned again (due to the FRESh command). This guarantees that
        each reading gets returned only once. If a new (fresh) reading is not available when SENS:DATA:FRES? is sent,
        error -230 Data corrupt or stale will occur.
        """
        return self.query("SENS:DATA:FRES")

    def get_post_math_data(self):
        """
        CALCulate:DATA:FRESh?

        Read the latest post-math reading. The return reading will be filtered if the averaging filter is enabled.
        Once a reading is returned, it cannot be returned again (due to the FRESh command). This guarantees that
        each reading gets returned only once. If a new (fresh) reading is not available when SENS:DATA:FRES? is sent,
        error -230 Data corrupt or stale will occur.
        """
        return self.query("CALC:DATA:FRES")

