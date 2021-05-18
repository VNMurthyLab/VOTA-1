from numpy import zeros,reshape
from PyDAQmx import *
from queue import Queue
import time

"""This example is a PyDAQmx version of the ContAcq_IntClk.c example
It illustrates the use of callback functions

This example demonstrates how to acquire a continuous amount of
data using the DAQ device's internal clock. It incrementally stores the data
in a Python list.
"""

class DAQaoDev(Task):
    
    def __init__(self,channels='Dev2/ao0'):
        Task.__init__(self)
        self.CreateAOVoltageChan(channels,"",-10.0,10.0,DAQmx_Val_Volts,None)

    def write_data(self,value):
        self.WriteAnalogScalarF64(1,10.0,value/100*4,None)

if __name__ == '__main__':
    task=DAQaoDev()
    task.StartTask()
    input('Acquiring samples continuously. Press Enter to interrupt\n')
    
    task.StopTask()
    task.ClearTask()