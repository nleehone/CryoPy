import numpy as np
import instrument_example.instrument as instr
import zmq


def set_temperature(T):
    instrument = instr.Instrument()
    instrument.set_temperature(T)

def get_temperature():
    instrument = instr.Instrument()
    return instrument.get_temperature() + 10.0*(np.random.rand()*2.0 - 1.0)


if __name__ == '__main__':
    context = zmq.Context()
    socket = context.socket(zmq.REP)
    socket.bind('tcp://*:5557')

    while True:
        command = socket.recv_json()
        if command['Cmd'] == 'Set':
            set_temperature(command['T'])
            socket.send_json({})
            "Here"
        elif command['Cmd'] == 'Get':
            socket.send_json({'T': get_temperature()})

