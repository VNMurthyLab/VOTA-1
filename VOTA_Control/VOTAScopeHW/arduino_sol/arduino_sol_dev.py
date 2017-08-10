'''
Created on Aug 9, 2017

@author: Hao Wu
'''
import numpy as np
import serial
import time
from queue import Queue

class ArduinoSolDev(object):
    '''
    classdocs
    '''

    def __init__(self, port='COM3',baud_rate=25000):
        '''
        Constructor
        '''
        self.port=port
        self.baud_rate=baud_rate
        #self.ser=serial.Serial(self.port,self.baud_rate,timeout=1)
        
    def write(self,sol_level=[0,0,0,0]):
        output=bytes('s','utf-8');
        for i in range(len(sol_level)):
            output=b''.join([output,sol_level[i].to_bytes(2,'big')])
        self.ser.write(output)
        
        
    def hello(self):
        print('hello')
        
    def read(self):
        return self.ser.readline()
    
    def open(self):
        self.ser.open()
        
    def close(self):
        self.ser.close()
    
    def __del__(self):
        self.close()
        del self.ser
        

if __name__ == '__main__':
    sol=ArduinoSolDev()
    time.sleep(2)
    a=time.time()
    for i in range(3):
        sol.write()
    b=time.time()
    print(sol.read(),i)
    
    print(b-a)