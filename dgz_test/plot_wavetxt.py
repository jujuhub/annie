import numpy as np
import matplotlib.pyplot as plt
import sys

FILE = sys.argv[1]
SAVEFILENAME = 'my_charges.txt'
IMPEDANCE = 50. # Ohms
dT = 2E-6 # s

if len(sys.argv) < 2:
    print("NO FILE INPUT")
    sys.exit(1)

#fileNames = []
#for val in sys.argv[1:]:
#    fileNames.append(val) # make a list of all file name args

#for val in fileNames:
#    try:
#        open(val)       # will be permission error
#    except:
#        print("FILE " + str(val) + " NOT FOUND")
#        sys.exit(1)

graphNumber = 1

#f = [open(i, 'r') for i in fileNames]

#holderArray = [[] for i in range(len(f))]
#for counter, rows in enumerate(izip(*f)):
#    for valCount, val in enumerate(rows):
#        holderArray[valCount].append(float(val))
#    if (counter + 1)%recordLength == 0

with open(FILE) as f:
    data = [line.split(' ')[-1] for line in f]

recordLength = int(data[0]) # num sample in one frame

holderArray = []
charge = []
voltage = 0.0
pedestal = 0.0

for i in range(len(data)):
    try:
        data[i] = float(data[i])
    except ValueError:
        data[i] = -1

counter = 0

for val in data:
    if (val > 3000. and val < 50000.):
        holderArray.append((val-(2**14)*0.86)*1000./8192.)
        counter += 1
        
        if counter%recordLength == 0: # if at end of frame
            voltage = sum(holderArray)
            pedestal = sum(holderArray[:int(0.05*recordLength)])*20. # fix
            charge.append(-(voltage - pedestal)*dT/IMPEDANCE)

            # plot event
            plt.ylim((-300, 50))
#            plt.plot(holderArray)
#            plt.show()

            # clear for next event
            holderArray = []
            voltage = 0.0
            pedestal = 0.0

    else: # skip header info
#        print(val)

np.savetxt(('{0}').format(SAVEFILENAME), charge)
