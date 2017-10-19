import numpy as np
import matplotlib.pyplot as plt
import sys
import os
from scipy import signal
import re
#import fastfilt as ff
#import finder_interface as fi
from scipy import signal
from itertools import izip

# Properties of the pulse of interest

arrayLength = 1030 # 4999 with 50k record length

def is_number(s):
    try:
        float(s)
        return True
    except ValueError:
        return False

if len(sys.argv) < 2:
    print 'NO FILE NAME INPUT'
    sys.exit(1)

fileNames = []
for val in sys.argv[1:]:
    fileNames.append(val)

for val in fileNames:
    try:
        open(val)   # will be a permission error
    except IOError:
        print 'FILE ' + str(val) + ' NOT FOUND'
        sys.exit(1)

graphNumber = 1

f = [open(i, 'r') for i in fileNames]
#tr=fi.reader(fileNames[0])
#finder = fi.pulse_finder('AveragedPulse_wave_280_Trigger8180_Long.txt', old_read=False,zn=20,pn=20,skip=2480,total=)
holderArray = [[] for i in range(len(f))]
for counter, rows in enumerate(izip(*f)):
    for valCount, val in enumerate(rows):
        #if fileNames[valCount] == 'wave7.txt':
        #       holderArray[valCount].append((int(val)-8000)/10. + 8000)
        #else:
        holderArray[valCount].append(float(val))
        if (counter + 1)%arrayLength == 0:
            for countPlots, plotArray in enumerate(holderArray):
                #finder.filter_sample(plotArray, display=True)
                plt.plot(plotArray, linewidth=2, label = str(fileNames[countPlots]))
                print 'INFO ABOUT WAVEFORM: ' + str(fileNames[countPlots])
                print 'MIN: ' + str(min(plotArray)) + ' ADC COUNTS = ' + str(min(plotArray)*1000./8192.) + ' mV'
                print 'MAX: ' + str(max(plotArray)) + ' ADC COUNTS = ' + str(max(plotArray)*1000./8192.) + ' mV'
                print 'AMPLITUDE: ' + str(max(plotArray) - min(plotArray)) + ' ADC COUNTS = ' + str((max(plotArray) - min(plotArray))*1000./8192.) + ' mV'
                #baseline = np.mean(plotArray[0:100])

            #plt.plot(peaksVals, [holderArray[x] for x in peaksVals], 'ro')
            #plt.plot(endVals, [holderArray[x] for x in endVals], 'go')

            #plt.plot([0, arrayLength], [baseline, baseline], color='black', linewidth=2)
                plt.title('GRAPH NUMBER ' + str(graphNumber))
                plt.legend(loc='best')
                plt.show()
                print 'FINISHED DATA BLOCK ' + str(graphNumber)

                graphNumber = graphNumber + 1
                holderArray = [[] for i in range(len(f))]
