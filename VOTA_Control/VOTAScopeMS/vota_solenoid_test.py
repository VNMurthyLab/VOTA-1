'''
Created on Aug 9, 2017

@author: Lab Rat
'''
from math import sqrt
from ScopeFoundry import Measurement
from ScopeFoundry.helper_funcs import sibling_path, load_qt_ui_file
from ScopeFoundry import h5_io
import pyqtgraph as pg
import numpy as np
import time
from random import randint,random

class VOTASolenoidTestMeasure(Measurement):
    
    # this is the name of the measurement that ScopeFoundry uses 
    # when displaying your measurement and saving data related to it    
    name = "vota_solenoid_test"
    
    def setup(self):
        """
        Runs once during App initialization.
        This is the place to load a user interface file,
        define settings, and set up data structures. 
        """
        
        # Define ui file to be used as a graphical interface
        # This file can be edited graphically with Qt Creator
        # sibling_path function allows python to find a file in the same folder
        # as this python module
        self.ui_filename = sibling_path(__file__, "ai_plot.ui")
        
        #Load ui file and convert it to a live QWidget of the user interface
        self.ui = load_qt_ui_file(self.ui_filename)

        # Measurement Specific Settings
        # This setting allows the option to save data to an h5 data file during a run
        # All settings are automatically added to the Microscope user interface
        self.settings.New('save_h5', dtype=bool, initial=False)
        self.settings.New('tdelay', dtype=int, initial=80,ro=True)
        self.settings.New('vmin',dtype=int,initial=700)
        self.settings.New('vmax',dtype=int,initial=2000)
        #self.settings.New('sampling_period', dtype=float, unit='s', initial=0.005)
        
        # Create empty numpy array to serve as a buffer for the acquired data
        #self.buffer = np.zeros(10000, dtype=float)
        
        # Define how often to update display during a run
        self.display_update_period = 0.1 
        
        # Convenient reference to the hardware used in the measurement
        self.daq_ai = self.app.hardware['daq_ai']
        self.arduino_sol =self.app.hardware['arduino_sol']
        self.odor_gen =self.app.hardware['odor_gen']


    def setup_figure(self):
        """
        Runs once during App initialization, after setup()
        This is the place to make all graphical interface initializations,
        build plots, etc.
        """
        
        # connect ui widgets to measurement/hardware settings or functions
        self.ui.start_pushButton.clicked.connect(self.start)
        self.ui.interrupt_pushButton.clicked.connect(self.interrupt)
        self.settings.save_h5.connect_to_widget(self.ui.save_h5_checkBox)
        
        # Set up pyqtgraph graph_layout in the UI
        self.graph_layout=pg.GraphicsLayoutWidget()
        self.ui.plot_groupBox.layout().addWidget(self.graph_layout)

        # Create PlotItem object (a set of axes)  
        self.plot1 = self.graph_layout.addPlot(row=1,col=1,title="PID",pen='r')
        self.plot2 = self.graph_layout.addPlot(row=2,col=1,title="PID vs target")
        self.plot3 = self.graph_layout.addPlot(row=3,col=1,title="Lick")
        self.plot4 = self.graph_layout.addPlot(row=4,col=1,title="Odor Output Target")
        # Create PlotDataItem object ( a scatter plot on the axes )
        self.plot_line1 = self.plot1.plot([0])    
        self.plot_line2 = self.plot2.plot([0])
        self.plot_line3 = self.plot3.plot([0])
             
        self.odor_plot_line1 = self.plot4.plot([0])  
        self.odor_plot_line2 = self.plot4.plot([1])  
        self.odor_plot_line3 = self.plot4.plot([2])  
        self.odor_plot_line4 = self.plot4.plot([3])  
        self.target_odor_line = self.plot2.plot([1])
        
        self.plot_line1.setPen('r')
        self.plot_line2.setPen('g')
        self.plot_line3.setPen('b')
        self.odor_plot_line1.setPen('r')
        self.odor_plot_line2.setPen('g')
        self.odor_plot_line3.setPen('b')
        self.odor_plot_line4.setPen('y')
        self.T=np.linspace(0,10,10000)
        self.k=0
    
    def update_display(self):
        """
        Displays (plots) the numpy array self.buffer. 
        This function runs repeatedly and automatically during the measurement run.
        its update frequency is defined by self.display_update_period
        """
        self.plot_line1.setData(self.k+self.T,self.buffer[:,0]) 
        self.plot_line2.setData(self.k+self.T,self.buffer[:,0]) 
        self.plot_line3.setData(self.k+self.T,self.buffer[:,2])
        self.odor_plot_line1.setData(self.k+self.T,self.buffer[:,3]) 
        self.odor_plot_line2.setData(self.k+self.T,self.buffer[:,4]) 
        self.odor_plot_line3.setData(self.k+self.T,self.buffer[:,5])
        self.odor_plot_line4.setData(self.k+self.T,self.buffer[:,6])
        self.target_odor_line.setData(self.k+self.T,self.buffer[:,5]/100)
        #print(self.buffer_h5.size)
    
    def run(self):
        """
        Runs when measurement is started. Runs in a separate thread from GUI.
        It should not update the graphical interface directly, and should only
        focus on data acquisition.
        """
        num_of_chan=self.daq_ai.settings.num_of_chan.value()
        self.buffer = np.zeros((10000,num_of_chan+4), dtype=float)
        self.buffer[0:self.settings.tdelay.value(),3]=100;
        self.odor_gen.make_ladder_speed(self.settings.vmin.value(),self.settings.vmax.value())
        
        # first, create a data file
        if self.settings['save_h5']:
            # if enabled will create an HDF5 file with the plotted data
            # first we create an H5 file (by default autosaved to app.settings['save_dir']
            # This stores all the hardware and app meta-data in the H5 file
            self.h5file = h5_io.h5_base_file(app=self.app, measurement=self)
            
            # create a measurement H5 group (folder) within self.h5file
            # This stores all the measurement meta-data in this group
            self.h5_group = h5_io.h5_create_measurement_group(measurement=self, h5group=self.h5file)
            
            # create an h5 dataset to store the data
            self.buffer_h5 = self.h5_group.create_dataset(name  = 'buffer', 
                                                          shape = self.buffer.shape,
                                                          dtype = self.buffer.dtype,
                                                          maxshape=(None,self.buffer.shape[1]))
        
        # We use a try/finally block, so that if anything goes wrong during a measurement,
        # the finally block can clean things up, e.g. close the data file object.
        try:
            i = 0
            j = 0
            self.k=0
            step_size=self.daq_ai.settings.buffer_size.value()
           
            self.daq_ai.start()
            
            # Will run forever until interrupt is called.
            while not self.interrupt_measurement_called:
                i %= self.buffer.shape[0]
                if self.settings['save_h5']:
                    if j>(self.buffer_h5.shape[0]-step_size):
                        self.buffer_h5.resize((self.buffer_h5.shape[0]+self.buffer.shape[0],self.buffer.shape[1]))
                        self.k +=10
                if (i%25==0):
                    self.odor_gen.random()
                # Set progress bar percentage complete
                self.settings['progress'] = i * 100./self.buffer.shape[0]
                
                # Fills the buffer with sine wave readings from func_gen Hardware
                self.buffer[i:(i+step_size),0:num_of_chan] = self.daq_ai.read_data()
                
                if self.odor_gen.buffer_empty():
                    odor_value=[0,0,0,0]
                    odor_disp_value=odor_value
                else:
                    odor_value_packet=self.odor_gen.read()
                    odor_value=odor_value_packet[0]
                    odor_disp_value=odor_value_packet[1]
                     
                tdelay=self.settings.tdelay.value()
