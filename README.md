# FROG_
Creating an API for spectrometer and motor controller
**Currently only compatible with Windows OS**

# Necessary Downloads
* Download Thorlabs kinesis software for the DLLS: https://www.thorlabs.com/software_pages/ViewSoftwarePage.cfm?Code=Motion_Control&viewtab=0
  * There is a file called Thorlabs.MotionControl.DotNet_API.chm which is basically the documentation for all the functions that the motor controller software provides
* A couple of Python libraries to import:
  * tkinter
  * seabreeze
  * seatease
  * pythonnet

# Some GOATED githubs:
* [SeaBreeze](https://github.com/ap--/python-seabreeze): Lets you use Ocean Optics spectrometer through python
* [SeaTease](https://github.com/jonathanvanschenck/python-seatease): Simulates Ocean Optics spectrometer to test code without need of physical spectrometer
* [ThorLabs Motor Stepper](https://github.com/rwalle/py_thorlabs_ctrl/blob/master/py_thorlabs_ctrl/kinesis/motor.py): Code to interface with Thorlabs motor via python. Not exactly what I implemented, but helpful reference to functions in the Thorlabs dll.

# Known Issues
* Stepper Motor Controller doesn't seem to move correct amount after setting jog size (We set jog step size to 0.5, the jog step size with be registered to 0.102). Possible issue with Unit Converter and not recognizing that stage the motor is connected to (though we set the motor name in our initialization). Also not connected to stage yet, so this may just be an issue with using an isolated controller.
* Stepper Motor seems to be moving backwards when jogging forward and vice versa. May be due to not being homed.
## Both issues above seem to only be happening with the Dell computer. Using the exact same commit on the virtual machine results in no problem
* Haven't implemented anything to ensure that the frog wont use the same intensity reading for two steps if the integration time is much larger than the time it takes for the motor to move.
* Still need to implement the threshold data
* I should definitely change the refresh rate of the gui to just the same as the integration time of the spectrometer.
