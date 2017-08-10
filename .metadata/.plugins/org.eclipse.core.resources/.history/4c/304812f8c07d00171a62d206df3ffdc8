from ScopeFoundry import BaseMicroscopeApp

class VOTAScopeApp(BaseMicroscopeApp):

    # this is the name of the microscope that ScopeFoundry uses 
    # when storing data
    name = 'vota_scope'
    
    # You must define a setup function that adds all the 
    #capablities of the microscope and sets default settings
    
    def setup(self):
        
        #Add App wide settings
        initial_data_save_dir = 'D:\Hao\Data'
        self.settings.get_lq('save_dir').update_value(initial_data_save_dir)


        #Add hardware components
        from VOTAScopeHW.daq_ai.daq_ai_hw import DAQaiHW
        self.add_hardware(DAQaiHW(self))
        
        from VOTAScopeHW.arduino_sol.arduino_sol_hw import ArduinoSolHW
        self.add_hardware(ArduinoSolHW(self))
        
        #Add measurement components
        print("Create Measurement objects")
        from VOTAScopeMS.vota_sniff import VOTASniffMeasure
        self.add_measurement(VOTASniffMeasure(self))
        # Connect to custom gui
        
        # load side panel UI
        
        # show ui
        self.ui.show()
        self.ui.activateWindow()


if __name__ == '__main__':
    import sys
    
    app = VOTAScopeApp(sys.argv)
    sys.exit(app.exec_())