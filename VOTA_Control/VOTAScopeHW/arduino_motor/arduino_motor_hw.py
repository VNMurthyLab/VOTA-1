'''
Created on Aug 9, 2017

@author: Hao Wu
'''

from ScopeFoundry import HardwareComponent
from VOTAScopeHW.arduino_motor.arduino_motor_dev import ArduinoMotorDev
import time

class ArduinoMotorHW(HardwareComponent):
    '''
    Hardware Component Class for receiving AI input for breathing, licking etc
    '''
    
    name='arduino_motor'

    def setup(self,port='COM5',baud_rate=250000):
        '''
        add settings for analog input event
        '''
        self.settings.New(name='port',initial=port,dtype=str,ro=False)
        self.settings.New(name='baud_rate',initial=baud_rate,dtype=int,ro=False)
        self.settings.New(name='lick_position',initial=False,dtype=bool,ro=False)
        self.add_operation('reset',self.reset)
        
    def connect(self):
        self._dev=ArduinoMotorDev(self.settings.port.value(),
                          self.settings.baud_rate.value())
        time.sleep(2)
        self.settings.lick_position.connect_to_hardware(write_func=self._dev.switch)
        
    def reset(self):
        self._dev.reset()
        self.settings.lick_position.val = False
  
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
