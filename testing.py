import time
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
        serial_num = '26001568'
        motor_name = 'ZFS206'
        DeviceManagerCLI.BuildDeviceList()
        controller = KCubeStepper.CreateKCubeStepper(serial_num)
        if not controller == None:
            controller.Connect(serial_num)
            if not controller.IsSettingsInitialized():
                controller.WaitForSettingsInitialized(3000)
            
            controller.StartPolling(50) #send updates to PC, in ms
            time.sleep(0.1)
            controller.EnableDevice()
            time.sleep(0.1)

        config =  controller.LoadMotorConfiguration(serial_num, DeviceConfiguration.DeviceSettingsUseOptionType.UseFileSettings)
        config.DeviceSettingsName = motor_name
        config.UpdateCurrentConfiguration()
        controller.SetSettings(controller.MotorDeviceSettings, True, False)
        jog_params = controller.GetJogParams()
        jog_params.StepSize = Decimal(2.5)
        jog_params.JogMode = JogParametersBase.JogModes.SingleStep
        controller.SetJogParams(jog_params)

        controller.MoveJog(MotorDirection.Backward, 10000)
        controller.StopPolling()
        controller.Disconnect(False)
if __name__ == "__main__":
    main()
