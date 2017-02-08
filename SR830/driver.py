import visa
import time
import sys
sys.path.append('../')
from drivers import SR830
from component import *


class Driver(Driver):
    """
    Commands:
    """

    def __init__(self, driver_port):
        super().__init__(driver_port)
        rm = visa.ResourceManager()
        self.SR830 = SR830(rm.open_resource('ASRL4::INSTR'))

        self.get_commands = {
            'phase': self.get_phase,
            'reference_source': self.get_reference_source,
            'reference_frequency': self.get_reference_frequency,
            'reference_trigger': self.get_reference_trigger,
            'detection_harmonic': self.get_detection_harmonic,
            'output_amplitude': self.get_output_amplitude,
            'input_configuration': self.get_input_configuration,
            'input_coupling': self.get_input_coupling,
            'line_notch_filter_status': self.get_line_notch_filter_status,
            'sensitivity': self.get_sensitivity,
            'reserve_mode': self.get_reserve_mode,
            'time_constant': self.get_time_constant,
            'low_pass_filter_slope': self.get_low_pass_filter_slope,
            'synchronous_filter_status': self.get_synchronous_filter_status,
            'output_interface': self.get_output_interface,
            'snap_measurement': self.get_snap_measurement,
            'local_or_remote_state': self.get_local_or_remote_state,
            'standard_event_status_byte': self.get_standard_event_status_byte,
            'identify': self.identify,
        }

        self.set_commands = {
            'phase': self.set_phase,
            'reference_source': self.set_reference_source,
            'reference_frequency': self.set_reference_frequency,
            'reference_trigger': self.set_reference_trigger,
            'detection_harmonic': self.set_detection_harmonic,
            'output_amplitude': self.set_output_amplitude,
            'input_configuration': self.set_input_configuration,
            'input_coupling': self.set_input_coupling,
            'line_notch_filter_status': self.set_line_notch_filter_status,
            'sensitivity': self.set_sensitivity,
            'reserve_mode': self.set_reserve_mode,
            'time_constant': self.set_time_constant,
            'low_pass_filter_slope': self.set_low_pass_filter_slope,
            'synchronous_filter_status': self.set_synchronous_filter_status,
            'output_interface': self.set_output_interface,
            'reset': self.reset,
            'local_or_remote_state': self.set_local_or_remote_state,
            'clear_status_registers': self.clear_status_registers
        }

    def set_phase(self, pars):
        self.SR830.set_phase(pars['phase'])

    def set_reference_source(self, pars):
        self.SR830.set_reference_source(pars['source'])

    def set_reference_frequency(self, pars):
        self.SR830.set_reference_frequency(pars['frequency'])

    def set_reference_trigger(self, pars):
        self.SR830.set_reference_trigger(pars['trigger'])

    def set_detection_harmonic(self, pars):
        self.SR830.set_detection_harmonic(pars['harmonic'])

    def set_output_amplitude(self, pars):
        self.SR830.set_output_amplitude(pars['amplitude'])

    def set_input_configuration(self, pars):
        self.SR830.set_input_configuration(pars['input_config'])

    def set_input_coupling(self, pars):
        self.SR830.set_input_coupling(pars['coupling'])

    def set_line_notch_filter_status(self, pars):
        self.SR830.set_input_line_notch_filter_status(pars['notch_filter'])

    def set_sensitivity(self, pars):
        self.SR830.set_sensitivity(pars['sensitivity'])

    def set_reserve_mode(self, pars):
        self.SR830.set_reserve_mode(pars['mode'])

    def set_time_constant(self, pars):
        self.SR830.set_time_constant(pars['time_constant'])

    def set_low_pass_filter_slope(self, pars):
        self.SR830.set_low_pass_filter_slope(pars['slope'])

    def set_synchronous_filter_status(self, pars):
        self.SR830.set_synchronous_filter_status(pars['status'])

    def set_output_interface(self, pars):
        self.SR830.set_output_interface(pars['interface'])

    def reset(self, pars):
        self.SR830.reset()

    def set_local_or_remote_state(self, pars):
        self.SR830.set_local_or_remote_state(pars['state'])

    def clear_status_registers(self, pars):
        self.SR830.clear_status_registers()

    def identify(self, pars):
        return self.SR830.identify()

    def get_phase(self, pars):
        return self.SR830.get_phase()

    def get_reference_source(self, pars):
        return self.SR830.get_reference_source()

    def get_reference_frequency(self, pars):
        return self.SR830.get_reference_frequency()

    def get_reference_trigger(self, pars):
        return self.SR830.get_reference_trigger()

    def get_detection_harmonic(self, pars):
        return self.SR830.get_detection_harmonic()

    def get_output_amplitude(self, pars):
        return self.SR830.get_output_amplitude()

    def get_input_configuration(self, pars):
        return self.SR830.get_input_configuration()

    def get_input_coupling(self, pars):
        return self.SR830.get_input_coupling()

    def get_line_notch_filter_status(self, pars):
        return self.SR830.get_input_line_notch_filter_status()

    def get_sensitivity(self, pars):
        return self.SR830.get_sensitivity()

    def get_reserve_mode(self, pars):
        return self.SR830.get_reserve_mode()

    def get_time_constant(self, pars):
        return self.SR830.get_time_constant()

    def get_low_pass_filter_slope(self, pars):
        return self.SR830.get_low_pass_filter_slope()

    def get_synchronous_filter_status(self, pars):
        return self.SR830.get_synchronous_filter_status()

    def get_output_interface(self, pars):
        return self.SR830.get_output_interface()

    def get_snap_measurement(self, pars):
        return self.SR830.get_snap_measurement(pars)

    def get_local_or_remote_state(self, pars):
        return self.SR830.get_local_or_remote_state()

    def get_standard_event_status_byte(self, pars):
        return self.SR830.get_standard_event_status_byte()
