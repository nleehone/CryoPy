from SR830.config import *
import zmq
import sys
sys.path.append('../')
from component import Component
from threading import Thread
from drivers import SR830sensitivity


class Controller(Component):
    def __init__(self, command_port, acquirer_port, driver_port):
        super().__init__(command_port)

        self.acquirer_socket = self.context.socket(zmq.SUB)
        self.acquirer_socket.connect('tcp://localhost:{}'.format(acquirer_port))
        self.acquirer_socket.setsockopt_string(zmq.SUBSCRIBE, '')

        self.driver_socket = self.context.socket(zmq.REQ)
        self.driver_socket.connect('tcp://localhost:{}'.format(driver_port))
        
        self.upper_threshold = 0.9
        self.upper_threshold_count = 5
        self.lower_threshold = 0.1
        self.lower_threshold_count = 5
        self.auto_range = True
        
        self.low_count = 0
        self.high_count = 0
        
        p = Thread(target=self.control_loop)
        p.start()
        
        self.internal_commands = {
                                 "upper_threshold": self.set_upper_threshold, 
                                  "lower_threshold": self.set_lower_threshold,
                                  "upper_threshold_count": self.set_upper_threshold_count,
                                  "lower_threshold_count": self.set_lower_threshold_count,
                                  "auto_range": self.set_auto_range
                                  }
                                  
    def set_auto_range(self, auto):
        self.auto_range = auto
                                  
    def set_upper_threshold_count(self, count):
        self.upper_threshold_count = count
        
    def set_lower_threshold_count(self, count):
        self.lower_threshold_count = count
                                  
    def set_upper_threshold(self, threshold):
        self.upper_threshold = threshold
        
    def set_lower_threshold(self, threshold):
        self.lower_threshold = threshold

    def run(self):
        while True:
            cmd = self.command_socket.recv_json()
            method = cmd["METHOD"]

            if method == "GET":
                self.driver_socket.send_json(cmd)
                val = self.driver_socket.recv_json()
            elif method == "SET":
                command = cmd["CMD"]
                if command in self.internal_commands.keys():
                    self.internal_commands[command](cmd["PARS"])
                else:
                    self.driver_socket.send_json(cmd)
                    val = self.driver_socket.recv_json()
            
            self.command_socket.send_json(val)
            
    def control_loop(self):
        while True:
            res = self.acquirer_socket.recv_json()
            event_status = res['event_status']
            status = res['status']

            if self.auto_range:
                self.auto_range_func(status, res['x'])
                
                    
    def auto_range_func(self, status, value):
        if status & 4:
            print("Overload")
            
            self.driver_socket.send_json({'METHOD': 'GET', 'CMD': 'sensitivity', 'PARS': ''})
            sensitivity = self.driver_socket.recv_json()
            print(SR830sensitivity[sensitivity])
            self.driver_socket.send_json({'METHOD': 'SET', 'CMD': 'sensitivity', 'PARS': sensitivity + 1})
            self.driver_socket.recv_json()
            #self.command_socket.send_json({'METHOD': 'SET', 'CMD': })
        else:
            print("No Overload")
            self.driver_socket.send_json({'METHOD': 'GET', 'CMD': 'sensitivity', 'PARS': ''})
            sensitivity = SR830sensitivity[self.driver_socket.recv_json()]
            print(sensitivity)
            if sensitivity[2]*self.lower_threshold >= abs(value):
                print("Low")
                self.high_count = 0
                self.low_count += 1
            elif sensitivity[2]*self.upper_threshold <= abs(value):
                print("High")
                self.low_count = 0
                self.high_count += 1
            else:
                print("In range")
                self.low_count = 0
                self.high_count = 0
                
            if self.high_count >= self.upper_threshold_count:
                print("increase sensitivity")
                self.driver_socket.send_json({'METHOD': 'SET', 'CMD': 'sensitivity', 'PARS': sensitivity[0]+1})
                self.driver_socket.recv_json()
                self.high_count = 0
            elif self.low_count >= self.lower_threshold_count:
                print("decrease sensitivity")
                self.driver_socket.send_json({'METHOD': 'SET', 'CMD': 'sensitivity', 'PARS': sensitivity[0]-1})
                self.driver_socket.recv_json()
                self.low_count = 0


if __name__ == '__main__':
    Controller(controller_port, acquirer_pub_port, driver_port).run()
