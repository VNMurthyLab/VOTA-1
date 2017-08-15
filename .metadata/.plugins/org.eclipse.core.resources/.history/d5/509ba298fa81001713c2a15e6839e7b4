'''
Created on Aug 9, 2017

@author: Hao Wu
'''

from ScopeFoundry import HardwareComponent
from VOTAScopeHW.arduino_wheel.arduino_wheel_dev import ArduinoWheelDev
import time
from math import exp
class ArduinoWheelHW(HardwareComponent):
    '''
    Hardware Component Class for receiving AI input for breathing, licking etc
    '''
    
    name='arduino_wheel'

    def setup(self,port='COM4',baud_rate=500000):
        '''
        add settings for analog input event
        '''
        self.settings.New(name='port',initial=port,dtype=str,ro=False)
        self.settings.New(name='baud_rate',initial=baud_rate,dtype=int,ro=False)
        self.settings.New(name='position',initial=0,dtype=int,ro=True)
        self.settings.New(name='speed',initial=0,dtype=int,ro=True)

    def read(self):
        return self._dev.read()
       
    def connect(self):
        self._dev=ArduinoWheelDev(self.settings.port.value(),
                          self.settings.baud_rate.value())
                
        self.settings.position.connect_to_hardware(read_func=self._dev.read_position)
        self.settings.speed.connect_to_hardware(read_func=self._dev.read_speed)
        self.settings.position.read_from_hardware()
        self.settings.speed.read_from_hardware()

    
  
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
