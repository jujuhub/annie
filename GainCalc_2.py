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

#CHARGEDATAFILE='charge_data_001'
DATAPATH='.'
N_HIST_BINS=100

E_CHARGE = 1.60217657E-19 # Coulombs
NEG_CHARGE = -0.50e-11 # neg charge threshold for ignoring the weird frames

def plot():
    ######################################
    """
        Plots charge distribution, 
        fits Gaussian to the pedestal,
        fits double Gaussian to charge data,
        calculates chi^2 and gain
    """

    # Setting up test data
    def norm(x, mean, sd, n):
        """
            Used to fit gaussian to pedestal
            x: array of data ... hmm not sure why it needs to be array
            mean: mean of data
            sd: std dev of data
            n: normalization constant of gaussian
        """
        norm = [(n/(np.sqrt(2*np.pi)*sd))*np.exp(-(x[i] - mean)**2/(2*sd**2))
            for i in range(x.size)]
        return norm
    
    print("attempting to open " + (DATAPATH + '/{0}').format(CHARGEDATAFILE))
    with open((DATAPATH + '/{0}').format(CHARGEDATAFILE)) as f1:
        charge = np.loadtxt(f1, dtype = float) # removed the .txt after {0}

    # removes the very negative charges from the weird frames
    i=0
    new_charge = []

    while (i < len(charge)):
        if (charge[i] < NEG_CHARGE):
            print("skipped " + str(charge[i]))
        else:
            new_charge.append(charge[i])
        i+=1

    new_charge = np.array(new_charge)

    # plot the charge distribution
    fig = plt.figure()
    ax1 = fig.add_subplot(111)

    y_data, bins, patches = ax1.hist(new_charge, bins=N_HIST_BINS, 
            facecolor='orange')
    # not sure why he does this bc this gets overwritten
    plt.yscale('log', nonposy='clip')
    plt.xlabel('Coulombs')
    plt.ylabel('Counts')
    #plt.show()

    #print(type(bins))
    #bins = np.array(bins) # redundant; hist returns array already
    bins = 1E12*bins # why multiply by 1E12 only to undo it later? bc gaussian is for high means
    bin_centers = np.array(bins[:-1]+(bins[1]-bins[0])/2.0)
    
    #x_points = np.linspace(-1E-12, 7E-12, 1000) # tf?

    # Bin uncertainties found using square root of N approximation
    uncert_data = []
    for i in range(y_data.size):
        uncert_data.append(np.sqrt(y_data[i]))
        if uncert_data[i] == 0:
            uncert_data[i] =  1

    ######################################
    # Fitting the 0 p.e. pedestal
    # Take only first half of data (where our pedestal is located) 
    # THIS MAY BE A PROBLEM; how do you know it's first half of data?

    # Initial guess to the parameters of the pedestal gaussian
    gauss_guess = [0, 1, 1000]

    popt_ped, pcov_ped = curve_fit(norm, bin_centers[:len(bin_centers)/2],
                y_data[:len(bin_centers)/2],
                p0 = gauss_guess,
                sigma = uncert_data[:len(bin_centers)/2])

    #print("opt ped parameters: " + str(popt_ped))

    yfit_ped = norm(bin_centers, *popt_ped) # should this be calculated for 1st half of data only?

    # Now fit the 1 p.e. using a double gaussian fit
    gauss_approx = [1, 2, 100]

    def double_gauss(x, mu, sigma, n):
        # adds fitted pedestal and another gaussian
        gauss = (norm(x, popt_ped[0], popt_ped[1], popt_ped[2]) +
                 (n/(np.sqrt(2*np.pi)*sigma))*np.exp(-(x - mu)**2/(2*sigma**2)))
        return gauss
    
    popt, pcov = curve_fit(double_gauss, bin_centers, y_data,
            p0=gauss_approx, sigma=uncert_data)

    # fit double gaussian all at once
    def db_gauss(x, mu1, sigma1, n1, mu2, sigma2, n2):
        """
            x: data
            mu1, mu2: mean of pedestal, 1st peak
            sigma1, sigma2: sd of pedestal, 1st peak
            n1, n2: normalization constants

        """
        dbgauss = (n1/(np.sqrt(2*np.pi)*sigma1))*np.exp(-(x-mu1)**2/(2*sigma1**2)) + (n2/(np.sqrt(2*np.pi)*sigma2))*np.exp(-(x-mu2)**2/(2*sigma2**2))
        return dbgauss

    dbgauss_guess = [0, 1, 1000, 1, 2, 100]
    popt_dbg, pcov_dbg = curve_fit(db_gauss, bin_centers, y_data, p0=dbgauss_guess, sigma=uncert_data)

    dbgauss_fit = db_gauss(bin_centers, *popt_dbg)

    # def triple_gauss(x, mu1, sigma1, n1, mu2, sigma2, n2, mu3, sigma3, n3):
    #     trp_gauss = (n1/(np.sqrt(2*np.pi)*sigma1))*np.exp(-(x-mu1)**2/(2*sigma1**2)) + (n2/(np.sqrt(2*np.pi)*sigma2))*np.exp(-(x-mu2)**2/(2*sigma2**2)) + (n3/(np.sqrt(2*np.pi)*sigma3))*np.exp(-(x-mu3)**2/(2*sigma3**2))
    #     return trp_gauss

    # trp_gauss_guess = [0, 1, 1000, 0.5, 2, 10, 1, 2, 100]
    # popt_trg, pcov_trg = curve_fit(triple_gauss, bin_centers, y_data, p0=trp_gauss_guess, sigma=uncert_data)

    # trpgauss_fit = triple_gauss(bin_centers, *popt_trg)

    #popt[1] = np.abs(popt[1])
    print("--- individual fits / simultaneous fit ---")
    print("mean: " + str(popt[0]) + " / " + str(popt_dbg[3]))
    print("standard deviation: " + str(np.abs(popt[1])) + " / " + str(popt_dbg[4]))
    print("normalization constant: " + str(popt[2]) + " / " + str(popt_dbg[5]))

    # using single gaussian with double peak parameters...?
    y_fit = norm(bin_centers, *popt) # The *popt passes the arguments to func

    two_gauss_fit = double_gauss(bin_centers, *popt)

    bin_centers = bin_centers*1E-12


     # Calculate the chi-squared
    chi_squared = 0
    chi2 = 0
    for i in range(y_data.size):
        chi_squared += (y_data[i] - two_gauss_fit[i])**2/(uncert_data[i]**2)
        chi2 += (y_data[i] - dbgauss_fit[i])**2/(uncert_data[i]**2)
    reduced_chi_square = chi_squared/(len(bin_centers) - 6) # why subtract 6?
    reduced_chi2 = chi2/(len(bin_centers) - 6)
    print("chi-squared: " + str(chi_squared) + " / " + str(chi2))
    print("reduced_chi_square: " + str(reduced_chi_square) + " / " + str(reduced_chi2))

    # gain calc using individual gaussian fits
    gain = popt[0]*1E-12/E_CHARGE
    uncert_gain = popt[1]*1E-12/E_CHARGE/np.sqrt(popt[2])

    # gain calc using simultaneous double gaussian fit
    gain2 = popt_dbg[3]*1E-12/E_CHARGE
    uncert_gain2 = popt_dbg[4]*1E-12/E_CHARGE/np.sqrt(popt_dbg[5])
    print("gain: " + str(gain) + " +/- " + str(uncert_gain) + " / " + str(gain2) + " +/- " + str(uncert_gain2))

    # Plot the fits
    plt.plot(bin_centers, y_data, marker='*', lw=0, label='Output Charge Histogram')
    plt.plot(bin_centers, y_fit, label='1 P.E. Gaussian Fit')
    plt.plot(bin_centers, yfit_ped, label = '0 P.E. Gaussian Fit')

    plt.plot(bin_centers, dbgauss_fit, label='Double Gaussian Fit')

    # plt.plot(bin_centers, trpgauss_fit, label='Triple Gaussian Fit')
    
    plt.xlabel('PMT Output Charge(C)')
    plt.ylabel('Counts')
    plt.yscale('log')
    plt.ylim(1, 10000)
    plt.legend(loc=1)
    plt.errorbar(bin_centers, y_data, yerr=uncert_data, ls = 'None',
                 marker='o', ms=4)
    plt.show()
    return [popt[0]*1E-12 , popt[1]*1E-12, popt[2], popt_dbg[3]*1E-12, popt_dbg[4]*1E-12, popt_dbg[5]]

def main():
    print("running")
    data_array = plot()
    print("done")
    # q_out = data_array[0]
    # q_out_2 = data_array[3]
    # gain = q_out/E_CHARGE
    # gain2 = q_out_2/E_CHARGE
    # uncert_gain = data_array[1]/E_CHARGE/np.sqrt(data_array[2])
    # uncert_gain2 = data_array[4]/E_CHARGE/np.sqrt(data_array[5])
    # print 'gain:', gain ,'+/-', uncert_gain, ',', gain2, "+/-", uncert_gain2
    return

if __name__ == '__main__':
    main()
