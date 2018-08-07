# This is a python script used in conjunction with charges.cc

import sys
import numpy as np
import matplotlib.pyplot as plt
from scipy.optimize import curve_fit

# CONSTANTS
N_HIST_BINS = 100
E_CHARGE = 1.60217662E-19
NEG_CHARGE_CUT = -0.20E-12

# CURVE FIT FUNCTIONS
def gauss(x, mean, sd, n):
	return (n/(np.sqrt(2*np.pi)*sd))*np.exp(-(x-mean)**2/(2*sd**2))

def double_gauss(x, mean, sd, n):
	return (gauss(x, popt_ped[0], popt_ped[1], popt_ped[2]) + (n/(np.sqrt(2*np.pi)*sd))*np.exp(-(x-mean)**2/(2*sd**2)))


def main():
	with open(sys.argv[-1]) as f:
		charge = np.loadtxt(f, dtype=float)

	# skipping VERY negative charge values (early pulses)
	i = 0
	new_charge = []
	counter = 0

	while (i < len(charge)):
		if (charge[i] < NEG_CHARGE_CUT):
			counter += 1
		else:
			new_charge.append(charge[i])
		i += 1

	print(str(counter) + " charges skipped")
	new_charge = np.array(new_charge)

	# make charge distribution histogram
	fig = plt.figure(figsize=(12,8))
	ax1.fig.add_subplot(111)
	plt.yscale('log', nonposy='clip')
	plt.xlabel('charge (C)', fontsize=13)
	plt.ylabel('count', fontsize=13)

	ydata, bins, patches = ax1.hist(new_charge, bins=N_HIST_BINS, facecolor='orage')

	bins=1.E12*bins
	bin_centers = np.array(bins[:-1] + (bins[1]-bins[0])/2.0)

	# bin uncertainties
	uncert_data = []
	for i in range(ydata.size):
		uncert_data.append(np.sqrt(ydata[i]))
		if uncert_data[i] == 0:
			uncert_data[i] = 1

	# pedestal fit
	ped_index = 0
	for i in range(ydata[:35].size):
		if (ydata[i] == max(ydata[:35]):
			ped_index = i # find index of pedestal peak
	iPedStart = 0
	if (ped_index > 8): # arbitrarily chosen numbers
		iPedStart = ped_index - 5

	popt_ped, pcov_ped = curve_fit(gauss, bin_centers[iPedStart:ped_index + 5], ydata[iPedStart:ped_index + 5], p0=[0, 0.5, 2500], sigma=uncert_data[iPedStart:ped_index + 5])

	# spe fit
	spe_index = 0
	for i in range(ydata[ped_index + 8:ped_index + 28]):
		if (ydata[i + ped_index + 8] == max(ydata[ped_index + 8:ped_index + 28])):
			spe_index = i + ped_index + 8
	iSPEStart = ped_index + 8
	if ( (ped_index - spe_index) < 5 ):
		iSPEStart = spe_index - 3

	popt_spe, pcov_spe = curve_fit(gauss, bincenters[iSPEStart:spe_index + 5], ydata[iSPEStart:spe_index + 5], p0=[1.5, 1, 350], sigma=uncert_data[iSPEStart:spe_index + 5])

	
