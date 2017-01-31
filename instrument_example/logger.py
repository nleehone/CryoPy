import zmq
import time


if __name__ == '__main__':
    context = zmq.Context()

    socket = context.socket(zmq.SUB)
    socket.connect('tcp://localhost:5555')
    socket.setsockopt_string(zmq.SUBSCRIBE, '')

    last_time = time.time()

    while True:
        message = socket.recv()
        if time.time() - last_time >= 10:
            last_time = time.time()
            print(message)
