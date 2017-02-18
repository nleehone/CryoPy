from component import Acquirer
from SR830.config import *
import time
import sys
sys.path.append('../')


class SR830Acquirer(Acquirer):
    def __init__(self):
        super().__init__("SR830")

    def acquire(self):
        # Get the data from the instrument driver
        measurement_time = time.time()
        self.publish(measurement_time)
        #self.driver_socket.send_json({'METHOD': 'GET', 'CMD': 'snap_measurement', 'PARS': [1,2]})
        #data = self.driver_socket.recv_json()
        #self.driver_socket.send_json({'METHOD': 'GET', 'CMD': 'status', 'PARS': ''})
        #status = self.driver_socket.recv_json()
        #self.driver_socket.send_json({'METHOD': 'GET', 'CMD': 'standard_event_status_byte', 'PARS': ''})
        #event_status = self.driver_socket.recv_json()

        #print(data)
        #print(not (status&4))
        #x, y = map(float, data)
        #res = {'Lock-In X': x,
        #       'Lock-In Y': y,
        #       'Valid': not (status & 4),
        #       'Status': status,
        #       'Event_status': event_status,
        #       'Time': measurement_time
        #       }
        #print(time.time(), res)
        #self.pub_socket.send_multipart([b'lock-in', json.dumps(res).encode('utf-8')])

        time.sleep(1)


if __name__ == '__main__':
    with SR830Acquirer() as acquirer:
        pass
