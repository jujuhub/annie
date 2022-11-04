# Plots absorption at a certain wavelength over time
# by: Julie He <juhe@ucdavis.edu>

import numpy as np
import matplotlib.pyplot as plt
import sys

FILE=sys.argv[1]
WAVELENGTH=sys.argv[2]
MATERIAL=sys.argv[3]

with open(FILE) as f:
	data = np.loadtxt(f, delimiter=",", usecols=(1,))

plt.title(str(MATERIAL) + ": abs at " + str(WAVELENGTH) + " nm")
plt.xlabel("time [weeks]")
plt.ylabel("abs")
plt.xlim(0,25)
#plt.ylim(0, 0.25)
plt.plot(data,'bo')
plt.savefig("plots/" + str(MATERIAL) + "_" + str(WAVELENGTH) + "nm.png")
#plt.show()
