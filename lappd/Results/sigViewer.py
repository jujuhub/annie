import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import glob
import time
import sys

DATAFILE = sys.argv[1]
#print(DATAFILE)
FRAMESIZE = 256

MAX_NEVT = 500
NEVT = 10
if (len(sys.argv) > 2):
  if (int(sys.argv[2]) < 1 or int(sys.argv[2]) > MAX_NEVT):
    print("error! invalid number of evts! you entered: " + sys.argv[2])
  else:
    NEVT = int(sys.argv[2])
print("Num of events to process: " + str(NEVT))

NCH = 10
if (len(sys.argv) > 3):
#  print(type(sys.argv[3]))
  if (int(sys.argv[3]) < 0 or int(sys.argv[3]) > 30):
    print("error! invalid number of chns! you entered: " + sys.argv[3])
  else:
    NCH = int(sys.argv[3])
print("Num of channels to process: " + str(NCH))

GROUP_EVTS = False
PLOT_NEVTS = 10
if (len(sys.argv) > 4):
  if (int(sys.argv[4]) < 0):
    print("error! invalid number of evts per plot! you entered: " + sys.argv[4])
  else:
    GROUP_EVTS = True
    PLOT_NEVTS = int(sys.argv[4])
  print("Plotting  " + str(PLOT_NEVTS) + "  per plot")
  print("Processing Chn " + str(NCH))

##### NEW DATA FORMAT #####
#"""
#data = np.loadtxt(DATAFILE, delimiter=' ', dtype='string', comments='#', usecols=None)

data = pd.read_csv(DATAFILE, sep=' ', header=None, 
                   names=["sample", 
                          "Chn1","Chn2","Chn3","Chn4","Chn5",
                          "Chn6","Chn7","Chn8","Chn9","Chn10",
                          "Chn11","Chn12","Chn13","Chn14","Chn15",
                          "Chn16","Chn17","Chn18","Chn19","Chn20",
                          "Chn21","Chn22","Chn23","Chn24","Chn25",
                          "Chn26","Chn27","Chn28","Chn29","Chn30",
                          "meta","nan"])

#ax = plt.gca()

# NEVT events for a specific channel NCH
if (GROUP_EVTS):
  for evt in range(NEVT):
    ax = plt.gca()
    e = data.iloc[evt*FRAMESIZE:(evt+1)*FRAMESIZE, [0,NCH]]
    e.plot(x="sample", ax=ax, legend=False)
    
    if (((evt+1)%PLOT_NEVTS == 0) or (evt == NEVT-1)):
      print("events processed: " + str(evt+1))
      plt.title("Chn " + str(NCH))
      plt.xlabel("sample no.")
      plt.ylabel("ADC count")
      plt.show(block=False)
      plt.pause(1)
      plt.close()

# NEVT events for NCH channels
else:
  for ch in range(1, NCH+1): # for each channel
    ax = plt.gca()
    for evt in range(NEVT):
      e = data.iloc[evt*FRAMESIZE:(evt+1)*FRAMESIZE, [0,ch]]
      e.plot(x="sample", ax=ax, legend=False)
#      print("debug")
    print("showing " + str(NEVT) + " evts for chn " + str(ch))

    plt.title("Chn " + str(ch))
    plt.xlabel("sample no.")
    plt.ylabel("ADC count")
#    plt.legend('', frameon=False)
    plt.show(block=False)
    plt.pause(1)
    plt.close()

#print("Num events: " + str(evt))
#"""


##### OLD DATA FORMAT #####
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
