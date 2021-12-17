'''
  Purpose: Determine PMT gain based on AmBe data

  Written by : J. He
'''

#imports
import glob, os, sys, uproot, json
import numpy as np
import matplotlib.pyplot as plt
import pandas as pd
import scipy.optimize as opt

import lib.ROOTProcessor as rp
#import lib.PMTGainFit as gf
import lib.GainFinder_noROOT as gf
import lib.Functions as fn

#defines
DATADIR = 'data/'
NBINS = 500

pmtIDs = list(range(332,464))
src_runs = [22,23,27,29,30,32,33,34,38,39,40,41,42,48,49,50,51,53,54,
               55,57,58,59,60,62,63]
bkg_runs = [64,65,66,67,68,69,70,71,72,73,74,75,76,77]
mybranches = ['eventTimeTank', 'hitQ', 'hitPE', 'hitDetID']

def fitGain(pmtQ):
  def norm(x, mean, sd, n): #n = normalization constant of gaussian
    return((n/(np.sqrt(2*np.pi)*sd))*np.exp(-(x - mean)**2/(2*sd**2)))

  #Plot charge distribution
  fig = plt.figure()
  ax = fig.subplot(111)

  bin_freq, bin_edges, patches = ax.hist(pmtQ, bins=NBINS, facecolor='orange')
  plt.yscale('log')

#  bin_edges = 1E12*bin_edges
  bin_centers = np.array(bin_edges[:-1]+(bin_edges[1]-bin_edges[0])/2.0) #midpoint of bin

  #Bin uncertainties found using square root of N approx
  uncert_data = []
  for i in range(bin_freq.size):
    uncert_data.append(np.sqrt(bin_freq[i]))
    if uncert_data[i] == 0:
      uncert_data[i] =  1

  ###############################
  #Fitting the 0 p.e. pedestal

  #Initial guess to the parameters of pedestal gaussian
  ped_params = [0, 1, 1000]

  #Take only first half of data where our pedestal is located
  popt_sub, pcov_sub = curve_fit(norm, bin_centers[:len(bin_centers)/2],
                bin_freq[:len(bin_centers)/2],
                p0 = ped_params,
                sigma = uncert_data[:len(bin_centers)/2])

  #take mean of 1st peak (pedestal) and subtract
  print(popt_sub[0])
  newPmtQ = pmtQ - popt_sub[0]


#main
if __name__=='__main__':
  flist = glob.glob(DATADIR + "NTuple_*.root")

  bkgProcessor = rp.ROOTProcessor("phaseIITankClusterTree")
  print("  ..for bkg data")
  srcProcessor = rp.ROOTProcessor("phaseIITankClusterTree")
  print("  ..for src data")
  hasBkg = False
  hasSrc = False
  for f in flist:
    #print(" > current file: " + f)
    nrun = f[-7:-5]   #extract run number
    #print(" > nrun = " + nrun)
    if (int(nrun) in bkg_runs):
      bkgProcessor.addROOTFile(f, branches_to_get=mybranches)
      hasBkg = True
    elif (int(nrun) in src_runs):
      srcProcessor.addROOTFile(f, branches_to_get=mybranches)
      hasSrc = True
    else:
      print("Skipping NTuple_%s.root"%(nrun))

  if (hasBkg):
    bdata = bkgProcessor.getProcessedData()
    bdf = pd.DataFrame(bdata)
    print("bdf len: " + str(len(bdf)))
    exp_bdf = bdf.set_index(['eventTimeTank']).apply(pd.Series.explode).reset_index()

  if (hasSrc):
    sdata = srcProcessor.getProcessedData()
    sdf = pd.DataFrame(sdata)
    print("sdf len: " + str(len(sdf)))
    exp_sdf = sdf.set_index(['eventTimeTank']).apply(pd.Series.explode).reset_index()

  for pmt in range(332,338):
    if (hasBkg):
      charge = np.array((exp_bdf[exp_bdf['hitDetID'] == pmt])['hitQ'])
      if (charge.size <= 0): #if no charges found for this pmt
        print("\n  > NO CHARGES FOUND FOR PMT #%d\n"%pmt)
        continue
#      print(charge)
      print(" > Attempting to fit charge distribution ...")
      gf.gainFit(charge)

      plt.hist((exp_bdf[exp_bdf['hitDetID'] == pmt])['hitQ'], bins=NBINS, 
                edgecolor='black', linewidth=0.5)
      plt.title("PMT #" + str(pmt))
      plt.xlabel("charge [nC]")
      plt.ylabel("# [a.u.]")
      plt.yscale('log')
      plt.show()
