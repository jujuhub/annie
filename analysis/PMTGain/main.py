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
import lib.Plots as pl

#defines
DBFILE = 'DB/myGains_AmBe_bkg.json'
#DBFILE = 'DB/SimpleGainCurves_Default.json'
#DBFILE = 'DB/TransparencyGains.json'
DATADIR = 'data/'
NBINS = 500
MAXMU = 0.056

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
    print(" [debug] bdf len: " + str(len(bdf)))
    exp_bdf = bdf.set_index(['eventTimeTank']).apply(pd.Series.explode).reset_index()

  if (hasSrc):
    sdata = srcProcessor.getProcessedData()
    sdf = pd.DataFrame(sdata)
    print(" [debug] sdf len: " + str(len(sdf)))
    exp_sdf = sdf.set_index(['eventTimeTank']).apply(pd.Series.explode).reset_index()

  #Load dictionary of initial fit parameters
  with open("./DB/InitialParams.json", "r") as ip:
    init_params = json.load(ip)

  fitType = "EXP2SPE"   #hardcoded

  #Load database?
  with open(DBFILE) as dbfile:
    db = json.load(dbfile)
    fitdata = db[fitType]
    dbfile.close()

  #Initialize gain fitting class
  GainFinder = gf.GainFinder()  #create an instance of GF class
  if (fitType == "EXP2SPE"):    #set up the fit
    GainFinder.setFitFunction(fn.EXP2SPE)
    GainFinder.setInitialFitParams(init_params["EXP2SPEInitParams"])
    GainFinder.setBounds(init_params["EXP2SPELB"],init_params["EXP2SPEUB"])

  #Loop through channels in file and fit gains to each
  for pmt in range(332,338):
    print(" > Attemping to fit charge distribution for PMT #%d"%pmt)
    if (hasBkg):
      charge = np.array((exp_bdf[exp_bdf['hitDetID'] == pmt])['hitQ'])
      if (charge.size <= 0): #if no charges found for this pmt
        print("\n  > NO CHARGES FOUND FOR PMT #%d\n"%pmt)
        continue
      print(charge)
#      gf.gainFit(charge)

      #Fit photoelectron peaks
      FIT_TAIL = False
      FitComplete = False
      PedFitComplete = False
      GoodPedFit = False
      exp_fit_range = []

      while not PedFitComplete:
        #Fit pedestal and exponential tail from failed dynode hits
        print(" > PEDESTAL PARAMETERS: " + str(init_params["PedParams"]))
        ped_opt, ped_cov, ped_xdata, ped_ydata, ped_yunc = GainFinder.FitPedestal(charge, init_params["PedParams"], init_params["PedFitRange"], fit_tail=FIT_TAIL, exp_fit_range=exp_fit_range)

        if ped_opt is None:
          print(" > PEDESTAL FIT FAILED... BAD PMT?  SKIPPING") 
          PedFitComplete = True
          GoodPedFit = False
          FitComplete = True
          GoodFit = False
          continue

        pl.PlotPedestal(ped_xdata, ped_ydata, fn.gauss1, ped_xdata, ped_opt, "GaussPlusExpo")
