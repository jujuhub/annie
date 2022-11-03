# This script is used to look at the pedestal value
# of each frame/event in a data file taken with the
# CAEN DT5730 digitzer

# By: Julie He <juhe@ucdavis.edu>

import sys
import numpy as np
import matplotlib.pyplot as plt
from scipy.optimize import curve_fit

FILE = sys.argv[1]
RECORDLEN = 1030

# FUNCTIONS
def ped_slope(x, m, b):
  return(m*x + b)


with open(FILE) as f:
  print("Reading file...")
  data = f.readlines()

recordLength = 0
header = 0

for line in data[:10]:
  # get num of samples per frame
  if (line[:6] == 'Record'):
    recordLength = int(line.split(' ')[-1])
  # get num of header lines
  try:
    dummy = float(line)
  except ValueError:
    header += 1

if (recordLength == 0): # if no headers
  recordLength = RECORDLEN

holderArray = []
holdEnd = []
frameCounter = 0

for nthframe in range(len(data)/(recordLength + header)):
  ped_ini_part = 0.
  ped_end_part = 0.

  for val in data[nthframe*(recordLength + header) + header:nthframe*(recordLength + header)+ header + recordLength/10]:
    ped_ini_part += float(val)
#  print(ped_ini_part, nthframe)

  for val in data[nthframe*(recordLength + header) + header + 9*recordLength/10:(nthframe+1)*(recordLength + header)-1]:
    ped_end_part += float(val)
#    print(ped_end_part, nthframe)

#  if (0.86*(2**14)*(recordLength/10)-100 < ped_ini_part < 0.86*(2**14)*(recordLength/10)+100):
  holderArray.append(ped_ini_part/(recordLength/10))
  holdEnd.append(ped_end_part/(recordLength/10))

#popt, pcov = curve_fit(ped_slope, range(len(holderArray)), holderArray, p0=[-1.0E-3, 14091.])
#print(popt)

#ped_line_fit = ped_slope(np.array(range(len(holderArray))), *popt)

plt.title("Average Pedestal Value at Beginning and End of Frame\n")
plt.xlabel("initial (avg first 10%)")
plt.ylabel("final (avg last 10%)")
plt.plot(np.array(holderArray), np.array(holdEnd), marker='o', lw='0')
#plt.plot(holderArray)
#plt.plot(ped_line_fit, lw='2')
#plt.savefig("ped_before_after.png")
plt.show()

