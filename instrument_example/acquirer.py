import zmq
import time


if __name__ == '__main__':
    context = zmq.Context()
    socket = context.socket(zmq.PUB)
    socket.bind('tcp://*:5555')
    socket1 = context.socket(zmq.REQ)
    socket1.connect('tcp://localhost:5557')

    while True:
        socket1.send_json({'Cmd': 'Get'})
        temp = socket1.recv_json()['T']
        print('sending %s' % temp)
        socket.send_json({'T': temp})
        time.sleep(0.01)
