'''
Created on Aug 9, 2017

@author: Hao Wu
'''

from ScopeFoundry import HardwareComponent
from VOTAScopeHW.arduino_odometer.arduino_odometer_dev import ArduinoOdometerDev
import time
from math import exp

class ArduinoOdometerHW(HardwareComponent):
    '''
    Hardware Component Class for receiving AI input for breathing, licking etc
    '''
    
    name='arduino_odometer'

    def setup(self,port='COM4',baud_rate=250000):
        '''
        add settings for analog input event
        '''
        self.settings.New(name='port',initial=port,dtype=str,ro=False)
        self.settings.New(name='baud_rate',initial=baud_rate,dtype=int,ro=False)
        self.settings.New(name='x',initial=0,dtype=int,ro=True)
        self.settings.New(name='y',initial=0,dtype=int,ro=True)
        self.settings.New(name='vx',initial=0,dtype=int,ro=True)
        self.settings.New(name='vy',initial=0,dtype=int,ro=True)

    def read(self):
        position, speed = self._dev.read()
        self.settings.x.update_value(position[0])
        self.settings.y.update_value(position[1])
        self.settings.vx.update_value(speed[0])
        self.settings.vy.update_value(speed[1])
       
    def connect(self):
        self._dev=ArduinoOdometerDev(self.settings.port.value(),
                          self.settings.baud_rate.value())


    
  
    def start(self):
        self._dev.open()
        
    def stop(self):
        self._dev.close()
        
    def disconnect(self):
        try:
            self.stop()
            del self._dev
            del self.write
            
        except AttributeError:
            pass
