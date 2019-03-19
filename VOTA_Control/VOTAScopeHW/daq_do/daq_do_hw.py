'''
Created on Aug 9, 2017

@author: Hao Wu
'''

from ScopeFoundry import HardwareComponent
from .daq_do_dev import DAQSimpleDOTask
from PyDAQmx import *
import numpy as np
import time

class DAQdoHW(HardwareComponent):
    '''
    Hardware Component Class for receiving AI input for breathing, licking etc
    '''
    
    name='daq_do'

    def setup(self,channels='Dev2/port0/line2'):
        '''
        add settings for analog input eventsss
        '''
        self.settings.New(name='channels',initial=channels,dtype=str,ro=False)
        self.settings.New(name='on',initial=False,dtype=bool,ro=False)

        
                
    def connect(self):
        self._dev=DAQSimpleDOTask(self.settings.channels.value())
        self.settings.on.hardware_set_func = self._dev.write_bool

        
    def disconnect(self):
        try:
            self._dev.StopTask()
            self._dev.ClearTask()
            del self._dev
            
        except AttributeError:
            pass
        
if __name__ == '__main__':
    ai=DAQdoHW()
    ai.connect()
    print(ai._data)
    time.sleep(1)
    ai.disconnect()