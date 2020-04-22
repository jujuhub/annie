# Light Attenuation Study in 1% Gd Solution

""" This script calculates the sigma*beta factor of a material
    as a function of wavelength and plots the resulting curve
    at different times (implicit). Absorbance at 10m is also
    calculated (excluding Cherenkov light).

    written by: Julie He
"""

import glob, sys
import numpy as np
import matplotlib.pyplot as plt
from datetime import date
from scipy.optimize import curve_fit


# check user input
if (len(sys.argv) < 5):
  print("ERROR! Invalid syntax! Usage: 'python lightAtt.py FILE_EXT LAMBDA SURF_AREA VOLUME PLOT [0 or 1] '")
  sys.exit(1)


# global variables
DATAPATH = '/Users/juhe/annie/light_att_study/data/'
QE_EXT = 'r7081_qe'
GD_EXT = '1pct*_Gd'
FILE_EXT = sys.argv[1]
LAMBDA = round(float(sys.argv[2]))
LEN1 = 10. # cm; cuvette length
LEN2 = 1000. # cm; 10m
PLOT_ABS = int(sys.argv[5])


if (LAMBDA < 200.) or (LAMBDA > 750.):
  print("ERROR! Wavelength is out of bounds. Please choose a value between 200. and 750. nm ")
  sys.exit(1)

print("File extension: " + FILE_EXT + "\nWavelength [nm]: " + str(LAMBDA))


# load PMT QE for R7081 model
pmtQE_dict = {}
qeFile = glob.glob(DATAPATH + '../' + QE_EXT + '*.csv')
for line in open(qeFile[0]):
  parts = line.strip().split(',')
  pmtQE_dict[round(float(parts[0]))] = float(parts[1])
#print(pmtQE_dict)


# define SA, V_m / load a dictionary from csv
surfArea = abs(float(sys.argv[3])) # cm2
volGd = abs(float(sys.argv[4])) # mL or cm3
print("Surface area: " + str(surfArea) + " cm2 \nVolume: " + str(volGd) + " cm3 ")


# check directory for files with FILE_EXT
list_of_files = glob.glob(DATAPATH + 'File*' + FILE_EXT + '*.txt')
#print(list_of_files)
print("No. of files detected: " + str(len(list_of_files)))


# Gd spectrum first
gdFile = glob.glob(DATAPATH + 'File*' + GD_EXT + '*.txt')
startDate = (gdFile[0].strip().split('_'))[3]
print("Start date: " + str(startDate))
print("Gd file: " + gdFile[0])

gdAbs = []
for line in open(gdFile[0]):
  parts = line.strip().split(',')
  if (len(parts) == 1) or (parts[1] == '') or (parts[1] == '"Abs."'):
    continue
  else:
    gdA = float(parts[1])
    if (gdA < 0.):
      gdA = 0.
    gdAbs.append(gdA)


# for each data file, load data, perform calculations
dates = []
frac_dict = {}
sigbeta_dict = {}
for f in list_of_files:
  # extract date and calculate num of days from start date
  parts = f.strip().split('_')
  yymmdd = parts[3]
  dates.append(int(yymmdd))
  nDays = (date(2000+int(yymmdd[0:2]), int(yymmdd[2:4]), int(yymmdd[4:6])) - date(2000+int(startDate[0:2]), int(startDate[2:4]), int(startDate[4:6]))).days
  if (nDays == 0):
    nDays = 1

  # lists
  wavelen = []
  Abs = []
  Abs_10m = []
  sigmaBeta = []

  i = 0
  for line in open(f):
    parts = line.strip().split(',')
#    map(str.strip, parts) # map? str? what does this do?
    if (len(parts) == 1) or (parts[1] == '') or (parts[1] == '"Abs."'):
      continue
    else:
      wavelen.append(float(parts[0]))

      A1 = float(parts[1])
      if (A1 < 0):
        A1 = 0.
      Abs.append(A1)

      sb = np.log(10.) * abs(A1-gdAbs[i]) / (surfArea/volGd) / nDays / LEN1
      sigmaBeta.append(sb)

      if (float(parts[0]) == LAMBDA):
        if (LAMBDA < 270.) or (LAMBDA > 723.):
          frac_dict[nDays] = 0.
        else:
          frac_dict[nDays] = 10**(-A1*LEN2/LEN1)*pmtQE_dict[LAMBDA]/100.
        sigbeta_dict[nDays] = sb

      i+=1

  if (PLOT_ABS):
    plt.plot(wavelen, sigmaBeta, label = yymmdd)

print("Fraction of light (no Cherenkov) at 10m at " + str(LAMBDA) + " nm: ")
#for x in frac_dict:
#  print(str(x) + " " + str(frac_dict[x]) + " " + str(sigbeta_dict[x]))
print(sorted(frac_dict.items()))
print("sigma*beta factor at " + str(LAMBDA) + " nm: ")
print(sorted(sigbeta_dict.items()))

# plot each curve and display
#dates.sort()
#plt.plot(*zip(*sorted(frac_dict.items())))
plt.plot(*zip(*sorted(sigbeta_dict.items())))
plt.xlabel("time [d]", fontsize=13)
plt.ylabel("sigma*beta [1/d]", fontsize=13)

#plt.xlim((190, 760))
#plt.xlabel("wavelength [nm]", fontsize=13)
#plt.ylabel("\u03C3\u03B2 [1/day]", fontsize=13)
#plt.legend()
plt.show()
