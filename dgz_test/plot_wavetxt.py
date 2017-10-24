# PMT pulse distribution script for digitizer data

import numpy as np
import matplotlib.pyplot as plt
import sys

FILE = sys.argv[1]
SAVEFILENAME = 'my_charges.txt'

PEAK_VOLTAGE = 0.080 # V ; need to play around with
IMPEDANCE = 50. # Ohms
dT = 2E-9 # s ; sampling interval

# check if file name given 
if len(sys.argv) < 2:
    print("NO FILE INPUT")
    sys.exit(1)

#fileNames = []
#for val in sys.argv[1:]:
#    fileNames.append(val) # make a list of all file name args

#for val in fileNames:
#    try:
#        open(val)       # will be permission error
#    except IOError:
#        print("FILE " + str(val) + " NOT FOUND")
#        sys.exit(1)

#graphNumber = 1

#f = [open(i, 'r') for i in fileNames]

#holderArray = [[] for i in range(len(f))]
#for counter, rows in enumerate(izip(*f)):
#    for valCount, val in enumerate(rows):
#        holderArray[valCount].append(float(val))
#    if (counter + 1)%recordLength == 0


def main():
    # open data file
    print("Reading file...")
    with open(FILE) as f:
        data = [line.split(' ')[-1] for line in f] # reads last column of values into list

    recordLength = int(data[0]) # num samples in one frame

    print("Integrating pulses...")
    holderArray = []
    charge = []
    voltage = 0.0
#    frameStart = 7 # skip header info
#    frameCounter = 0

    j = 7
    while j != len(data): # while we are not at the end of file
        # convert ADC to volts and store in temp list
        holderArray.append(float(data[j] - (2**14)*0.86)*1000./8192.) # 0.86 hard coded
        j += 1 # increment sample counter
        
        if (j-1)%(recordLength + 7) == 0: # if at end of frame
            voltage = sum(holderArray) # sum up area of the frame

            skip_frame = False # initialize skip_frame variable
#            frameCounter += 1 # increment frame count

            # sum pedestal over first 5% of frame
            pedestal = 0
            DC = 0
            for k in range(0, len(holderArray)/20):
                # check for early pulses
                DC = float(DC*(k)) + holderArray[k]/float(k + 1)
                if abs(float(holderArray[k+1]) - DC) > PEAK_VOLTAGE: 
                    # skip entire frame
                    skip_frame == True
                else: # if no peaks, add to pedestal
                    pedestal += float(holderArray[k])
            pedestal *= len(holderArray)/k # fix

            if skip_frame == True:
                print("Skipped frame: " + str(frameCounter))
            else:
                charge.append(-(voltage - pedestal)*dT/IMPEDANCE)

                # plot event
#            plt.ylim((-30, 10)) # V
#            plt.plot(holderArray)
#            plt.show()

            # clear for next event
            holderArray = []
            voltage = 0.0
            j+=7


np.savetxt(('{0}').format(SAVEFILENAME), charge)
