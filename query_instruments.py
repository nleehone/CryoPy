# -*- coding: utf-8 -*-
"""
Created on Wed Feb 22 09:07:08 2017

@author: CryogenicSystem
"""

import visa
import pyvisa
import time

rm = visa.ResourceManager()
resources = list(rm.list_resources())
resources.remove('ASRL10::INSTR')
print(resources)

# List common baud rates first. 9600 has to be first so that the SR830 doesn't mess up
# Otherwise it causes the interface to error out continuously and requires a manual restart
baud_rates = (19200, 9600, 57600, 38400, 115200, 4800, 2400, 1200, 600, 300)
parities = (visa.constants.Parity.none, visa.constants.Parity.odd, visa.constants.Parity.even)
data_bits = (8, 7, 6, 5)

pars = {"baud_rate": 0,
        "data_bits": 0,
        "stop_bits": 0,
        "parity": 0,
        "read_termination": 0
        }
        
def set_instrument(instr, params):
    instr.data_bits = params['data_bits']
    instr.read_termination = params['read_termination']
    instr.parity = params['parity']
    instr.stop_bits = params['stop_bits']
    instr.baud_rate = params['baud_rate']

for resource in resources[2:]:
    instrument = rm.open_resource(resource)
    instrument.timeout = 500
    
    pars['read_termination'] = instrument.CR
    pars['stop_bits'] = visa.constants.StopBits.one

    print("Trying to connect to resource:", resource)
    
    #for key in pyvisa.attributes.AttributesByID.keys():
    #    try:
    #        print(pyvisa.attributes.AttributesByID[key], instrument.get_visa_attribute(key))
    #    except Exception:
    #        pass
    found = False
    for data_bit in data_bits:
        pars['data_bits'] = data_bit
        for parity in parities:
            pars['parity'] = parity
            for baud in baud_rates:
                pars['baud_rate'] = baud
                idn = "None"
                try:
                    set_instrument(instrument, pars)
                    #print("Trying baud:", baud)
                    instrument.write("*CLS")
                    time.sleep(0.5)
                    idn = instrument.query("*IDN?")
                    #idn = instrument.read(encoding="unicode_escape")
                    #idn = idn.encode('unicode_escape')
                    if idn:
                        print(idn, pars)
                        found = True
                        break
                except (pyvisa.errors.VisaIOError, UnicodeDecodeError) as e:
                    pass
                    #print(idn)
                    #print("Count not contact", resource)
            if found:
                break
        if found:
            break
    else:
        print("Could not connect to", resource)
    print("----------------------------------")