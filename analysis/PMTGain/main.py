'''
  Purpose: Determine PMT gain based on AmBe data

  Written by : J. He
    with code adapted from Teal's version
'''

### imports ###
import glob, os, sys, uproot, json
import numpy as np
import matplotlib.pyplot as plt
import pandas as pd
import scipy.optimize as opt

import lib.ROOTProcessor as rp
import lib.GainFinder_noROOT as gf
import lib.Functions as fn
import lib.Plots as pl


#check if charge data stored in txt file
# AmBe data format (txt): eventTimeTank,hitT,hitQ,hitDetID
# LED data format (txt): hitDetID,charge(hist_x),freq(hist_y),unc
if (len(sys.argv) != 2):
  print(" > MISSING OR EXCESS ARGUMENT(S)!")
  print(" > SYNTAX: python3 main.py [0/1/2/5]")
  print("   0: no txt file\n   1: AmBe BKG\n   2: AmBe SRC\n   5: LED\n")
  sys.exit(1)

HASCSV = False
HASBKG = False
HASSRC = False
HASLED = False

try:
  NUMARG = int(sys.argv[-1])
except ValueError:
  print(" Not a valid argument...\n")
  sys.exit(1)
if (NUMARG == 1):
  HASCSV = True
  HASBKG = True
if (NUMARG == 2):
  HASCSV = True
  HASSRC = True
if (NUMARG == 5):
  HASLED = True


### defines ###
DATADIR = "data/src/"
DBFILE = "DB/LEDmaxpk_gains_Gauss1.json"  #calculated gains/etc stored here
CSVFILE = "src_charges_10hits_3pC.txt"    #input ambe data
LEDFILE = "LED_R3134_3158_maxpeak_hcharge.txt"    #input led data
SPFTFILE = ""   #customized fit range for pmts
NBINS = 210
SIPMTCUT = 85.    #[ns]
NHITS = 10    #also n of PMTs firing
TCUT = 15000.   #[ns]
QPERPMT = 0.003   #[nC]
MINQ = -0.001
MAXQ = 0.02
MAXMU = 0.008
VIS = 1.      #ped visible
NOTVIS = 0.   #ped not visible

### some lists ###
#pmtIDs = list(range(416,464))  #full range:[332,464], ETEL:[353,372]
#dthr = pd.read_csv("tuned_threshold.txt", header=None, names=['pmtID','adc'], sep=',')
#pmtIDs = list(dthr[dthr['adc'] != 7]['pmtID'].astype(int))
pmtIDs = list(range(332,372))   #ETEL:352-372

src_runs = [22,23,27,29,30,32,33,34,38,39,40,41,42,48,49,50,51,53,54,
               55,57,58,59,60,62,63]
bkg_runs = [64,65,66,67,68,69,70,71,72,73,74,75,76,77]
mybranches = ['eventTimeTank', 'hitQ', 'hitT', 'hitPE', 'hitDetID', 'clusterPE', 'clusterHits', 'clusterCharge', 'SiPMNum', 'SiPMhitT']
drop_cols = ['clusterCharge', 'clusterPE', 'clusterHits', 'hitPE', 'SiPMNum', 'SiPMhitT']


