from ScopeFoundry import BaseMicroscopeApp
from PyQt5.QtGui import QColor

class VOTAScopeApp(BaseMicroscopeApp):

    # this is the name of the microscope that ScopeFoundry uses 
    # when storing data
    name = 'vota_scope'
    
    # You must define a setup function that adds all the 
    #capablities of the microscope and sets default settings
    
    def setup(self):
        
        #Add App wide settings
        initial_data_save_dir = 'D:\Hao\Data'
        self.settings.save_dir.update_value(initial_data_save_dir)


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
        from VOTAScopeHW.arduino_water.arduino_water_hw import ArduinoWaterHW
        self.add_hardware(ArduinoWaterHW(self))
        from VOTAScopeHW.camera.camera_hw import CameraHW
        self.add_hardware(CameraHW(self))
        
        #Add measurement components
        print("Create Measurement objects")
        from VOTAScopeMS.vota_calibration import VOTACalibrationMeasure
        self.add_measurement(VOTACalibrationMeasure(self))
        from VOTAScopeMS.lick_training import VOTALickTrainingMeasure
        self.add_measurement(VOTALickTrainingMeasure(self))
        from VOTAScopeMS.vota_sniff import VOTASniffMeasure
        self.add_measurement(VOTASniffMeasure(self))
#         from VOTAScopeMS.vota_solenoid_test import VOTASolenoidTestMeasure
#         self.add_measurement(VOTASolenoidTestMeasure(self))
        # Connect to custom gui
        
        # load side panel UI
        
        # show ui
        self.ui.show()
        self.ui.activateWindow()
        
        w=self.ui
        p = w.palette()
        p.setColor(w.backgroundRole(), QColor(0,0,0))
        w.setPalette(p)
        #connect to main interface


if __name__ == '__main__':
    import sys
    
    app = VOTAScopeApp(sys.argv)
    app.ui.setWindowTitle("Virtual Odor Tracking Arena")
    
    app.hardware['daq_ai'].settings.connected.update_value(True)
    app.hardware['arduino_sol'].settings.connected.update_value(True)
    app.hardware['odor_gen'].settings.connected.update_value(True)
    app.hardware['arduino_wheel'].settings.connected.update_value(True)
    app.hardware['arduino_water'].settings.connected.update_value(True)
    app.hardware['camera'].settings.connected.update_value(True)
    
    sys.exit(app.exec_())
