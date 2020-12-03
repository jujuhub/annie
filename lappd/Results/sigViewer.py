import numpy as np
import matplotlib.pyplot as plt
import glob
import sys

DATAFILE = sys.argv[-1]
#print(DATAFILE)

# channel by channel
"""
ch = 0
for ch in range(30):
  for f in glob.glob("Data_*.txt"):
#    print(f)
    data = np.loadtxt(f, delimiter=' ', dtype='int', comments='#', usecols=None)
#  for i in range(len(data)):
    plt.plot(data[ch][3:])
  plt.title("Ch " + str(ch))
  plt.show()
#"""

# event by event
"""
for f in glob.glob("Data_*.txt"):
  print(f)
  data = np.loadtxt(f, delimiter=' ', dtype='int', comments='#', usecols=None)
  for i in range(len(data)):
    plt.plot(data[i][3:])
  plt.title(f)
  plt.show()
"""

# new data format (v0.9d)
#"""
data = np.loadtxt(DATAFILE, delimiter=' ', dtype='string', comments='#', usecols=None)

y = []
evt = 0
for ch in range(30):
  # for each channel
  for s in range(len(data)):
    y.append(int(data[s][ch+1]))
    if ((len(y)%256) == 0):
      plt.plot(y)
      y = []
  plt.title("Chn " + str(ch))
  plt.show()
  y = []
#"""
