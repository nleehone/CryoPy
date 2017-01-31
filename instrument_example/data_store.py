import zmq


if __name__ == '__main__':
    context = zmq.Context()

    socket = context.socket(zmq.SUB)
    socket.connect('tcp://localhost:5555')
    socket.setsockopt_string(zmq.SUBSCRIBE, '')

    while True:
        message = socket.recv()
        print(message)
