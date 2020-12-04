import numpy as np
import matplotlib.pyplot as plt
import glob
import sys

NEVT = 10
NCH = 6
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
for ch in range(NCH):
  # for each channel
  for s in range(len(data)): 
    y.append(int(data[s][ch+1]))

    if ((len(y)%256) == 0): # if one event complete
      evt += 1
      print("DEBUG: evt: " + str(evt) + " len(y)%256: " + str(len(y)%256))
      plt.plot(y)
      y = [] # reset

    if (evt == NEVT):
      print(str(NEVT) + " evts reached\n")
      break

  plt.title("Chn " + str(ch))
  plt.xlabel("sample no.")
  plt.ylabel("ADC count")
  plt.show()
  # reset for next chn
  y = []
  evt = 0

#print("Num events: " + str(evt))
#"""
