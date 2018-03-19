'''
Created on Aug 9, 2017

@author: Hao Wu
'''

from ScopeFoundry import HardwareComponent
from VOTAScopeHW.arduino_water.arduino_water_dev import ArduinoWaterDev
import time
from math import exp
class ArduinoWaterHW(HardwareComponent):
    '''
    Hardware Component Class for receiving AI input for breathing, licking etc
    '''
    
    name='arduino_water'

    def setup(self,port='COM6',baud_rate=250000):
        '''
        add settings for analog input event
        '''
        self.settings.New(name='port',initial=port,dtype=str,ro=False)
        self.settings.New(name='baud_rate',initial=baud_rate,dtype=int,ro=False)
        self.settings.New(name='water_on',initial=False,dtype=bool,ro=False)
        
        self.settings.New(name='water_on_0',initial=False,dtype=bool,ro=False)
        self.settings.New(name='water_on_1',initial=False,dtype=bool,ro=False)
        
        self.add_operation(name='manual_drop_0',op_func = self.give_water_manual_0)
        self.add_operation(name='manual_drop_1',op_func = self.give_water_manual_1)
        
        self.open_time=[]
        self.open_time.append(self.settings.New(name='open_time_0',initial=85,dtype=int,ro=False,vmin=1,vmax=1000))
        self.open_time.append(self.settings.New(name='open_time_1',initial=85,dtype=int,ro=False,vmin=1,vmax=1000))

    def give_water_manual_0(self):
        self.give_water(side=0)
        
    def give_water_manual_1(self):
        self.give_water(side=1)
        
    def give_water(self,side=0):
        self._dev.drop_water(side,self.open_time[side].value())
            
       
    def connect(self):
        self._dev=ArduinoWaterDev(self.settings.port.value(),
                          self.settings.baud_rate.value())
        self.settings.water_on_0.connect_to_hardware(write_func=self._dev.switch0)
        self.settings.water_on_1.connect_to_hardware(write_func=self._dev.switch1)
        time.sleep(2)

    
  
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