#        plt.plot(ped_xdata, ped_ydata)
#        pedfit = fn.gauss1(ped_xdata, *ped_opt)
#        plt.plot(ped_xdata, pedfit)
#        plt.show()

        above_ped = 0
        past_ped = np.where(ped_xdata > (ped_opt[1] + 3.*ped_opt[2]))[0]

        if FIT_TAIL:
          plt.plot(ped_xdata[past_ped], ped_ydata[past_ped])
          plt.plot(ped_xdata[past_ped], fn.expo(ped_xdata[past_ped], ped_opt[3], ped_opt[4], ped_opt[5]))
          above_ped = np.sum(ped_ydata[past_ped] - fn.expo(ped_xdata[past_ped], ped_opt[3], ped_opt[4], ped_opt[5]))
        else:
          above_ped = np.sum(ped_ydata[past_ped] - fn.gauss1(ped_xdata[past_ped], ped_opt[0], ped_opt[1], ped_opt[2]))
        plt.show()
        print("4SIGMA PAST PED, EXP. SUBTRACTED: " + str(above_ped))
        if (above_ped < 300):
          print("Low statistics beyond pedestal! May just be fitting on fluctuations.")
          skip_fit = str(input("Skip this fit?"))
          if (skip_fit in ["y", "Y", "yes", "Yes", "YES", "yEs"]):
            PedFitComplete = True
            GoodPedFit = False
            FitComplete = True
            GoodFit = False
            continue
        ped_good = str(input("Happy with pedestal fit? [y/N]: "))
        if (ped_good in ["y", "Y", "yes", "Yes", "YES", "yEs"]):
          PedFitComplete = True
          GoodPedFit = True
        else:
          if FIT_TAIL:
            fit_min = str(input("Exponential window min: "))
            fit_max = str(input("Exponential window max: "))
            exp_fit_range = [float(fit_min), float(fit_max)]

      UseDefault = "y"

      print(" [debug] ped_opt: " + str(ped_opt))
      while not FitComplete:
        print(" > SIGMA LIMIT IS: " + str(ped_opt[2]))
        GainFinder.setTauMax(4.*ped_opt[2])
        init_mean = str(input("Guess at SPE mean: "))
        if (float(init_mean) >= MAXMU):
          print("TRY LESS THAN " + str(MAXMU))
          continue
        try:
          GainFinder.setInitMean(float(init_mean))
        except ValueError:
          print("Input not recognized.  Trying a save bet of 0.001")
          GainFinder.setInitMean(0.001)
        if (UseDefault in ["y", "Y", "yes", "Yes", "YES", "yEs"]):
          popt, pcov, xdata, ydata, y_unc = GainFinder.FitPEPeaks(charge, exclude_ped=True, subtract_ped=True)
        elif (UseDefault in ["n", "N", "no", "No", "NO", "nO"]):
          InitialParams = pin.GetInitialParameters(fitType)
          popt, pcov, xdata, ydata, y_unc = GainFinder.FitPEPeaks(charge)

        if popt is None:
          print("FIT FAILED.  WE'RE MOVING ON TO THE NEXT CHANNEL")
          FitComplete = True
          GoodFit = False
          continue
        print("BEST FIT PARAMETERS: " + str(popt))
        pl.PlotHistPEDAndPEs_V2(xdata, ydata, ped_opt, popt, fitType)
        if popt is None:
          retry_fit = str(input("Fit failed! Retry? [y/N]: "))
          if (retry_fit not in ["y", "Y", "yes", "Yes", "YES", "yEs"]):
            FitComplete = True
            continue
          else:
            UseDefault = str(input("Use default fit parameters? [y/N/"))
        approve_fit = str(input("Fit converged! Happy with this fit? [y/N]: "))
        if (approve_fit in ["y", "Y", "yes", "Yes", "YES", "yEs"]):
          FitComplete = True
          GoodFit = True
        else:
          retry = str(input("Try again? [y/N]: "))
          if (retry not in ["y", "Y", "yes", "Yes", "YES", "yEs"]):
            FitComplete = True
            GoodFit = False

      if GoodFit:
        #With the pedestal and 1PE peak fit, estimate the PV ratio
        Valley_inds = np.where((xdata > ped_opt[1]) & (xdata < popt[1]))
        Valley_min = np.argmin(ydata[Valley_inds])
        print(" > VALLEY MIN AT BIN: " + str(xdata[Valley_min]))
        Valley_estimate_bins = ydata[np.arange(Valley_min-1, Valley_min+4, 1)]
        Valley_estimate = np.average(Valley_estimate_bins)
        print(" > VALLEY MEAN ESTIMATE: " + str(Valley_estimate))
        V_unc = np.std(Valley_estimate_bins)
        Peak_max = np.abs(xdata-popt[1]).argmin()
        print(" > PEAK MAX AT BIN: " + str(xdata[Peak_max]))
        Peak_estimate_bins = ydata[np.arange(Peak_max-2, Peak_max+3, 1)]
        Peak_estimate = np.average(Peak_estimate_bins)
        print(" > PEAK MEAN ESTIMATE: " + str(Peak_estimate))
        P_unc = np.std(Peak_estimate_bins)
        print(" > P/V RATIO ESTIMATE: " + str(Peak_estimate/Valley_estimate))
        PV_unc = (Peak_estimate/Valley_estimate)*np.sqrt((1./V_unc)**2 + (1./P_unc)**2)
        print(" > P/V RATIO UNC: " + str(PV_unc))

        #Since we've made it out, save to the DB
        db[fitType]["Channel"].append(pmt)
        db[fitType]["RunNumber"].append(nrun)
