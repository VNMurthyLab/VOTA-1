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
        print("Create Hardware objects")
        from VOTAScopeHW.daq_ai.daq_ai_hw import DAQaiHW
        self.add_hardware(DAQaiHW(self))
        from VOTAScopeHW.arduino_sol.arduino_sol_hw import ArduinoSolHW
        self.add_hardware(ArduinoSolHW(self))
        from VOTAScopeHW.odor_gen.odor_gen_hw import OdorGenHW
        self.add_hardware(OdorGenHW(self))
        from VOTAScopeHW.arduino_wheel.arduino_wheel_hw import ArduinoWheelHW
        self.add_hardware(ArduinoWheelHW(self))
        
        #Add measurement components
        print("Create Measurement objects")
        from VOTAScopeMS.vota_sniff import VOTASniffMeasure
        self.add_measurement(VOTASniffMeasure(self))
#         from VOTAScopeMS.vota_solenoid_test import VOTASolenoidTestMeasure
#         self.add_measurement(VOTASolenoidTestMeasure(self))
        # Connect to custom gui
        
        # load side panel UI
        
        # show ui
        self.ui.show()
        self.ui.activateWindow()
        
        #connect to main interface


if __name__ == '__main__':
    import sys
    
    app = VOTAScopeApp(sys.argv)
    app.hardware['daq_ai'].settings.connected.update_value(True)
    app.hardware['arduino_sol'].settings.connected.update_value(True)
    app.hardware['odor_gen'].settings.connected.update_value(True)
    app.hardware['arduino_wheel'].settings.connected.update_value(True)
    sys.exit(app.exec_())
