from tkinter import Y
import matplotlib.pyplot as plt
import numpy as np
import spectrometer
spec = spectrometer.Virtual_Spectrometer()
wavelength, intensity = spec.get_both()
#use intensity as a measure for matshow.
#we need to to know how many steps we do in our
# delay path
DELAY_PATH_STEPS=10
our_matrix = np.zeros((len(wavelength),DELAY_PATH_STEPS))
fig, ax = plt.subplots()
#ax.set_yticks(np.linspace(wavelength[0], wavelength[-1], 20))
#spec.change_integration_time(1000)
for i in range(DELAY_PATH_STEPS):
    intensity = spec.get_intensities()
    our_matrix[:, i] = intensity
ax.imshow(our_matrix, aspect='auto', extent=[0,10,wavelength[-1], wavelength[0]])
plt.show()


