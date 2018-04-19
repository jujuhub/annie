# Pulse counting script for digitizer data output
# by Julie He <juhe@ucdavis.edu>

import numpy as np
import matplotlib.pyplot as plt
import sys

FILE = sys.argv[1] 
SAMPLE_RATE = 500.E6 # S/s
HEADER = 7
THRESHOLD1 = 0.002 # V; 14000 ~= 0.00247V
THRESHOLD2 = 0.003
THRESHOLD3 = 0.004

def main():
	print("Reading file...")
	with open(FILE) as f:
		data = [line.split(' ')[-1] for line in f]

	recordLength = int(data[0])
	frameTime = recordLength/SAMPLE_RATE
	print(frameTime)
	frameCounter = 0
	nPulses1 = 0
	nPulses2 = 0
	nPulses3 = 0

	for i in range(len(data)/(recordLength + HEADER)): # for each frame
		# initialize variables 
		holderArray = []
		frameStart = i*(recordLength+HEADER) + HEADER
		frameEnd = (i+1)*(recordLength+HEADER)

		# initialize pedestal
		ped = 0.
		for val in data[frameStart:frameStart+recordLength/10]:
		# use first 10% of frame to find avg pedestal value
			ped += float(val)
#		print(ped)
		ped = ped/(recordLength/10)
#		print(ped)

		# convert val to int and store in temp array
		for val in data[frameStart:frameEnd]:
			holderArray.append((float(val) - ped)/8192.)

		peak = min(holderArray)
		if abs(peak) > THRESHOLD1:
			nPulses1 += 1
#			plt.plot(holderArray)
#			plt.show()

		if abs(peak) > THRESHOLD2:
			nPulses2 += 1

		if abs(peak) > THRESHOLD3:
			nPulses3 += 1

		frameCounter += 1

	if frameCounter == len(data)/(recordLength + HEADER):
		print("processed all frames")
	else:
		print("did not process all frames")

	print("number of frames: " + str(frameCounter))
	print("number of frames with pulses > 0.002V: " + str(nPulses1) + " / DN: " + str(nPulses1/(frameCounter*frameTime)) + " Hz")
	print("number of frames with pulses > 0.003V: " + str(nPulses2) + " / DN: " + str(nPulses2/(frameCounter*frameTime)) + " Hz")
	print("number of frames with pulses > 0.004V: " + str(nPulses3) + " / DN: " + str(nPulses3/(frameCounter*frameTime)) + " Hz")

	return

if __name__ == '__main__':
	main()
