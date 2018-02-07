'''
Created on Aug 9, 2017

@author: Hao Wu
'''
import numpy as np
import serial
import time
from queue import Queue
from math import pow 

class ArduinoOdometerDev(object):
    '''
    classdocs
    '''

    def __init__(self, port='COM4',baud_rate=250000):
        '''
        Constructor
        '''
        self.port=port
        self.baud_rate=baud_rate
        self.ser=serial.Serial(self.port,self.baud_rate,timeout=1)
        #self.open()
        self.x = 0
        self.y = 0
        self.vx=0
        self.vy=0
        
    def update(self):
        self.ser.flush()
        self.ser.write(bytes('r','utf-8'))
        self.vx=self.byte_to_int(self.ser.read(8))
        self.vy=self.byte_to_int(self.ser.read(8))
        self.x += self.vx
        self.y += self.vy
        
        
    def byte_to_int(self,b):
        x=0
        for i in range(7):
            x+=b[i]*pow(2,i)
        if b[7]:
            x-=128
        return int(x)
    
    def read(self):
        self.update()
        return (self.x,self.y),(self.vx,self.vy)
    
    def read_position(self):
        self.update()
        return (self.x,self.y)
    
    def read_raw(self):
        self.ser.write(bytes('r','utf-8'))
        return self.ser.read(8)
    
    def read_speed(self):
        self.update()
        return (self.vx,self.vy)
    
    def open(self):
        self.ser.open()
        time.sleep(2)
        
    def close(self):
        self.ser.close()
    
    def __del__(self):
        self.close()
        del self.ser
        

if __name__ == '__main__':
    sol=ArduinoOdometerDev()
    time.sleep(3)
    a=time.time()
    for i in range(100):
        time.sleep(0.01)
        print(sol.read())
    b=time.time()
    print(b-a)