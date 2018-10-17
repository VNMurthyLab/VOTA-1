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

    def setup(self,light_channel='Dev2/port0/line1',camera_channel='Dev2/port0/line0'):
        '''
        add settings for analog input eventsss
        '''
        self.settings.New(name='light_channel',dtype=str,initial=light_channel)
        self.settings.New(name='camera_channel',dtype=str,initial=camera_channel)
        self.settings.New(name='light_switch',initial=False,dtype=bool,ro=False)
        self.settings.New(name='camera_switch',initial=False,dtype=bool,ro=False)
    
    def connect(self):
        self._light = DAQSimpleDOTask(self.settings.light_channel.value())
        self._camera = DAQSimpleDOTask(self.settings.camera_channel.value())
        self.settings.light_switch.connect_to_hardware(write_func=self._light.write_bool)
        self.settings.camera_switch.connect_to_hardware(write_func=self._camera.write_bool)
        
    def disconnect(self):
        try:
            self._light.close()
            self._camera.close()
            self.settings.light_switch.connect_to_hardware(write_func=None)
            self.settings.camera_switch.connect_to_hardware(write_func=None)
            del self._light
            del self._camera
            
        except AttributeError:
            pass