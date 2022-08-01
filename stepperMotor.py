import time
import numpy as np
import clr
clr.AddReference("C:\Program Files\Thorlabs\Kinesis\Thorlabs.MotionControl.DeviceManagerCLI.dll")
clr.AddReference("C:\Program Files\Thorlabs\Kinesis\Thorlabs.MotionControl.GenericMotorCLI.dll")
clr.AddReference("C:\Program Files\Thorlabs\Kinesis\Thorlabs.MotionControl.KCube.StepperMotorCLI.dll")
from Thorlabs.MotionControl.DeviceManagerCLI import *
from Thorlabs.MotionControl.GenericMotorCLI import *
from Thorlabs.MotionControl.GenericMotorCLI import KCubeMotor
from Thorlabs.MotionControl.GenericMotorCLI.ControlParameters import JogParametersBase
from Thorlabs.MotionControl.KCube.StepperMotorCLI import *
from System import Decimal

class Controller:
    def __init__(self,serial_num, motor_name):
        print('starting')
        DeviceManagerCLI.BuildDeviceList()
        self.serial_num = serial_num
        self.motor_name = motor_name
        self.controller = KCubeStepper.CreateKCubeStepper(self.serial_num)
        print('connecting')
        self.connect()
        print('jogging')
        self.jog_test()
        print('disconnecting')
        self.disconnect()



    def connect(self):
        if not self.controller == None:
            self.controller.Connect(self.serial_num)

            if not self.controller.IsSettingsInitiailized():
                self.controller.WaitForSettingsInitialized(3000)
            
            self.controller.StartPolling(50) #send updates to PC, in ms
            time.sleep(0.1)
            self.controller.EnableDevice()
            time.sleep(0.1)

        config =  self.controller.LoadMotorConfiguration(self.serial_num, DeviceConfiguration.DeviceSettingsUseOptionType.UseFileSettings)
        config.DeviceSettingsName = self.motor_name
        config.UpdateCurrentConfiguration()
        self.controller.SetSettings(self.controller.MotorDeviceSettings, True, False)

    def jog_test(self):
        jog_params = self.controller.GetJogParams()

        jog_params.StepSize = Decimal(0.5)
        jog_params.MaxVelocity = Decimal(10)
        jog_params.JogMode = JogParametersBase.JogModes.SingleStep

        self.controller.SetJogParams(jog_params)

        print("Moving Motor")
        self.controller.MoveJog(MotorDirection.Forward, 10000)
        self.controller.MoveTo_DeviceUnit(0, 70000)
    def disconnect(self):
        self.controller.StopPolling()
        self.controller.Disconnect(False)

            




def main():
    serial_num = str("26001568")
    print("starting")
    DeviceManagerCLI.BuildDeviceList()
    print("built device list")
    controller = KCubeStepper.CreateKCubeStepper(serial_num)

    if not controller == None: #I don't like the use of a double negative but kept for now
        controller.Connect(serial_num)

        if not controller.IsSettingsInitialized(): #if not yet initialized, just wait a bit
            controller.WaitForSettingsInitialized(3000) #in ms
        
        controller.StartPolling(50) #send updates to PC, in ms
        time.sleep(.1) #in sec
        controller.EnableDevice()
        time.sleep(.1)

        config =  controller.LoadMotorConfiguration(serial_num, DeviceConfiguration.DeviceSettingsUseOptionType.UseFileSettings)
        config.DeviceSettingsName = str("KST101")
        config.UpdateCurrentConfiguration()
        controller.SetSettings(controller.MotorDeviceSettings, True, False)

        #print("Homing Motor")
        #controller.Home(60000)

        jog_params = controller.GetJogParams()

        jog_params.StepSize = Decimal(0.5)
        jog_params.MaxVelocity = Decimal(10)
        jog_params.JogMode = JogParametersBase.JogModes.SingleStep

        controller.SetJogParams(jog_params)

        print("Moving Motor")
        controller.MoveJog(MotorDirection.Forward, 10000)
        controller.MoveTo_DeviceUnit(0, 70000)

        controller.StopPolling()
        controller.Disconnect(False)



if __name__ == '__main__':
    main()