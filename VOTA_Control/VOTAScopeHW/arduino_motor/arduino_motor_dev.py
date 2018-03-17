'''
Created on Aug 9, 2017

@author: Hao Wu
'''
import numpy as np
import serial
import time
from queue import Queue

class ArduinoMotorDev(object):
    '''
    classdocs
    '''

    def __init__(self, port='COM5',baud_rate=250000):
        '''
        Constructor
        '''
        self.port=port
        self.baud_rate=baud_rate
        self.ser=serial.Serial(self.port,self.baud_rate,timeout=1)
        self.lick_position = True
        
        #self.open()
        
    def reset(self):
        output=bytes('r','utf-8')
        self.ser.write(output)
        time.sleep(0.4)
        self.backward()
        self.lick_position = False
        
    def switch(self, position):
        if position == self.lick_position:
            pass
        else:
            if position:
                self.forward()
            else:
                self.backward()
            self.lick_position = position
         
    def forward(self):
        output=bytes('f','utf-8')
        self.ser.write(output)
        
    def backward(self):
        output=bytes('b','utf-8')
        self.ser.write(output)
        
    def close(self):
        self.ser.close()
        
    
    def __del__(self):
        self.close()
        del self.ser


if __name__ == '__main__':
    motor=ArduinoMotorDev()
    time.sleep(2)
    motor.forward()
    time.sleep(1)
    motor.backward()