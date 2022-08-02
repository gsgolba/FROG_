# Get any spectrometer
import seatease.spectrometers as s
import seatease.cseatease as c
import matplotlib.pyplot as plt

spec = s.Spectrometer.from_first_available()
MILLI_TO_SEC = 1000

# List the devices, and instantiate one of them
dev_list = s.list_devices()
print(dev_list) # Prints list of available devices
spec = s.Spectrometer(dev_list[0])
plt.figure()
spec.integration_time_micros(5 * MILLI_TO_SEC)
plt.plot(spec.wavelengths(), spec.intensities())
plt.show()