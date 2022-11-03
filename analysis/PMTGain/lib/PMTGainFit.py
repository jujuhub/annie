'''
  Gain calculation from histogram acquired from plotCSV.py
  
  Written by: Sam Crnkovich <sdcrnkovich@ucdavis.edu>
  Modified by: J. He

'''

#imports
import numpy as np
from scipy.optimize import curve_fit
import matplotlib.pyplot as plt
from . import Curves as curv  #this syntax works if running `python3 ...`

#defines
NBINS = 500
E_CHARGE = 1.60217662E-19  #Coulombs
NEG_CHARGE = -0.50E-11     #neg charge threshold for ignoring weird frames

def gainFit(charge):
  '''
    input:
    - charge: an array of charge values in units of nC
  '''

  #Plot charge distribution
  fig, ax = plt.subplots(1,1, sharex=True, sharey=True)

  bin_freq, bin_edges, patches0 = ax.hist(charge, bins=NBINS)
#  ax.yscale('log')

  #Get midpoints of bins
  bin_centers0 = np.array(bin_edges[:-1]+(bin_edges[1]-bin_edges[0])/2.0) 

  #Bin uncertainties found using square root of N approx
  uncert_data = []
  for i in range(bin_freq.size):
    uncert_data.append(np.sqrt(bin_freq[i]))
    if uncert_data[i] == 0:
      uncert_data[i] =  1


  ###########################################
  ### Fitting the pedestal
  ###########################################
  qmax_i = np.argmax(bin_freq)
  print(" [debug] qmax_i: %d"%qmax_i)
  valley_i = 0
  for i in range(qmax_i+1, NBINS//3):
    if (bin_freq[i] < bin_freq[i-1]):
      continue
    else:
      valley_i = i
      print(" [debug] valley_i: %d"%valley_i)
      break

  #Initial guess to the parameters of pedestal gaussian
  ped_params = [0, 0.02, 10000]

  #Take only first part of data where pedestal is located
  popt_sub, pcov_sub = curve_fit(curv.Norm, bin_centers0[:valley_i],
                        bin_freq[:valley_i], p0 = ped_params,
                        sigma = uncert_data[:valley_i])

  #Take mean of 1st peak (pedestal) and subtract #TODO:why subtract?
  print(" [debug] popt_sub[0]: %f"%popt_sub[0])
#  charge = charge - popt_sub[0]*1E-12
#  charge = charge - popt_sub[0]
  ped_fit = curv.Norm(bin_centers0[:valley_i].astype(float), *popt_sub)

  plt.plot(bin_centers0[:valley_i], ped_fit)
  plt.yscale('log')
  plt.show()

'''
  i = 0
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
   
  y_data, bins, patches = ax1.hist(new_charge, bins=NBINS)

#  bins = 1E12*bins
  bin_centers = np.array(bins[:-1]+(bins[1]-bins[0])/2.0)

  popt_ped, pcov_ped = curve_fit(curv.Norm, bin_centers[5:len(bin_centers)//2],
                y_data[5:len(bin_centers)//2],
                p0 = ped_params,
                sigma = uncert_data[5:len(bin_centers)//2])

    yfit_ped = curv.Norm(bin_centers, *popt_ped)

    # Now fit the 1 p.e. using a double gaussian fit
    gauss_approx = [*popt_ped, 0.2, 0.02, 100]

    popt, pcov = curve_fit(curv.double_gauss, bin_centers, y_data,
            p0=gauss_approx, sigma=uncert_data)

    two_gauss_fit = curv.double_gauss(bin_centers, *popt) # shouldn't it be evaulated for 2nd half of data? ...


    # fit double gaussian to pedestal and 1 p.e. at once
    dbgauss_guess = [0, 0.02, 10000, 0.2, 0.02, 500]

    popt_dbg, pcov_dbg = curve_fit(curv.db_gauss, bin_centers, y_data, p0=dbgauss_guess, sigma=uncert_data)

    dbgauss_fit = curv.db_gauss(bin_centers, *popt_dbg)


    # print stats // individial vs simultaneous
    print("--- individual fits / simultaneous fit ---")
    print("mean: " + str(popt[0]) + " / " + str(popt_dbg[3]))
    print("standard deviation: " + str(popt[1]) + " / " + str(popt_dbg[4]))
    print("normalization constant: " + str(popt[2]) + " / " + str(popt_dbg[5]))

    # y_fit = curv.Norm(bin_centers, *popt) # The *popt passes the arguments to func

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
'''
