'''
Created on Aug 9, 2017

@author: Hao Wu
'''
import numpy as np
import serial
import time
from queue import Queue
import h5py as h5

class ArduinoWaterDev(object):
    '''
    classdocs
    '''

    def __init__(self, port='COM6',baud_rate=250000):
        '''
        Constructor
        '''
        self.port=port
        self.baud_rate=baud_rate
        self.ser=serial.Serial(self.port,self.baud_rate,timeout=1)
        self.w=['w','W']
        self.o=['o','O']
        self.f=['f','F']
        #self.open()
        
        
    def drop_water(self,side=0,wait_time=20):
        output=bytes(self.w[side],'utf-8')
        output=output+int(wait_time).to_bytes(1,'little')
        self.ser.write(output)
        #print(output)

    def read(self):
        return self.ser.readline()
    
    def switch(self,side=0,water_on=False):
        if water_on:
            self.water_on(side)
        else:
            self.water_off(side)
    
    def switch0(self,wt=False):
        self.switch(0,wt)
        
    def switch1(self,wt=False):
        self.switch(1,wt)
        
    def open(self):
        self.ser.open()
        time.sleep(2)
        
    def close(self):
        self.ser.close()
        
    def water_on(self,side=0):
        output=bytes(self.o[side],'utf-8')
        self.ser.write(output)
        self.read()
    
    def water_off(self,side=0):
        output=bytes(self.f[side],'utf-8')
        self.ser.write(output)
        self.read()
    
    def __del__(self):
        self.close()
        del self.ser


if __name__ == '__main__':
    water=ArduinoWaterDev()
    time.sleep(2)
    for i in range(100):
        time.sleep(0.2)
        water.drop_water(1,85)
