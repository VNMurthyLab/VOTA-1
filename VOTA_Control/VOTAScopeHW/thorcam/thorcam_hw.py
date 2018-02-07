'''
Created on Aug 9, 2017

@author: Hao Wu
'''

from ScopeFoundry import HardwareComponent
from VOTAScopeHW.thorcam.uc480 import uc480
import time

class ThorCamHW(HardwareComponent):
    '''
    Hardware Component Class for receiving AI input for breathing, licking etc
    '''
    
    name='thorcam'

    def setup(self,camera_id=0):
        self.settings.New(name='file_name',dtype=str,initial='D:\Hao\Data\Twitch.avi',ro=True)
                
    def connect(self):
        self._dev=uc480()
        self._dev.connect()
        self._dev.start_live()
        self._dev.set_exposure(10)
        self._dev.set_pixelclock(43)
        self._dev.set_framerate(25.01)
    def read(self):
        return self._dev.read()
    
    def write(self):
        self._dev.write()
    
    def open_file(self):
        self._dev.open_file(self.settings.file_name.value())
    
    def close_file(self):
        self._dev.close_file()
        
    def disconnect(self):
        try:
            self._dev.stop_live()
            self._dev.disconnect()
            del self._dev
            
        except AttributeError:
            pass
        
if __name__ == '__main__':
    ai=DAQaiHW()
    ai.connect()
    print(ai._data)
    time.sleep(1)
    ai.disconnect()