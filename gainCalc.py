#!/opt/local/bin/python2.7
# Gain calculation from histogram acquired from plotCSV.py
# by Sam Crnkovich
# sdcrnkovich@ucdavis.edu

import numpy as np
from scipy.optimize import curve_fit
import matplotlib.pyplot as plt

CHARGEDATAFILE='my_charges'
DATAPATH='.'
N_HIST_BINS=100

def plot():
    ######################################
    # Setting up test data
    def norm(x, mean, sd, n):
        norm = [(n/(np.sqrt(2*np.pi)*sd))*np.exp(-(x[i] - mean)**2/(2*sd**2))
            for i in range(x.size)]
        return norm
    print 'attempting to open ' + (DATAPATH + '/{0}.txt').format(CHARGEDATAFILE)
    with open((DATAPATH + '/{0}.txt').format(CHARGEDATAFILE)) as f1:
        charge = np.loadtxt(f1, dtype = float)


    # plot the charge distribution
    fig = plt.figure()
    ax1 = fig.add_subplot(111)

    y_data, bins, patches = ax1.hist(charge, bins=N_HIST_BINS,
                                     facecolor='orange')
    plt.yscale('log', nonposy='clip')
    plt.xlabel('Coulombs')
    plt.ylabel('Counts')
    #plt.show()

    bins = np.array(bins)
    bins = 1E12*bins
    bin_centers = np.array(bins[:-1]+(bins[1]-bins[0])/2.0)
    
    x_points = np.linspace(-1E-12, 7E-12, 1000)

    # Bin uncertainties found using square root of N approximation
    uncert_data = []
    for i in range(y_data.size):
        uncert_data.append(np.sqrt(y_data[i]))
        if uncert_data[i] == 0:
            uncert_data[i] =  1

    ######################################
    # Fitting the 0 p.e. pedestal
    # Take only first half of data (where our pedestal is located) ; this may be a problem

    # Initial guess to the parameters of the pedestal gaussian
    gauss_guess = [0, 1, 1000]

    popt_ped, pcov_ped = curve_fit(norm, bin_centers[:len(bin_centers)/2],
                                   y_data[:len(bin_centers)/2],
                                   p0 = gauss_guess,
                                   sigma = uncert_data[:len(bin_centers)/2])

    yfit_ped = norm(bin_centers, *popt_ped)

    # Now fit the 1 p.e. using a double gaussian fit
    gauss_approx = [1, 2, 100]

    def double_gauss(x, mu, sigma, n):
        gauss = (norm(x, popt_ped[0], popt_ped[1], popt_ped[2]) +
                 (n/(np.sqrt(2*np.pi)*sigma))*np.exp(-(x - mu)**2/(2*sigma**2)))
        return gauss
    
    popt, pcov = curve_fit(double_gauss, bin_centers, y_data,
                           p0=gauss_approx, sigma=uncert_data)

    
    popt[1] = np.abs(popt[1])
    print 'mean:', popt[0]
    print 'standard deviation:', popt[1] 
    print 'normalization constant:', popt[2]

    y_fit = norm(bin_centers, *popt) # The *popt passes the arguments to func

    two_gauss_fit = double_gauss(bin_centers, *popt)

    bin_centers = bin_centers*1E-12


     # Calculate the chi-squared
    chi_squared = 0
    for i in range(y_data.size):
        chi_squared += (y_data[i] - two_gauss_fit[i])**2/(uncert_data[i]**2)
    reduced_chi_square = chi_squared/(len(bin_centers) - 6)
    print 'chi-squared:', chi_squared
    print 'reduced_chi_square:', reduced_chi_square

    # Plot the fits
    plt.plot(bin_centers, y_data, marker='*', lw=0, label='Output Charge Histogram')
    plt.plot(bin_centers, y_fit, label='1 P.E. Gaussian Fit')
    plt.plot(bin_centers, yfit_ped, label = '0 P.E. Gaussian Fit')
    plt.xlabel('PMT Output Charge(C)')
    plt.ylabel('Counts')
    plt.yscale('log')
    plt.ylim(1, 10000)
    plt.legend(loc=1)
    plt.errorbar(bin_centers, y_data, yerr=uncert_data, ls = 'None',
                 marker='o', ms=4)
    plt.show()
    return [popt[0]*1E-12 , popt[1]*1E-12, popt[2]]

def main():
    print'running'
    data_array = plot()
    print 1
    q_out = data_array[0]
    q_in = 1.60217657E-19 # charge in Coulumbs
    gain = q_out/q_in
    uncert_gain = data_array[1]/q_in/np.sqrt(data_array[2])
    print 'gain:', gain ,'+/-', uncert_gain
    return

if __name__ == '__main__':
    main()
