'''
Created on Mar 29, 2018

@author: Hao Wu
'''
import PySpin
import os
import time
class AviType(object):
    """'Enum' to select AVI video type to be created and saved"""
    UNCOMPRESSED = 0
    MJPG = 1
    H264 = 2

class Recorder(object):
    '''
    PySpin AVI recorder binding
    '''
    def __init__(self, fname, frame_rate, compress = True, width = 1024, height = 1024):
        self.fname = fname
        self.frame_rate = frame_rate
        
        #setup option for AVIRecorder
        if compress:
            chosenAviType = AviType.H264
            option = PySpin.H264Option()
            option.frameRate = self.frame_rate
            option.bitrate = 2560000
            option.height = height
            option.width = width
        else:
            chosenAviType = AviType.UNCOMPRESSED
            option = PySpin.AVIOption()
            option.frameRate = self.frame_rate
            
        
        #create instance for recorder    
        self.rec = PySpin.SpinVideo()
        
        if os.path.exists(self.fname + '-0000.avi'):
            print("File already exists, saving with timestamp")
            timestamp =time.strftime('%H%M%S',time.localtime())
            self.fname = self.fname + timestamp
        #create file
        try:
            self.rec.Open(self.fname,option)
        except PySpin.SpinnakerException as ex:
            print("Error: %s" % ex)
        
    def save_frame(self,image):
        try:
            self.rec.Append(image)
        except PySpin.SpinnakerException as ex:
            print("Error: %s" % ex)
            
        
    def close(self):
        self.rec.Close()
    
class FLIRRecDev(object):
    '''
    Virtual Device that hold a list of running recorders
    '''
    def __init__(self, path):
        self.path = path
        self.recorder = dict()
    
    def get_path(self,path):
        return self.path
    
    def set_path(self,path):
        self.path = path
    
    def create_file(self, name, frame_rate, compress = True, width = 1024, height = 1024):
        fname = os.path.join(self.path,name)
        self.recorder[name] = Recorder(fname, frame_rate, compress, width, height)
        
    def save_frame(self,name, image):
        if name in self.recorder:
            self.recorder[name].save_frame(image)
        else:
            print(name + ' recorder does not exist or already closed.')
    
    def close_file(self,name):
        if name in self.recorder:
            self.recorder[name].close()
            del self.recorder[name]
        else:
            print(name + ' recorder does not exist or already closed..')
            
    def close(self):
        for name in self.recorder:
            self.recorder[name].close()
            

        
        