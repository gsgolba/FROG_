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

UNIT_CONVERTER = 4.901960784313725
WAIT_TIME = 5000
class Controller:
    def __init__(self, serial_num, motor_name):
        print('starting')
        self.serial_num = serial_num
        self.motor_name = motor_name
        DeviceManagerCLI.BuildDeviceList()
        self.controller = KCubeStepper.CreateKCubeStepper(self.serial_num)
    def connect(self):
        if not self.controller == None:
            self.controller.Connect(self.serial_num)
            if not self.controller.IsSettingsInitialized():
                self.controller.WaitForSettingsInitialized(3000)
            
            self.controller.StartPolling(50) #send updates to PC, in ms
            time.sleep(0.1)
            self.controller.EnableDevice()
            time.sleep(0.1)

        config =  self.controller.LoadMotorConfiguration(self.serial_num, DeviceConfiguration.DeviceSettingsUseOptionType.UseFileSettings)
        config.DeviceSettingsName = str(self.motor_name)
        config.UpdateCurrentConfiguration()
        self.controller.SetSettings(self.controller.MotorDeviceSettings, True, False)


    def disconnect(self):
        self.controller.StopPolling()
        self.controller.Disconnect(False)
    def get_serial_number(self):
        device_info = self.controller.GetDeviceInfo()
        return device_info.SerialNumber
    def get_name(self):
        device_info = self.controller.GetDeviceInfo()
        return device_info.Name
    def get_position(self):
        return Decimal.ToDouble(self.controller.DevicePosition)
    def is_homed(self):
        return self.controller.Status.IsHomed
    def home(self):
        self.wait()
        self.controller.Home(0)
    def move_relative(self, dis):
        self.wait()
        self.controller.SetMoveRelativeDistance(Decimal(dis))
        workDone = InitializeWaitHandler()
        self.controller.MoveRelative(workDone)
    def move_absolute(self, pos):
        self.wait()
        self.controller.MoveTo(Decimal(pos), workDone)
    def disable(self):
        self.controller.DisableDevice()
    def set_jog_step_size(self, step_size):
        jog_params = self.controller.GetJogParams()
        jog_params.StepSize = Decimal(step_size)
        jog_params.JogMode = JogParametersBase.JogModes.SingleStep
        self.controller.SetJogParams(jog_params)
    def get_jog_step_size(self):
        self.wait()
        return self.controller.GetJogStepSize()
    def jog_forward(self):
        self.wait()
        self.controller.MoveJog(MotorDirection.Forward, workDone)
    def jog_backward(self):
        self.wait()
        self.controller.MoveJog(MotorDirection.Backward, workDone)
    def wait(self, waitTimeout = WAIT_TIME):
        if self.controller.IsDeviceBusy():
            self.controller.Wait(waitTimeout)
            self.wait()

def main():
    myController = Controller(str('26001568'), str('ZST225'))
    myController.connect()
    myController.set_jog_step_size(1.0)
    print('my step size: ', myController.get_jog_step_size())
    myController.jog_forward()
    time.sleep(2)
    #print(myController.get_position())
    myController.jog_backward()
    myController.disconnect()

if __name__ == "__main__":
    main()