#!/opt/local/bin/python2.7
# Gain calculation from histogram acquired from plotCSV.py
# by Sam Crnkovich
# sdcrnkovich@ucdavis.edu

# modified by Julie He

import numpy as np
from scipy.optimize import curve_fit
import matplotlib.pyplot as plt

# need name of file at command line
import sys
CHARGEDATAFILE=sys.argv[-1]

DATAPATH='.'

N_HIST_BINS=100
E_CHARGE = 1.60217662E-19 # Coulombs
NEG_CHARGE = -0.50E-11 # neg charge threshold for ignoring the weird frames

def plot():
    ######################################
    
    def norm(x, mean, sd, n):
        # n: normalization constant of gaussian
        norm = (n/(np.sqrt(2*np.pi)*sd))*np.exp(-(x - mean)**2/(2*sd**2))
        return norm

    # Setting up test data    
    print("attempting to open " + (DATAPATH + '/{0}').format(CHARGEDATAFILE))
    with open((DATAPATH + '/{0}').format(CHARGEDATAFILE)) as f1:
        charge = np.loadtxt(f1, dtype = float) # removed the .txt after {0}

    # plot the charge distribution
    fig0 = plt.figure()
    ax0 = fig0.add_subplot(111)

    bin_freq, bin_edges, patches0 = ax0.hist(charge, bins=N_HIST_BINS, facecolor='orange')
    plt.yscale('log')

    bin_edges = 1E12*bin_edges
    bin_centers0 = np.array(bin_edges[:-1]+(bin_edges[1]-bin_edges[0])/2.0) # midpoint of bin

    # Bin uncertainties found using square root of N approx
    uncert_data = []
    for i in range(bin_freq.size):
        uncert_data.append(np.sqrt(bin_freq[i]))
        if uncert_data[i] == 0:
            uncert_data[i] =  1


    ######################################
    # Fitting the 0 p.e. pedestal
    # Take only first half of data where our pedestal is located

    # Initial guess to the parameters of pedestal gaussian
    ped_params = [0, 1, 1000]

    popt_sub, pcov_sub = curve_fit(norm, bin_centers0[:len(bin_centers0)/2],
                bin_freq[:len(bin_centers0)/2],
                p0 = ped_params,
                sigma = uncert_data[:len(bin_centers0)/2])

    # take mean of 1st peak (pedestal) and subtract
    print(popt_sub[0])
    charge = charge - popt_sub[0]*1E-12

    i=0
    new_charge = []

    while (i < len(charge)):
        # if charge value lies very far to the left, skip
        if (charge[i] < NEG_CHARGE): 
            print("skipped " + str(charge[i]))
        else:
            new_charge.append(charge[i])
        i+=1

    new_charge = np.array(new_charge)

    fig = plt.figure()
    ax1 = fig.add_subplot(111)
    
    y_data, bins, patches = ax1.hist(new_charge, bins=N_HIST_BINS, facecolor='orange')

    bins = 1E12*bins
    bin_centers = np.array(bins[:-1]+(bins[1]-bins[0])/2.0)

    popt_ped, pcov_ped = curve_fit(norm, bin_centers[:len(bin_centers)/2],
                y_data[:len(bin_centers)/2],
                p0 = ped_params,
                sigma = uncert_data[:len(bin_centers)/2])

    yfit_ped = norm(bin_centers, *popt_ped)

    # Now fit the 1 p.e. using a double gaussian fit
    gauss_approx = [1, 2, 100]

    def double_gauss(x, mu, sigma, n):
        # adds another gaussian to fitted pedestal
        gauss = (norm(x, popt_ped[0], popt_ped[1], popt_ped[2]) +
                 (n/(np.sqrt(2*np.pi)*sigma))*np.exp(-(x - mu)**2/(2*sigma**2)))
        return gauss
    
    popt, pcov = curve_fit(double_gauss, bin_centers, y_data,
            p0=gauss_approx, sigma=uncert_data)

    two_gauss_fit = double_gauss(bin_centers, *popt) # shouldn't it be evaulated for 2nd half of data? ...

    # fit double gaussian to pedestal and 1 p.e. at once
    def db_gauss(x, mu1, sigma1, n1, mu2, sigma2, n2):
        return (n1/(np.sqrt(2*np.pi)*sigma1))*np.exp(-(x-mu1)**2/(2*sigma1**2)) + (n2/(np.sqrt(2*np.pi)*sigma2))*np.exp(-(x-mu2)**2/(2*sigma2**2))

    dbgauss_guess = [0, 1, 1000, 1, 2, 100]

    popt_dbg, pcov_dbg = curve_fit(db_gauss, bin_centers, y_data, p0=dbgauss_guess, sigma=uncert_data)

    dbgauss_fit = db_gauss(bin_centers, *popt_dbg)


    # print stats // individial vs simultaneous
    print("--- individual fits / simultaneous fit ---")
    print("mean: " + str(popt[0]) + " / " + str(popt_dbg[3]))
    print("standard deviation: " + str(popt[1]) + " / " + str(popt_dbg[4]))
    print("normalization constant: " + str(popt[2]) + " / " + str(popt_dbg[5]))

    # y_fit = norm(bin_centers, *popt) # The *popt passes the arguments to func

    bin_centers = bin_centers*1E-12

     # Calculate chi-squared
    chi_squared = 0 # individual fit
    chi2 = 0 # simultaneous fit
    for i in range(y_data.size):
        chi_squared += (y_data[i] - two_gauss_fit[i])**2/(uncert_data[i]**2)
        chi2 += (y_data[i] - dbgauss_fit[i])**2/(uncert_data[i]**2)
    reduced_chi_square = chi_squared/(len(bin_centers) - 6) # why subtract 6? 6 parameters
    red_chi2 = chi2/(len(bin_centers) - 6)
    print("chi-squared: " + str(chi_squared) + " / " + str(chi2))
    print("reduced_chi_square: " + str(reduced_chi_square) + " / " + str(red_chi2))

    # gain calc using individual gaussian fits
    gain = popt[0]*1E-12/E_CHARGE
    uncert_gain = popt[1]*1E-12/E_CHARGE/np.sqrt(popt[2])
    # gain calc using simultaneous double gaussian fit
    gain2 = popt_dbg[3]*1E-12/E_CHARGE
    uncert_gain2 = popt_dbg[4]*1E-12/E_CHARGE/np.sqrt(popt_dbg[5])
    print("gain: " + str(gain) + " +/- " + str(uncert_gain) + " / " + str(gain2) + " +/- " + str(uncert_gain2))


    # Plot the fits
    plt.plot(bin_centers, y_data, marker='*', lw=0, label='Output Charge Histogram')
    plt.plot(bin_centers, yfit_ped, label = '0 P.E. Gaussian Fit')
    plt.plot(bin_centers, two_gauss_fit, label='1 P.E. Gaussian Fit') # why doesn't he use the two_gauss_fit? doesn't make too much of a diff
    plt.plot(bin_centers, dbgauss_fit, label='Double Gaussian Fit')

    plt.xlabel('PMT Output Charge(C)')
    plt.ylabel('Counts')
    plt.yscale('log')
    plt.ylim(1, 100000)
    plt.legend(loc=1)
    plt.errorbar(bin_centers, y_data, yerr=uncert_data, ls = 'None', marker='o', ms=4)
    plt.show()
    return [popt[0]*1E-12, popt[1]*1E-12, popt[2], popt_dbg[3]*1E-12, popt_dbg[4]*1E-12, popt_dbg[5]]

def main():
    print("running")
    data_array = plot()
    print("done")
    return

if __name__ == '__main__':
    main()
