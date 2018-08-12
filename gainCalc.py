# This is a python script used in conjunction with charges.cc
# Written by: Julie He <juhe@ucdavis.edu>
# Last updated: Aug 11, 2018

import sys
import numpy as np
import matplotlib.pyplot as plt
from scipy.optimize import curve_fit

# CONSTANTS
N_HIST_BINS = 100
E_CHARGE = 1.60217662E-19 # C
NEG_CHARGE_CUT = -0.20E-12

# CURVE FIT FUNCTIONS
def gauss(x, mean, sd, n):
	return (n/(np.sqrt(2*np.pi)*sd))*np.exp(-(x-mean)**2/(2*sd**2))

def double_gauss(x, mean, sd, n):
	return (gauss(x, popt_ped[0], popt_ped[1], popt_ped[2]) + (n/(np.sqrt(2*np.pi)*sd))*np.exp(-(x-mean)**2/(2*sd**2)))

# MAIN
def main(filename):
	with open(filename) as f:
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
	ax1 = fig.add_subplot(111)
#	plt.yscale('log', nonposy='clip')
#	plt.xlabel('charge (C)', fontsize=13)
#	plt.ylabel('count', fontsize=13)

	ydata, bins, patches = ax1.hist(new_charge, bins=N_HIST_BINS, facecolor='orange')

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
	for i in range(ydata.size):
		if (ydata[i] == max(ydata)):
			ped_index = i # find index of pedestal peak
#	iPedStart = 0
#	if (ped_index > 8): # arbitrarily chosen numbers
#		iPedStart = ped_index - 5
	ped_end_index = ped_index + 5

	popt_ped, pcov_ped = curve_fit(gauss, bin_centers[:ped_end_index], ydata[:ped_end_index], p0=[0, 0.5, 2500], sigma=uncert_data[:ped_end_index])

	ped_fit = gauss(bin_centers, *popt_ped)

	# spe fit
	spe_index = 0
	for i in range(ydata[ped_end_index:ped_end_index + 10].size):
		if (ydata[i + ped_end_index] == max(ydata[ped_end_index:ped_end_index + 10])):
			spe_index = i + ped_end_index
	spe_end_index = spe_index + 5

	popt_spe, pcov_spe = curve_fit(gauss, bin_centers[ped_end_index:spe_end_index], ydata[ped_end_index:spe_end_index], p0=[1.5, 1, 350], sigma=uncert_data[ped_end_index:spe_end_index])	

	spe_fit = gauss(bin_centers, *popt_spe)

	bin_centers = bin_centers*1E-12
	gain = (popt_spe[0] - popt_ped[0])*1E-12/E_CHARGE

	valley_index = 0
	for i in range(ydata[:spe_index].size):
		if ydata[i] == min(ydata[ped_index:spe_index]):
			valley_index = i + ped_index
	p2v = ydata[spe_index]/ydata[valley_index]
			
	print("Gain = " + str(gain))
	print("Peak-to-valley ratio = " + str(p2v))

	# plotting
#	plt.figure(figsize=(12,8))
	plt.title("Charge Distribution with Peak Fitting\n", fontsize=17)
	plt.xlabel("charge (C)", fontsize=15)
	plt.ylabel("count", fontsize=15)
	plt.hist(new_charge, bins=N_HIST_BINS)
	plt.plot(bin_centers, ped_fit, label="Pedestal", lw=2)
	plt.plot(bin_centers, spe_fit, label="Single PE", lw=2)
	plt.legend(loc=1)
	plt.show()

	return

if __name__ == '__main__':
	if (len(sys.argv) != 2):
		print("ERROR: Invalid file input!\nSyntax: python gainCalc.py <filename.txt>\n")
	else:
		main(sys.argv[-1])
