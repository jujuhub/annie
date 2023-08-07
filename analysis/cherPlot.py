import numpy as np
import matplotlib.pyplot as plt

x = np.arange(150., 750., 0.1)
y = 5.25E6/x**2

fig, ax = plt.subplots()

ax.plot(x, y, color='#ff8d33')
ax.fill_between(x[1500:5500], 0, y[1500:5500], alpha=0.5)
ax.set_xlabel('wavelength [nm]')
ax.axhline(0, color='black')
ax.axvline(0, color='black')

plt.show()
