import zmq
import time
import h5py
import numpy as np
import json


class DataSet(object):
    """
    Encapsulation of a dataset and a counter to keep track of what row to write the data into
    """
    def __init__(self, group, name, attrmap, typedef):
        self.ds = group.create_dataset(name, (0, 1), maxshape=(None, len(typedef)), dtype=typedef)
        for name, value in attrmap.items():
            self.ds.attrs[name] = value
        self.count = 0
        self.typedef = typedef

    def add_data(self, data):
        print(data)
        self.ds.resize(self.count+1, axis=0)
        self.ds[self.count] = tuple(data[name] for name in self.typedef.names)
        self.count += 1


if __name__ == '__main__':
    context = zmq.Context()

    socket = context.socket(zmq.SUB)
    socket.connect('tcp://localhost:5581')
    socket.connect('tcp://localhost:5556')
    socket.setsockopt_string(zmq.SUBSCRIBE, '')
    
    file_name = 'test.hdf5'
    with h5py.File(file_name, 'w') as f:
        f.attrs['file_name'] = file_name
        f.attrs['file_creation_time'] = time.strftime("%a, %d %b %Y %X +0000", time.gmtime())
        f.attrs['operator'] = 'Nicholas'
        f.attrs['sample'] = 'Test sample'
        f.attrs['comment'] = 'Comment'
        
        raw_data = f.create_group('raw_data')
        
        lockin_type = np.dtype([
                            ('Time', float),
                            ('Lock-In X', float),
                            ('Lock-In Y', float),
                            ('Valid', bool),
                            ])
        
        ls350_type = np.dtype([
                               ('Time', float),
                               ('TempA', float),
                               ('TempB', float),
                               ('SensA', float),
                               ('SensB', float),
                               ])

        lockin_ds = DataSet(raw_data, 'Lock-In', {'instrument': 'SR830'}, lockin_type)
        t_ds = DataSet(raw_data, 'Temperature', {'instrument': 'LS350'}, ls350_type)

        count = 0
        while True:
            tag, data = map(lambda x: x.decode('utf-8'), socket.recv_multipart())
            data = json.loads(data)
            
            if tag == 'lock-in':
                lockin_ds.add_data(data)
            elif tag == 'LS350':
                t_ds.add_data(data)
