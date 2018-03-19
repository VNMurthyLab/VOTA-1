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
import h5py

class ArduinoSolHW(HardwareComponent):
    '''
    Hardware Component Class for receiving AI input for breathing, licking etc
    '''
    
    name='arduino_sol'

    def setup(self,port='COM3',baud_rate=500000,fname='D:\\Hao\\VOTA\\VOTA_Control\\VOTAScopeHW\\arduino_sol_8\\calib.h5'):
        '''
        add settings for analog input event
        '''
        self.settings.New(name='port',initial=port,dtype=str,ro=False)
        self.settings.New(name='baud_rate',initial=baud_rate,dtype=int,ro=False)
        self.settings.New(name='calibration_fname',initial=fname,dtype=str,ro=False)
        self.settings.New(name='load_calibration',initial=False,dtype=bool)
        self.settings.New(name='calibration_on', dtype=bool, initial=True,ro=False)
        self.sols=[]

        self.sols.append(self.settings.New(name='clean_air1',initial=0,dtype=int,ro=False,vmin=0,vmax=100))
        self.sols.append(self.settings.New(name='odor1',initial=0,dtype=int,ro=False,vmin=0,vmax=100))
        self.sols.append(self.settings.New(name='odor2',initial=0,dtype=int,ro=False,vmin=0,vmax=100))
        self.sols.append(self.settings.New(name='odor3',initial=0,dtype=int,ro=False,vmin=0,vmax=100))
        self.sols.append(self.settings.New(name='clean_air2',initial=0,dtype=int,ro=False,vmin=0,vmax=100))
        self.sols.append(self.settings.New(name='odor4',initial=0,dtype=int,ro=False,vmin=0,vmax=100))
        self.sols.append(self.settings.New(name='odor5',initial=0,dtype=int,ro=False,vmin=0,vmax=100))
        self.sols.append(self.settings.New(name='odor6',initial=0,dtype=int,ro=False,vmin=0,vmax=100))
        self.load_calib()
        
        self.sols_old = []
        for i in range(8):
            self.sols_old.append(self.sols[i].value())
        
        
    def connect(self):
        self._dev=ArduinoSolDev(self.settings.port.value(),
                          self.settings.baud_rate.value())
    
    def write(self):
        for i in range(len(self.sols)):
            x=self.sols[i].value()
            if (x!=self.sols_old[i]):
                if self.settings.calibration_on.value():
                    self._dev.write(i,int(self.calib[x,i]))
                else:
                    self._dev.write(i,x)
            self.sols_old[i] = x
        
    def set_low(self):
        for counter,sol in enumerate(self.sols):
            sol.update_value(0)
    
    def write_low(self):
        self.set_low()
        self.write()
            
    def write_default(self):
        self.set_low()
        self.sols[0].update_value(0)
        self.sols[4].update_value(0)
        self.write()
            
    def load(self,vals):
        for i in range(len(vals)):
            self.sols[i].update_value(vals[i])
    
    def load_calib(self):
        fname = self.settings.calibration_fname.value()
        calib_file = h5py.File(fname,'r')
        calib_dset = calib_file['calib']
        self.calib = calib_dset[:]
        
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