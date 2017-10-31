'''
Created on Aug 9, 2017

@author: Hao Wu
'''

from ScopeFoundry import HardwareComponent
from .arduino_sol_dev import ArduinoSolDev
from PyDAQmx import *
import numpy as np
import time
from math import exp
class ArduinoSolHW(HardwareComponent):
    '''
    Hardware Component Class for receiving AI input for breathing, licking etc
    '''
    
    name='arduino_sol'

    def setup(self,port='COM3',baud_rate=250000,fname='D:\\Hao\\VOTA\\VOTA_Control\\VOTAScopeHW\\arduino_sol\\sol_calib.h5'):
        '''
        add settings for analog input event
        '''
        self.settings.New(name='port',initial=port,dtype=str,ro=False)
        self.settings.New(name='baud_rate',initial=baud_rate,dtype=int,ro=False)
        self.settings.New(name='calibration_fname',initial=fname,dtype=str,ro=False)
        
        self.sols=[]

        self.sols.append(self.settings.New(name='clean_cair',initial=0,dtype=int,ro=False,vmin=0,vmax=100))
        self.sols.append(self.settings.New(name='odor1',initial=0,dtype=int,ro=False,vmin=0,vmax=100))
        self.sols.append(self.settings.New(name='odor2',initial=0,dtype=int,ro=False,vmin=0,vmax=100))
        self.sols.append(self.settings.New(name='odor3',initial=0,dtype=int,ro=False,vmin=0,vmax=100))
        
    def connect(self):
        self._dev=ArduinoSolDev(self.settings.port.value(),
                          self.settings.baud_rate.value(),
                          self.settings.calibration_fname.value())
    
   
    def write(self):
        sol_vals=[]
        for i in range(len(self.sols)):
            x=self.sols[i].value()
            sol_vals.append(int(x))
        
        self._dev.write(sol_vals)
        
    def set_low(self):
        for sol in self.sols:
            sol.update_value(0)
    
    def write_low(self):
        self.set_low()
        self.write()
            
    def write_default(self):
        self.set_low()
        self.sols[0].update_value(100)
        self.write()
            
    def load(self,vals):
        for i in range(len(vals)):
            self.sols[i].update_value(vals[i])
        
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

if __name__ == '__main__':
    ai=DAQaiHW()
    ai.connect()
    print(ai._data)
    time.sleep(1)
    ai.disconnect()