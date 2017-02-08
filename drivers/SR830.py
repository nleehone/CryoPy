import pyvisa
from enum import IntEnum, unique
from .driver import Driver


@unique
class Sensitivity(IntEnum):
    S_2nVfA = 0
    S_5nVfA = 1
    S_10nVfA = 2
    S_20nVfA = 3
    S_50nVfA = 4
    S_100nVfA = 5
    S_200nVfA = 6
    S_500nVfA = 7
    S_1uVpA = 8
    S_2uVpA = 9
    S_5uVpA = 10
    S_10uVpA = 11
    S_20uVpA = 12
    S_50uVpA = 13
    S_100uVpA = 14
    S_200uVpA = 15
    S_500uVpA = 16
    S_1mVnA = 17
    S_2mVnA = 18
    S_5mVnA = 19
    S_10mVnA = 20
    S_20mVnA = 21
    S_50mVnA = 22
    S_100mVnA = 23
    S_200mVnA = 24
    S_500mVnA = 25
    S_1VuA = 26


@unique
class TimeConstant(IntEnum):
    TC_10us = 0
    TC_30us = 1
    TC_100us = 2
    TC_300us = 3
    TC_1ms = 4
    TC_3ms = 5
    TC_10ms = 6
    TC_30ms = 7
    TC_100ms = 8
    TC_300ms = 9
    TC_1s = 10
    TC_3s = 11
    TC_10s = 12
    TC_30s = 13
    TC_100s = 14
    TC_300s = 15
    TC_1ks = 16
    TC_3ks = 17
    TC_10ks = 18
    TC_30ks = 19


