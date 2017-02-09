import zmq
import time
import h5py
import numpy as np

if __name__ == '__main__':
    context = zmq.Context()

    socket = context.socket(zmq.SUB)
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
        
        newtype = np.dtype([('Lock-In X', float),
                            ('Lock-In Y', float),
                            ('Valid', bool),
                            ])

        lockin_ds = raw_data.create_dataset('Lock-In', (0,1), maxshape=(None, len(newtype)), dtype=newtype)
        lockin_ds.attrs['instrument'] = 'SR830'
    
        last_time = time.time()
        count = 0
        while True:
            message = socket.recv_json()
            print(message)

            x, y = message['x'], message['y']
            valid = message['valid']

            lockin_ds.resize(count+1,axis=0)
            lockin_ds[count] = (x, y, valid)
            count += 1
            