#        db[fitType]["LEDsOn"].append(ap.LED)
#        db[fitType]["LEDPINs"].append(ap.PIN)
#        db[fitType]["Date"].append(ap.DATE)
#        db[fitType]["V"].append(int(ap.VOLTS))
        db[fitType]["PV"].append(Peak_estimate/Valley_estimate)
        db[fitType]["PV_unc"].append(PV_unc)
        errs = np.sqrt(np.diag(pcov))
        if fitType in ["Gauss2","Gauss3"]:
          db[fitType]["c1Height"].append(popt[0])
          db[fitType]["c1Mu"].append(popt[1])
          db[fitType]["c1Sigma"].append(popt[2])
          db[fitType]["c2HScale"].append(popt[3])
          db[fitType]["c2MScale"].append(popt[4])
          db[fitType]["c2SScale"].append(popt[5])
          db[fitType]["c1Height_unc"].append(errs[0])
          db[fitType]["c1Mu_unc"].append(errs[1])
          db[fitType]["c1Sigma_unc"].append(errs[2])
          db[fitType]["c2HScale_unc"].append(errs[3])
          db[fitType]["c2MScale_unc"].append(errs[4])
          db[fitType]["c2SScale_unc"].append(errs[5])
        if fitType in ["SPE2Peaks","EXP2SPE","EXP3SPE"]:
          db[fitType]["c1Height"].append(popt[0])
          db[fitType]["c1Mu"].append(popt[1])
          db[fitType]["c1Sigma"].append(popt[2])
          db[fitType]["c2HScale"].append(popt[3])
          db[fitType]["c2MScale"].append(popt[4])
          db[fitType]["c2SScale"].append(popt[5])
          db[fitType]["SCScale"].append(popt[6])
          db[fitType]["c1Height_unc"].append(errs[0])
          db[fitType]["c1Mu_unc"].append(errs[1])
          db[fitType]["c1Sigma_unc"].append(errs[2])
          db[fitType]["c2HScale_unc"].append(errs[3])
          db[fitType]["c2MScale_unc"].append(errs[4])
          db[fitType]["c2SScale_unc"].append(errs[5])
          db[fitType]["SCScale_unc"].append(errs[6])
        if fitType in ["EXP2SPE","EXP3SPE"]:
          db[fitType]["CExp"].append(popt[7])
          db[fitType]["f_mu"].append(popt[8])
          db[fitType]["tau"].append(popt[9])
          db[fitType]["CExp_unc"].append(errs[7])
          db[fitType]["f_mu_unc"].append(errs[8])
          db[fitType]["tau_unc"].append(errs[9])
  with open(DBFILE, "w") as dbfile:
    json.dump(db, dbfile, sort_keys=False, indent=4)



      #plotting
#      plt.hist((exp_bdf[exp_bdf['hitDetID'] == pmt])['hitQ'], bins=NBINS, 
#                edgecolor='black', linewidth=0.5)
#      plt.title("PMT #" + str(pmt))
#      plt.xlabel("charge [nC]")
#      plt.ylabel("# [a.u.]")
#      plt.yscale('log')
#      plt.show()