class SR830(Driver):
    def __init__(self, resource):
        super().__init__(resource)

        try:
            # Try to setup the device for serial operation
            resource.baud_rate = 57600
            resource.data_bits = 7
            resource.parity = pyvisa.constants.Parity.odd
        except AttributeError:
            pass

    def get_phase(self):
        """
        PHAS?
        Queries the reference phase shift
        """
        return float(self.query("PHAS?"))

    def set_phase(self, phase):
        """
        PHAS {phase}

        Sets the reference phase shift. Phases are rounded by the SR830 to 0.01 degrees.
        Valid phases are -360 <= phase <= 729.99. The input phase will be clamped to range value.
        Phases are wrapped at +/-180 degrees by the SR830. For example, specifying a phase of 541.0 will
        set the phase to -179.00 degrees.
        """
        if phase < -360:
            phase = 360
        elif phase > 729.99:
            phase = 729.99
        self.write("PHAS {}".format(phase))

    def get_reference_source(self):
        """
        FMOD?
        Query the reference source. External => 0, Internal =>1
        """
        return int(self.query("FMOD?"))

    def set_reference_source(self, i):
        """
        FMOD {i}
        Set the reference source. External => 0, Internal => 1
        """
        self.write("FMOD {}".format(i))

    def get_reference_frequency(self):
        """
        FREQ?
        Query the reference frequency. Works in both external and internal reference modes.
        """
        return float(self.query("FREQ?"))

    def set_reference_frequency(self, frequency):
        """
        FREQ {f}
        Sets the frequency of the internal oscillator. This command is only allowed if the reference source is
        internal.

        The frequency is specified in Hz and is rounded by the SR830 to 5 digits or 0.0001 Hz, whichever is greater.
        The frequency is limited to 0.001 <= f <= 102000 Hz by the SR830. If the harmonic number is greater than 1, then
        the frequency is limited to n*f <= 102 kHz.
        """
        self.write("FREQ {}".format(frequency))

    def get_reference_trigger(self):
        """
        RSLP?
        Queries the reference trigger when using the external reference mode.
        Sine zero crossing => 0
        TTL rising edge => 1
        TTL falling edge => 2
        """
        return int(self.query("RSLP?"))

    def set_reference_trigger(self, i):
        """
        RSLP {i}
        Set the reference trigger when using the external reference mode. At frequencies below 1 Hz the TTL reference
        must be used.

        Sine zero crossing => 0
        TTL rising edge => 1
        TTL falling edge => 2
        """
        self.write("RSLP {}".format(i))

    def get_detection_harmonic(self):
        """
        HARM?
        Queries the detection harmonic.
        """
        return int(self.query("HARM?"))

    def set_detection_harmonic(self, i):
        """
        HARM {i}
        Sets the lock-in to detect the i-th harmonic of the reference frequency. The harmonic is limited to integer
        values 1 <= i <= 19999 and is also limited to i*f <= 102 kHz. If the value of i would set the detection
        frequency to a value larger that 102 kHz, the SR830 will set i to the largest value such that
        i*f <= 102 kHz
        """
        self.write("HARM {}".format(i))

    def get_output_amplitude(self):
        """
        SLVL?
        Queries the amplitude of the sine output. The value is rounded to 0.002 V.
        """
        return float(self.query("SLVL?"))

    def set_output_amplitude(self, amplitude):
        """
        SLVL {amplitude}
        Sets the amplitude of the sine output. The value is rounded by the SR830 to 0.002 V. The value is also
        limited by the SR830 to 0.004 <= amplitude <= 5.000 V.
        """
        self.write("SLVL {}".format(amplitude))

    def get_input_configuration(self):
        """
        ISRC?
        Queries the input configuration.
        A => 0
        A-B => 1
        I(1 MOhm) => 2
        I(100 MOhm) => 3
        """
        return int(self.query("ISRC?"))

    def set_input_configuration(self, i):
        """
        ISRC {i}
        Sets the input configuration.
        A => 0
        A-B => 1
        I(1 MOhm) => 2
        I(100 MOhm) => 3

        See Manual for additional information about input sensitivities.
        """
        self.write("ISRC {}".format(i))

    def get_input_coupling(self):
        """
        ICPL?
        Queries the input coupling
        Float => 0
        Ground => 1
        """
        return int(self.query("ICPL?"))

    def set_input_coupling(self, i):
        """
        ICPL {i}
        Sets the input coupling
        Float => 0
        Ground => 1
        """
        self.write("ICPL {}".format(i))

    def get_input_line_notch_filter_status(self):
        """
        ILIN?
        Queries the input line notch filter status
        Out/no filter => 0
        Line notch => 1
        2xLine notch => 2
        Both notch => 3
        """
        return int(self.query("ILIN?"))

    def set_input_line_notch_filter_status(self, i):
        """
        ILIN
        Set the input line notch filter status
        Out/no filter => 0
        Line notch => 1
        2xLine notch => 2
        Both notch => 3
        """
        self.write("ILIN {}".format(i))

    def get_sensitivity(self):
        """
        SENS?
        Queries the sensitivity. For conversion of value to sensitivity see Sensitivity enum
        """
        return Sensitivity(int(self.query("SENS?")))

    def set_sensitivity(self, sens):
        """
        SENS {sens}
        Sets the sensitivity. For conversion of value to sensitivity see Sensitivity enum
        """
        self.write("SENS {sens}".format(int(sens)))

    def get_reserve_mode(self):
        """
        RMOD?
        Query the reserve mode.
        High Reserve => 0
        Normal => 1
        Low Noise => 2
        """
        return int(self.query("RMOD?"))

    def set_reserve_mode(self, i):
        """
        RMOD {i}
        Set the reserve mode
        High Reserve => 0
        Normal => 1
        Low Noise => 2
        """
        self.write("RMOD {i}".format(i))

    def get_time_constant(self):
        """
        OFLT?
        Queries the time constant
        """
        return TimeConstant(self.query("OFLT?"))

    def set_time_constant(self, i):
        """
        OFLT {i}
        Sets the time constant

        See manual for all time constant constraints.
        """
        self.write("OFLT {}".format(int(i)))

    def get_low_pass_filter_slope(self):
        """
        OFSL?
        Queries the low pass filter slope.
        6dB/oct => 0
        12dB/oct => 1
        18dB/oct => 2
        24dB/oct => 3
        """
        return int(self.query("OFSL?"))

    def set_low_pass_filter_slope(self, i):
        """
        OFSL {i}
        Sets the low pass filter slope.
        6dB/oct => 0
        12dB/oct => 1
        18dB/oct => 2
        24dB/oct => 3
        """
        self.write("OFSL {i}".format(i))

    def get_synchronous_filter_status(self):
        """
        SYNC?
        Queries the synchronous filter status
        """
        return int(self.query("SYNC?"))

    def set_synchronous_filter_status(self, i):
        """
        SYNC {i}
        Sets the synchronous filter status. Synchronous filtering is turned on only if the detection frequency
        (reference * harmonic number) is less than 200 Hz.
        Off => 0
        Synchronous filtering below 200 Hz => 1
        """
        self.write("SYNC {i}".format(i))

    def get_output_interface(self):
        """
        OUTX?
        Queries the output interface
        RS232 => 0
        GPIB => 1
        """
        return int(self.query("OUT?"))

    def set_output_interface(self, i):
        """
        OUTX {i}
        Sets the output interface. This command should be sent before any query commands to direct the responses
        to the correct interface.
        RS232 => 0
        GPIB => 1
        """
        self.write("OUTX {}".format(i))

    def get_snap_measurement(self, parameters):
        """
        SNAP?i,j{,k,l,m,n}
        Records the values of 2 to 6 parameters at a single instant
        See the manual for details and limitations of this command

        parameters is a list of 2 to 6 integers
        """
        if len(parameters) < 2 or len(parameters) > 6:
            raise ValueError("The number of parameters in a SNAP measurement must be between 2 and 6 inclusive.")

        return self.query("SNAP?{}".format(",".join(parameters)))

    def reset(self):
        """
        *RST
        Resets the SR830 to its default configurations. The communications setup is not changed. Data stored in
        buffers will be lost.
        """
        self.write("*RST")

    def identify(self):
        """
        *IDN?
        Queries the device's identification string.

        The string will have the following format:
        "Stanford_Research_Systems,SR830,s/n00111,ver1.000".

        In this example, the serial number is 00111 and the firmware version is 1.000
        """
        return self.query("*IDN?")

    def get_local_or_remote_state(self):
        """
        LOCL?
        Queries whether the SR830 is in local or remote mode.
        Local => 0
        Remote => 1
        Local Lockout => 2
        """
        return int(self.query("LOCL?"))

    def set_local_or_remote_state(self, i):
        """
        LOCL {i}
        Sets whether the SR830 is in local or remote mode.
        Local => 0
        Remote => 1
        Local Lockout => 2
        """
        self.write("LOCL {}".format(i))

    def clear_status_registers(self):
        """
        *CLS
        Clears all status registers. The status ENABLE registers are NOT cleared.
        """
        self.write("*CLS")

    def get_standard_event_status_byte(self):
        """
        *ESR?
        Queries the standard event status byte. The byte is cleared after reading.
        """
        return int(self.query("*ESR?"))