### main ###
if __name__=='__main__':
  #set up ROOT processor if (AmBe) data not from txt file
  if ((not HASCSV) and (not HASLED)):
    bkgProcessor = rp.ROOTProcessor("phaseIITankClusterTree")
    print("  ..for bkg data")
    srcProcessor = rp.ROOTProcessor("phaseIITankClusterTree")
    print("  ..for src data")

    nrun = -69
    flist = glob.glob(DATADIR + "NTuple_*.root")
    if (not flist):
      print(" No files found...")
      sys.exit(1)
    for f in flist:
      nrun = f[-7:-5]   #extract run number
      #print(" > nrun = " + nrun)
      if (int(nrun) in bkg_runs):
        bkgProcessor.addROOTFile(f, branches_to_get=mybranches)
        HASBKG = True
      elif (int(nrun) in src_runs):
        srcProcessor.addROOTFile(f, branches_to_get=mybranches)
        HASSRC = True
      else:
        print("Skipping NTuple_%s.root"%(nrun))

    if (HASBKG):
      bdata = bkgProcessor.getProcessedData()
      bdf = pd.DataFrame(bdata)
      #apply cut on nHits
      print(" [debug] len(bdf): " + str(len(bdf)))
      bdf = bdf[bdf['clusterHits'] < NHITS]
      print(" [debug] len(bdf): " + str(len(bdf)))
      bdf = bdf[(bdf['clusterCharge'] / bdf['clusterHits']) < QPERPMT]
      print(" [debug] len(bdf): " + str(len(bdf)))
      #bdf = bdf[bdf['hitDetID'].apply(lambda x: len(x) < NHITS)]
      bdf = bdf[['eventTimeTank','hitT','hitQ','hitDetID']]
      exp_df = bdf.set_index(['eventTimeTank']).apply(pd.Series.explode).reset_index()

    if (HASSRC):
      sdata = srcProcessor.getProcessedData()
      sdf = pd.DataFrame(sdata)
      #cut on SiPM hits
      #print(" [debug] len(sdf): " + str(len(sdf)))
      #sdf = sdf[sdf['SiPMNum'].apply(lambda x: (len(x) == 2) and (1.0 in x) and (2.0 in x))]  #req 1 hit in each SiPM and only 1 per SiPM
      #print(" [debug] len(sdf): " + str(len(sdf)))
      #sdf = sdf[sdf['SiPMhitT'].apply(lambda tp: abs(tp[0]-tp[1]) < SIPMTCUT)]
      #cut on nHits
      print(" [debug] len(sdf): " + str(len(sdf)))
      sdf = sdf[sdf['clusterHits'] < NHITS]
      print(" [debug] len(sdf): " + str(len(sdf)))
      sdf = sdf[(sdf['clusterCharge'] / sdf['clusterHits']) < QPERPMT]
      print(" [debug] len(sdf): " + str(len(sdf)))
      sdf = sdf.drop(columns=drop_cols)
      exp_df = sdf.set_index(['eventTimeTank']).apply(pd.Series.explode).reset_index()

    #save to txt file (for easy loading later)
    print(" > saving data to txt...")
    exp_df.to_csv(DATADIR+CSVFILE, index=False)
    print(" > data saved to: " + DATADIR + CSVFILE)

  #load data from txt file
  if (HASCSV):  #assumes data in file is all bkg or all src
    print(" > Loading data from: " + DATADIR + CSVFILE)
    exp_df = pd.read_csv(DATADIR+CSVFILE)

  if (HASLED):
    print(" > Loading data from: " + DATADIR + LEDFILE)
    exp_df = pd.read_csv(DATADIR+LEDFILE, header=None, names=['hitDetID', 'xdata', 'ydata', 'unc'], sep=',')
    #print(exp_df.head(10))

  #load special fit ranges
  spf = pd.DataFrame()
  if (SPFTFILE != ""):
    print(" > Loading special fit ranges from: " + SPFTFILE)
    spf = pd.read_csv(DATADIR+SPFTFILE, header=0, sep=',')

  #Load dictionary of initial fit parameters
  with open("./DB/InitialParams.json", "r") as ip:
    init_params = json.load(ip)

  fitType = "Gauss1"   #hardcoded
  print(" > USING FIT TYPE: >> " + fitType + " <<")

  #Load database?
  with open(DBFILE) as dbfile:
    db = json.load(dbfile)
    fitdata = db[fitType]   #not used anywhere..
    dbfile.close()

  #Initialize gain fitting class
  GainFinder = gf.GainFinder()  #create an instance of GF class
  if(fitType == "Gauss1"):
    GainFinder.setFitFunction(fn.gauss1)
    GainFinder.setInitialFitParams(init_params["GaussInitParams"])
    GainFinder.setBounds(init_params["GaussLB"],init_params["GaussUB"])
  if (fitType == "EXP2SPE"):    #set up the fit
    GainFinder.setFitFunction(fn.EXP2SPE)
    GainFinder.setInitialFitParams(init_params["EXP2SPEInitParams"])
    GainFinder.setBounds(init_params["EXP2SPELB"],init_params["EXP2SPEUB"])
  if (fitType == "SPE"):
    GainFinder.setFitFunction(fn.SPEGaussians_NoExp)
    GainFinder.setInitialFitParams(init_params["SPEInitParams"])
    GainFinder.setBounds(init_params["SPELB"],init_params["SPEUB"])

  #Loop through channels in file and fit gains to each
  #fig, ax = plt.subplots()    #best not to have this in loop (mem issues)
  for pmt in pmtIDs:
    print("Attempting to fit charge distribution for PMT #%d"%pmt)
    evts = []
    evts_unc = []
    bin_centers = []

    if (HASLED):
      evts = np.array(exp_df[(exp_df['hitDetID'] == pmt)]['ydata'])
      bin_centers = np.array(exp_df[(exp_df['hitDetID'] == pmt)]['xdata'])
      evts_unc = np.array(exp_df[(exp_df['hitDetID'] == pmt)]['unc'])
      if (not evts.any()):
        print("\n  > NO CHARGES FOUND FOR PMT #%d\n"%pmt)
        continue
    else:
      charge = np.array([])
      if (HASBKG):
        charge = np.array((exp_df[(exp_df['hitDetID'] == pmt) & (exp_df['hitT'] > TCUT) & (exp_df['hitQ'] >= MINQ) & (exp_df['hitQ'] <= MAXQ)])['hitQ'])
      if (HASSRC):
        charge = np.array((exp_df[(exp_df['hitDetID'] == pmt) & (exp_df['hitQ'] >= MINQ) & (exp_df['hitQ'] <= MAXQ)])['hitQ'])    #no time cut
      if (charge.size <= 0): #if no charges found for this pmt
        print("\n  > NO CHARGES FOUND FOR PMT #%d\n"%pmt)
        continue

    fig, ax = plt.subplots()    #need this when loop plotting
    ax.set_title("charge distribution for pmt #%d"%pmt)
    ax.set_xlabel("charge [nC]")
    ax.set_ylabel("n events")
    if (HASLED):
      ax.plot(bin_centers, evts)
      #ax.bar(bin_centers, evts, align='center', width=0.9*(bin_centers[1]-bin_centers[0]))
    if (not HASLED):
      evts, bin_edges, patches = ax.hist(charge, bins=NBINS, range=(MINQ,MAXQ), ec="white")
    plt.show()

    #Fit photoelectron peaks
    FIT_TAIL = False          #hardcoded
    FitComplete = False
    PedFitComplete = False
    GoodPedFit = False        #nothing done w this
    exp_fit_range = []

    ped_exist = str(input("Is the pedestal visible? [y/N]: "))
    #ped_exist = "N"   #hardcoded
    if (ped_exist in ["y", "Y", "yes", "Yes", "YES", "yEs"]):
      VisiblePed = VIS
    elif (ped_exist in ["n", "N", "no", "No", "NO", "nO"]):
      VisiblePed = NOTVIS
      PedFitComplete = True
      ped_opt = [0., -999., -999.]
    else:
      VisiblePed = NOTVIS
      print("Invalid input. Assuming pedestal is not present...")

    #get midpoint of bins & uncertainty
    if (not HASLED):
      bin_centers = np.array(bin_edges[:-1]+(bin_edges[1]-bin_edges[0])/2.)
      evts_unc = []
      for i in range(len(evts)):  #TODO:how ROOT do uncertainty?
        if (evts[i] <= 0):
          evts_unc.append(1)
        else:
          evts_unc.append(np.sqrt(evts[i]))
      evts_unc = np.array(evts_unc)

    while not PedFitComplete:
      #Fit pedestal and exponential tail from failed dynode hits
      print("                         [C1 (amplitude), m1, s1]")
      print(" > PEDESTAL PARAMETERS: " + str(init_params["PedParams"]))
      ped_opt, ped_cov, ped_xdata, ped_ydata, ped_yunc = GainFinder.FitPedestal(evts, bin_centers, evts_unc, init_params["PedParams"], init_params["PedFitRange"], fit_tail=FIT_TAIL, exp_fit_range=exp_fit_range)

      if ped_opt is None:   #TODO:what if no pedestal?
        print(" > PEDESTAL FIT FAILED... BAD PMT?  SKIPPING")
        PedFitComplete = True
        GoodPedFit = False
        FitComplete = True
        GoodFit = False
        continue

      pl.PlotPedestal(ped_xdata, ped_ydata, fn.gauss1, ped_xdata, ped_opt, "GaussPlusExpo")

      above_ped = 0
      past_ped = np.where(ped_xdata > (ped_opt[1] + 3.*ped_opt[2]))[0]


      if FIT_TAIL:
        plt.plot(ped_xdata[past_ped], ped_ydata[past_ped])
        plt.plot(ped_xdata[past_ped], fn.expo(ped_xdata[past_ped], ped_opt[3], ped_opt[4], ped_opt[5]))
        above_ped = np.sum(ped_ydata[past_ped] - fn.expo(ped_xdata[past_ped], ped_opt[3], ped_opt[4], ped_opt[5]))
      else:
        above_ped = np.sum(ped_ydata[past_ped] - fn.gauss1(ped_xdata[past_ped], ped_opt[0], ped_opt[1], ped_opt[2]))
      plt.show()
      print(" > 4SIGMA PAST PED, EXP. SUBTRACTED: " + str(above_ped))
      if (above_ped < 300):
        print("Low statistics beyond pedestal! May just be fitting on fluctuations.")
        skip_fit = str(input("Skip this fit?"))
        if (skip_fit in ["y", "Y", "yes", "Yes", "YES", "yEs"]):
          PedFitComplete = True
          GoodPedFit = False
          FitComplete = True
          GoodFit = False
          continue

      keep_ped = str(input("Keep pedestal fit? [y/N]: "))
      if (keep_ped in ["y", "Y", "yes", "Yes", "YES", "yEs"]):
        ped_good = str(input("Happy with pedestal fit? [y/N]: "))
        if (ped_good in ["y", "Y", "yes", "Yes", "YES", "yEs"]):
          PedFitComplete = True
          GoodPedFit = True
        else:
          if FIT_TAIL:
            fit_min = str(input("Exponential window min: "))
            fit_max = str(input("Exponential window max: "))
            exp_fit_range = [float(fit_min), float(fit_max)]
      else:
        print(" > setting optimized pedestal parameters to 0...")
        GainFinder.ped_mean = -999.
        GainFinder.ped_sigma = -999.
        ped_opt[0] = 0.
        #ped_opt[1] = 0.
        #ped_opt[2] = 0.
        VisiblePed = NOTVIS
        PedFitComplete = True
    #end while not PedFitComplete loop      


    UseDefault = "y"

    print(" [debug] ped_opt: " + str(ped_opt))

    while not FitComplete:
      print(" > SIGMA LIMIT IS: " + str(ped_opt[2]))
      if (fitType == "EXP2SPE"):
        GainFinder.upper_bounds[8] = 0.001 #reset tau
        if (VisiblePed == VIS):
          GainFinder.setTauMax(4.*abs(ped_opt[2])) #juju:defined gaussian doesn't care about sign of sigma so it may produce negative sigma
        else:
          print(" > TAU MAX IS: " + str(GainFinder.upper_bounds[8]))
      init_mean = str(input("Guess at SPE mean: "))
      #init_mean = 0.001   #hardcoded
      if ((pmt == 343) and (HASSRC)):
        init_mean = 0.005
      if ((pmt == 456) and (HASLED)):
        init_mean = 0.0006
      if (float(init_mean) >= MAXMU):
        print("TRY LESS THAN " + str(MAXMU))
        continue
      try:
        GainFinder.setInitMean(float(init_mean))
      except ValueError:
        print("Input not recognized.  Trying a save bet of 0.001")
        GainFinder.setInitMean(0.001)
      if (UseDefault in ["y", "Y", "yes", "Yes", "YES", "yEs"]):
        if (VisiblePed == 0.):  #if ped not visible
          ##### SPECIAL FITS ####################################
          if ((pmt == 343) and (HASSRC)):
            print(" [debug] fitting pmt #343")
            GainFinder.upper_bounds = [1E4, 0.007, 0.0025]
            print(GainFinder.upper_bounds)
            popt, pcov, xdata, ydata, y_unc = GainFinder.FitPEPeaks(evts, bin_centers, evts_unc, exclude_ped=False, subtract_ped=False, fit_range=[0.0002,0.008])
            GainFinder.upper_bounds = init_params["GaussUB"]    #reset UB

          if ((len(spf.index) != 0) and (pmt in list(spf['pmtID']))):
            print(" [debug] SPECIAL FIT RANGE FOR PMT #%d"%pmt)
            popt, pcov, xdata, ydata, y_unc = GainFinder.FitPEPeaks(evts, bin_centers, evts_unc, exclude_ped=False, subtract_ped=False, fit_range=[spf[spf['pmtID'] == pmt]['fr_LB'].values[0], spf[spf['pmtID'] == pmt]['fr_UB'].values[0]])

          else:
            GainFinder.upper_bounds = init_params["GaussUB"]
            print(GainFinder.upper_bounds)
            #popt, pcov, xdata, ydata, y_unc = GainFinder.FitPEPeaks(evts, bin_centers, evts_unc, exclude_ped=False, subtract_ped=False)
            #using fit range
            popt, pcov, xdata, ydata, y_unc = GainFinder.FitPEPeaks(evts, bin_centers, evts_unc, exclude_ped=False, subtract_ped=False, fit_range=init_params["GaussFitRange"])
          #popt, pcov, xdata, ydata, y_unc = GainFinder.FitPEPeaks(evts, bin_centers, evts_unc, exclude_ped=False, subtract_ped=False)
          #using fit range
          #popt, pcov, xdata, ydata, y_unc = GainFinder.FitPEPeaks(evts, bin_centers, evts_unc, exclude_ped=False, subtract_ped=False, fit_range=init_params["GaussFitRange"])
        else:   #if ped is visible
          if (pmt == 343):
            print(" [debug] fitting pmt #343")
            GainFinder.upper_bounds = [1E4, 0.007, 0.002]
            print(GainFinder.upper_bounds)
            popt, pcov, xdata, ydata, y_unc = GainFinder.FitPEPeaks(evts, bin_centers, evts_unc, exclude_ped=True, subtract_ped=False, fit_range=[0,0.008])
          else:
            GainFinder.upper_bounds = init_params["GaussUB"]
            print(GainFinder.upper_bounds)
            # WITH fit range
            #popt, pcov, xdata, ydata, y_unc = GainFinder.FitPEPeaks(evts, bin_centers, evts_unc, exclude_ped=False, subtract_ped=True, fit_range=init_params["GaussFitRange"])   #TODO:throwing an error about sigma
            # WITHOUT fit range
            popt, pcov, xdata, ydata, y_unc = GainFinder.FitPEPeaks(evts, bin_centers, evts_unc, exclude_ped=False, subtract_ped=True)
      elif (UseDefault in ["n", "N", "no", "No", "NO", "nO"]):
        InitialParams = pin.GetInitialParameters(fitType)
        #popt, pcov, xdata, ydata, y_unc = GainFinder.FitPEPeaks(charge)

      if popt is None:
        print("FIT FAILED.  WE'RE MOVING ON TO THE NEXT CHANNEL")
        FitComplete = True
        GoodFit = False
        continue    #the rest of this loop is skipped; UseDefault basically hard-coded
      print("BEST FIT PARAMETERS: " + str(popt))
      #pl.PlotHistPEDAndPEs_V2(bin_centers, evts, ped_opt, popt, fitType, VisiblePed)
      pl.PlotHistPEDAndPEs_V2(pmt, NUMARG, xdata, ydata, bin_centers, evts, ped_opt, popt, fitType, VisiblePed)
      if popt is None:
        retry_fit = str(input("Fit failed! Retry? [y/N]: "))
        if (retry_fit not in ["y", "Y", "yes", "Yes", "YES", "yEs"]):
          FitComplete = True
          continue
        else:
          UseDefault = str(input("Use default fit parameters? [y/N]"))
      approve_fit = str(input("Fit converged! Happy with this fit? [y/N]: "))
      #approve_fit = "Y"   #hardcoded
      if (approve_fit in ["y", "Y", "yes", "Yes", "YES", "yEs"]):
        FitComplete = True
        GoodFit = True
      else:
        retry = str(input("Try again? [y/N]: "))
        if (retry not in ["y", "Y", "yes", "Yes", "YES", "yEs"]):
          FitComplete = True
          GoodFit = False
    #end while not FitComplete loop

    if GoodFit:
      if (VisiblePed == VIS):
        #With the pedestal and 1PE peak fit, estimate the PV ratio
        Valley_inds = np.where((xdata > ped_opt[1]) & (xdata < popt[1]))
        try:
          Valley_min = np.argmin(ydata[Valley_inds])
        except ValueError:
          print(" !! ERROR !! UNABLE TO FIND P/V RATIO")
          Valley_estimate = -999.
          Peak_estimate = 1.
          PV_unc = -999.
        else:
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
#      db[fitType]["RunNumber"].append(nrun)
#      db[fitType]["LEDsOn"].append(ap.LED)
#      db[fitType]["LEDPINs"].append(ap.PIN)
#      db[fitType]["Date"].append(ap.DATE)
#      db[fitType]["V"].append(int(ap.VOLTS))
      if (VisiblePed == VIS):
        db[fitType]["PV"].append(Peak_estimate/Valley_estimate)
        db[fitType]["PV_unc"].append(PV_unc)
      #else:
      #  db[fitType]["PV"].append(-999.)
      #  db[fitType]["PV_unc"].append(-999.)
      errs = np.sqrt(np.diag(pcov))
      if fitType in ["Gauss2","Gauss3", "SPE"]:   #TODO:add SPE json
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
      if fitType in ["Gauss1"]:
        db[fitType]["c1Height"].append(popt[0])
        db[fitType]["c1Mu"].append(popt[1])
        db[fitType]["c1Sigma"].append(popt[2])
        db[fitType]["c1Height_unc"].append(errs[0])
        db[fitType]["c1Mu_unc"].append(errs[1])
        db[fitType]["c1Sigma_unc"].append(errs[2])
  with open(DBFILE, "w") as dbfile:
    print("\nSAVING TO DATABASE...")
    json.dump(db, dbfile, sort_keys=False, indent=4)

  print("DONE!")

