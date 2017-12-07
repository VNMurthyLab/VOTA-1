'''
Created on Aug 9, 2017

@author: Hao Wu
'''
import numpy as np
import serial
import time
from queue import Queue
import h5py as h5

class ArduinoSolDev(object):
    '''
    classdocs
    '''
    
    def __init__(self, port='COM3',baud_rate=500000):
        '''
        Constructor
        '''
        self.port=port
        self.baud_rate=baud_rate
        self.ser=serial.Serial(self.port,self.baud_rate,timeout=1)
        #self.open()
        self.chan_id = [b'\x02',b'\x01',b'\x08',b'\x04',b'\x20',b'\x10',b'\x80',b'\x40']
        
    def write(self,sol,level):
        output=bytes('w','utf-8');
        output=output + self.chan_id[sol]
        output=output+level.to_bytes(1,'big')
        self.ser.write(output)

    def read(self):
        return self.ser.readline()
    
    def open(self):
        self.ser.open()
        time.sleep(2)
        
    def close(self):
        self.ser.close()
    
    def __del__(self):
        self.close()
        del self.ser
    

if __name__ == '__main__':
    sol=ArduinoSolDev()
    time.sleep(2)
#     a=time.time()
#     for i in range(1000):
#         sol.write()
#     b=time.time()
#     print(sol.read(),i)
#     
#     print(b-a)
