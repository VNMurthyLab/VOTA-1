'''
Created on Aug 9, 2017

@author: Hao Wu
'''

from ScopeFoundry import HardwareComponent
from .flircam_dev import FLIRCamDev

class FLIRCamHW(HardwareComponent):
    '''
    Hardware Component Class for receiving AI input for breathing, licking etc
    '''
    
    name='flircam'

    def setup(self,camera_sn = ''):
        self.settings.New(name='camera_sn',dtype=str,initial=camera_sn,ro=True)
        self.settings.New(name ='model', dtype = str, initial ='N/A',ro = True)
        self.settings.New(name = 'width', dtype = int, initial = 360, spinbox_step = 4, ro = False)
        self.settings.New(name = 'height', dtype = int, initial = 240, spinbox_step = 4, ro = False)
        self.settings.New(name = 'offset_x', dtype = int, initial = 180, spinbox_step = 4, ro = False)
        self.settings.New(name = 'offset_y', dtype = int, initial = 300, spinbox_step = 4, ro = False)
        self.settings.New(name = 'auto_exposure', dtype = bool, initial = True, ro = False)
        self.settings.New(name = 'exposure_time', dtype = float, initial = 3000, ro = False)
        self.settings.New(name = 'video_mode', dtype = int, initial = 0, ro = False, vmin = 0, vmax = 5)
        
        self.settings.New(name = 'trigger_mode',dtype=bool,initial=False)
        self.settings.New(name = 'hardware_trigger',dtype=bool,initial=False)
        self.settings.New(name = 'frame_rate', dtype = float, initial = 200, ro = False, vmin = 0, vmax = 500)
                
    def connect(self):
        #connect to the camera device
        self._dev=FLIRCamDev(self.settings.camera_sn.value())
        
        #define read functions
        self.settings.model.hardware_read_func = self._dev.get_model
        self.settings.width.hardware_read_func = self._dev.get_width
        self.settings.height.hardware_read_func = self._dev.get_height
        self.settings.offset_x.hardware_read_func = self._dev.get_offset_x
        self.settings.offset_y.hardware_read_func = self._dev.get_offset_y
        self.settings.auto_exposure.hardware_read_func = self._dev.get_auto_exposure
        self.settings.exposure_time.hardware_read_func = self._dev.get_exp
        self.settings.video_mode.hardware_read_func = self._dev.get_video_mode
        self.settings.frame_rate.hardware_read_func = self._dev.get_frame_rate
        self.settings.trigger_mode.hardware_read_func = self._dev.get_trigger_mode
        self.settings.hardware_trigger.hardware_read_func = self._dev.get_hardware_trigger
        
        #define set functions
        self.settings.auto_exposure.hardware_set_func = self._dev.set_auto_exposure
        self.settings.exposure_time.hardware_set_func = self._dev.set_exp
        self.settings.width.hardware_set_func = self._dev.set_width
        self.settings.height.hardware_set_func = self._dev.set_height
        self.settings.offset_x.hardware_set_func = self._dev.set_offset_x
        self.settings.offset_y.hardware_set_func = self._dev.set_offset_y
        self.settings.video_mode.hardware_set_func = self._dev.set_video_mode
        self.settings.frame_rate.hardware_set_func = self._dev.set_frame_rate
        self.settings.trigger_mode.hardware_set_func = self._dev.set_trigger_mode
        self.settings.hardware_trigger.hardware_set_func = self._dev.set_hardware_trigger
        
        #read camera info
        self.settings.trigger_mode.update_value(False)
        self.read_from_hardware()
        
        
    
    def start(self):
        self._dev.start()
    
    def stop(self):
        self._dev.stop()
        
    def read(self,timeout=2000):
        return self._dev.read(timeout)
    
    def empty(self):
        return self._dev.empty()
    
    def write(self):
        self._dev.write()
        
    def to_numpy(self,image):
        return self._dev.to_numpy(image)
        
    def disconnect(self):
        '''
        need bug fix for pointer issues
        '''
        try:
            # remove read functions
            self.settings.model.hardware_read_func = None
            self.settings.width.hardware_read_func = None
            self.settings.height.hardware_read_func = None
            self.settings.auto_exposure.hardware_read_func = None
            self.settings.exposure_time.hardware_read_func = None
            self.settings.video_mode.hardware_read_func = None
            self.settings.frame_rate.hardware_read_func = None
            #remove set functions
            self.settings.auto_exposure.hardware_set_func = None
            self.settings.exposure_time.hardware_set_func = None
            self.settings.video_mode.hardware_set_func = None
            self.settings.frame_rate.hardware_set_func = None
            self.settings.trigger_mode.hardware_set_func = None
            self.settings.hardware_trigger.hardware_set_func = None
            
            self._dev.close()
            del self._dev
            
        except AttributeError:
            pass