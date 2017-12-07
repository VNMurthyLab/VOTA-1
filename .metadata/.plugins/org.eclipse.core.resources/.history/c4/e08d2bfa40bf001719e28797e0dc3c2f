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

    def __init__(self, port='COM3',baud_rate=250000,fname='D:\\Hao\\VOTA\\VOTA_Control\\VOTAScopeHW\\arduino_sol\\sol_calib.h5'):
        '''
        Constructor
        '''
        self.port=port
        self.baud_rate=baud_rate
        self.ser=serial.Serial(self.port,self.baud_rate,timeout=1)
        #self.open()
        self.calib=np.zeros((101,4),dtype=int)
        self.load_calib(fname)
        
    def write(self,sol_level=[0,0,0,0]):
        output=bytes('s','utf-8');
        for i in range(len(sol_level)):
            output=output+int(self.calib[sol_level[i],i]).to_bytes(2,'big')
        self.ser.write(output)
        
    def write_raw(self,sol_level=[0,0,0,0]):
        output=bytes('s','utf-8');
        for i in range(len(sol_level)):
            output=output+sol_level[i].to_bytes(2,'big')
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
    
    def load_calib(self,fname):
        f=h5.File(fname,'r')
        dset=f['calib']
        self.calib[:]=dset[:].transpose()
        f.close()

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
    sol.load_calib('sol_calib.h5')
    print(sol.calib)