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
        
        newtype = np.dtype([('Status A', int),
                             ('Status B', int),
                             ('Status C', int),
                             ('Status D', int),
                             ('Temp A', float), 
                            ('Temp B', float),
                            ('Temp C', float),
                            ('Temp D', float),
                            ('Setp A', float),
                            ('Setp B', float),
                            ('Setp C', float),
                            ('Setp D', float),
                            ('Sens A', float),
                            ('Sens B', float),
                            ('Sens C', float),
                            ('Sens D', float),
                            ('Htr Status 1', int),
                            ('Htr Status 2', int),
                            ('Htr Range 1', int),
                            ('Htr Range 2', int),
                            ('Htr Range 3', int),
                            ('Htr Range 4', int),
                            ('Htr Output 1', float),
                            ('Htr Output 2', float),
                            ('Htr Output 3', float),
                            ('Htr Output 4', float),
                            ('Htr MOut 1', float),
                            ('Htr MOut 2', float),
                            ('Htr MOut 3', float),
                            ('Htr MOut 4', float),
                            ('P 1', float),
                            ('I 1', float),
                            ('D 1', float),
                            ('P 2', float),
                            ('I 2', float),
                            ('D 2', float),
                            ('P 3', float),
                            ('I 3', float),
                            ('D 3', float),
                            ('P 4', float),
                            ('I 4', float),
                            ('D 4', float)
                            ])

        t_ds = raw_data.create_dataset('temperature', (0,1), maxshape=(None, len(newtype)), dtype=newtype)
        t_ds.attrs['instrument'] = 'LS350'
    
        last_time = time.time()
        count = 0
        while True:
            message = socket.recv_json()
            #if time.time() - last_time >= 10:
            #   last_time = time.time()
            #   print(message)
            print(message)
            
            rdgA,rdgB,rdgC,rdgD,tA,tB,tC,tD,sA,sB,sC,sD,set1,set2,set3,set4 = message['temperature'].split(';')
            htrst1,htrst2,htr_rng1,htr_rng2,htr_rng3,htr_rng4,htr1,htr2,aout3,aout4,mout1,mout2,mout3,mout4,pid1,pid2,pid3,pid4 = message['heater'].split(';')
            print(rdgA,rdgB,rdgC,rdgD)
            print(tA,tB,tC,tD)
            print(sA,sB,sC,sD)
            print(set1,set2,set3,set4)
            print(htrst1,htrst2)
            print(htr_rng1,htr_rng2,htr_rng3,htr_rng4)
            print(htr1,htr2,aout3,aout4)
            print(mout1,mout2,mout3,mout4)
            print(pid1)
            print(pid2)
            print(pid3)
            print(pid4)
            p1,i1,d1 = pid1.split(',')
            p2,i2,d2 = pid2.split(',')
            p3,i3,d3 = pid2.split(',')
            p4,i4,d4 = pid2.split(',')
            
            t_ds.resize(count+1,axis=0)
            t_ds[count] = (int(rdgA), int(rdgB), int(rdgC), int(rdgD),
                        float(tA), float(tB), float(tC), float(tD),
                        float(set1), float(set2), float(set3), float(set4),
                        float(sA), float(sB), float(sC), float(sD),
                        int(htrst1), int(htrst2),
                        int(htr_rng1), int(htr_rng2), int(htr_rng3), int(htr_rng4),
                        float(htr1), float(htr2), float(aout3), float(aout4),
                        float(mout1), float(mout2), float(mout3), float(mout4),
                        float(p1), float(i1), float(d1),
                        float(p2), float(i2), float(d2),
                        float(p3), float(i3), float(d3),
                        float(p4), float(i4), float(d4))
            count += 1
            
