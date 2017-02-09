import zmq
import time
import h5py
import numpy as np
import json

def create_dataset(group, name, attrmap, typedef):
    ds = group.create_dataset(name, (0, 1), maxshape=(None, len(typedef)), dtype=typedef)
    for name, value in attrmap.items():
        ds.attrs[name] = value
    return ds

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
        
        #t_data = raw_data.create_group('temperature')
        #t_data.attrs['instrument'] = 'LS350'
        
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
        
        lockin_ds = create_dataset(raw_data, 'Lock-In', {'instrument': 'SR830'}, lockin_type)
        t_ds = create_dataset(raw_data, 'Temperature', {'instrument': 'LS350'}, ls350_type)

    
        last_time = time.time()
        count = 0
        while True:
            tag, data = map(lambda x: x.decode('utf-8'), socket.recv_multipart())
            data = json.loads(data)
            
            if tag == 'lock-in':
                x, y = data['x'], data['y']
                valid = data['valid']
    
                lockin_ds.resize(count+1,axis=0)
                lockin_ds[count] = (data['time'], x, y, valid)
                count += 1
            elif tag == 'LS350':
                print(data)
            
