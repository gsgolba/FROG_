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