#                 if i>self.buffer.shape[0]-tdelay-step_size:
#                     wrap=i-self.buffer.shape[0]+tdelay
#                     
#                     self.buffer[wrap:(wrap+step_size),num_of_chan:(num_of_chan+4)]=odor_disp_value
#                 else:
#                     self.buffer[(i+tdelay):(i+tdelay+step_size),num_of_chan:(num_of_chan+4)]=odor_disp_value
#                 #self.arduino_sol._dev.write(odor_value)
#                 odor_disp_value=[]
#                 for sol in self.arduino_sol.sols:
#                     odor_disp_value.append(sol.value())
                self.buffer[i:(i++step_size),num_of_chan:(num_of_chan+4)]=odor_disp_value
                for i in range(4):
                    self.arduino_sol.sols[i].update_value(odor_value[i])
                self.arduino_sol.write()
#                  
                
                if self.settings['save_h5']:
                    # if we are saving data to disk, copy data to H5 dataset
                    self.buffer_h5[j:(j+step_size),:] = self.buffer[i:(i+step_size),:]
                    # flush H5
                    self.h5file.flush()
            
                
                # wait between readings.
                # We will use our sampling_period settings to define time
                #time.sleep(self.settings['sampling_period'])
                
                i += step_size
                j += step_size
               
                
                if self.interrupt_measurement_called:
                    # Listen for interrupt_measurement_called flag.
                    # This is critical to do, if you don't the measurement will
                    # never stop.
                    # The interrupt button is a polite request to the 
                    # Measurement thread. We must periodically check for
                    # an interrupt request
                    self.arduino_sol.write_low()
                    self.daq_ai.stop()
                    self.odor_gen.flush()
                    break

        finally:            
            if self.settings['save_h5']:
                # make sure to close the data file
                self.h5file.close()
