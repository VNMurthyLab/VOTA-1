'''
Created on Aug 9, 2017

@author: Hao Wu
'''
import numpy as np
import serial
import time
from queue import Queue
from math import pow 

class ArduinoWheelDev(object):
    '''
    classdocs
    '''

    def __init__(self, port='COM4',baud_rate=500000):
        '''
        Constructor
        '''
        self.port=port
        self.baud_rate=baud_rate
        self.ser=serial.Serial(self.port,self.baud_rate,timeout=1)
        #self.open()
        self.position=0
        self.last=0
        self.speed=0
        
    def update(self):
        self.ser.flush()
        self.ser.write(b'\x01')
        self.last=self.position
        self.position=self.byte_to_int(self.ser.read(10))
        self.speed=self.position-self.last
        if self.speed>512:
            self.speed-=1024
        elif self.speed<-512:
            self.speed+=1024
        
        
    def byte_to_int(self,b):
        x=0
        for i in range(len(b)):
            x+=b[i]*pow(2,9-i)
        return int(x)
    
    def read(self):
        self.update()
        return (1024-self.position),-self.speed
    
    def read_position(self):
        self.update()
        return (1024-self.position)
    
    def read_raw(self):
        self.ser.write(b'\x01')
        return self.ser.read(10)
    
    def read_speed(self):
        self.update()
        return -self.speed
    
    def open(self):
        self.ser.open()
        time.sleep(2)
        
    def close(self):
        self.ser.close()
    
    def __del__(self):
        self.close()
        del self.ser
        

if __name__ == '__main__':
    sol=ArduinoWheelDev()
    time.sleep(2)
    a=time.time()
    for i in range(100):
        print(sol.read())
    b=time.time()
    print(b-a)