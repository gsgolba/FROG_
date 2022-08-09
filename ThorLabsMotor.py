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

class Controller:
    def __init__(self, serial_num, motor_name):
        print('starting')
        self.serial_num = serial_num
        self.motor_name = motor_name
        self.controller = KCubeStepper.CreateKCubeStepper(self.serial_num)
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
        self.controller.Home(0)
    def move_relative(self, dis):
        self.controller.SetMoveRelativeDistance(Decimal(dis))
        self.controller.MoveRelative(0)
    def move_absolute(self, pos):
        self.controller.MoveTo(Decimal(pos), 0)
    def disable(self):
        self.controller.DisableDevice()
    def set_jog_step_size(self, step_size):
        jog_params = self.controller.GetJogParams()
        jog_params.StepSize = Decimal(step_size)
        jog_params.JogMode = JogParametersBase.JogModes.SingleStep

        self.controller.SetJogParams(jog_params)
    

