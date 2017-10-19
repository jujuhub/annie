# Calculates peak-to-valley ratio
# written by Julie He <juhe@ucdavis.edu>

import numpy as np
import matplotlib.pyplot as plt

import sys
CHARGEDATAFILE=sys.argv[-1]
DATAPATH='.'

N_HIST_BINS=100
NEG_CHARGE=-0.20e-11
DELTA=8
EXTRA=20

def ratio():
	F = open("peak2valley.txt", "a+")
	F2 = open("ET_peak2valley.txt", "a+")
	F3 = open("WB_peak2valley.txt", "a+")

	print("attempting to open " + (DATAPATH + '/{0}').format(CHARGEDATAFILE))
	with open((DATAPATH + '/{0}').format(CHARGEDATAFILE)) as f:
		charge = np.loadtxt(f, dtype=float)

	i=0
	new_charge=[]

	while(i < len(charge)):
	# skip the frames where pulse appears too early
		if(charge[i] > NEG_CHARGE):
			new_charge.append(charge[i])
		else:
			print("skipped " + str(charge[i]))
		i+=1

	new_charge = np.array(new_charge)

	ydata, bin_edges, patches = plt.hist(new_charge, bins=N_HIST_BINS)

	ped_i = 0
	spe_i = 0
	# spe_peak = max(ydata[BIN_END:BIN_END+EXTRA])

	for i in range(50):
		if (ydata[i] == max(ydata)):
			ped_i = i # find index of pedestal

	spe_peak = max(ydata[ped_i+DELTA:ped_i+EXTRA])
	
	for i in range(50):
		if (ydata[i] == spe_peak):
			spe_i = i # find index of SPE peak

	print(spe_peak/min(ydata[ped_i:spe_i]))

	F.write(str(spe_peak/min(ydata[ped_i:spe_i]))+'\n')

	if (CHARGEDATAFILE[:2] == 'WB'): # condition affected by bash script
		F3.write(str(spe_peak/min(ydata[ped_i:spe_i]))+'\n')
	else:
		F2.write(str(spe_peak/min(ydata[ped_i:spe_i]))+'\n')

	return

def main():
	print("running")
	ratio()
	return

if __name__ == '__main__':
	main()
