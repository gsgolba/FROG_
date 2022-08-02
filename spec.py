import seabreeze.spectrometers as s
import matplotlib.pyplot as plt

MILLI_TO_SEC = 1000
print(s.list_devices())
spec = s.Spectrometer.from_first_available()
plt.figure()
spec.integration_time_micros(10 * MILLI_TO_SEC)
plt.plot(spec.wavelengths(), spec.intensities())
plt.show()