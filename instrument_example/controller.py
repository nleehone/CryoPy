import zmq
from threading import Thread


def command_loop():
    # Contexts are thread dependent so we need to start the context here
    socket1 = context.socket(zmq.REP)
    socket1.bind('tcp://*:5556')
    socket2 = context.socket(zmq.REQ)
    socket2.connect('tcp://localhost:5557')

    while True:
        T = socket1.recv_json()['Set T']
        socket2.send_json({'Cmd': 'Set', 'T': T})
        socket2.recv_json()
        #driver.set_temperature(T)
        print("Set T")
        socket1.send(b'')


if __name__ == '__main__':
    context = zmq.Context()

    socket = context.socket(zmq.SUB)
    socket.connect('tcp://localhost:5555')
    socket.setsockopt_string(zmq.SUBSCRIBE, '')

    p = Thread(target=command_loop)
    p.start()

    while True:
        message = socket.recv()
        #print(message)
