'''
Created on Aug 9, 2017

@author: Hao Wu
'''

from ScopeFoundry import HardwareComponent
from .daq_ao_dev import DAQaoDev
from PyDAQmx import *
import numpy as np
import time

class DAQaoHW(HardwareComponent):
    '''
    Hardware Component Class for receiving AI input for breathing, licking etc
    '''
    
    name='daq_ao'

    def setup(self,channel='Dev2/ao0'):
        '''
        add settings for analog input eventsss
        '''
        self.settings.New(name='channel',initial=channel,dtype=str,ro=False)
        self.settings.New(name='voltage',initial=80,dtype=float,ro=False,vmin=0,vmax=100)
                
    def connect(self):
        self._dev=DAQaoDev(self.settings.channel.value())
        
        self.settings.voltage.hardware_set_func = self._dev.write_data
        self._dev.StartTask()
        
    def start(self):
        self._dev.StartTask()
        
    def stop(self):
        self._dev.StopTask()
        
    def disconnect(self):
        try:
            self._dev.StopTask()
            self._dev.ClearTask()
            del self._dev
            del self.write_data
            
        except AttributeError:
            pass
        
if __name__ == '__main__':
    ai=DAQaoHW()
    ai.connect()
    time.sleep(1)
    ai.disconnect()