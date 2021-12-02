#imports
import os, sys
import numpy as np
import matplotlib.pyplot as plt
from scipy.signal import find_peaks


if (len(sys.argv) != 2):
  print(" @@@@@ Missing filename !! @@@@@")
  print(" syntax: python findBeamStability.py [FILENAME]")
  exit(-1)

FILENAME=sys.argv[1]
if (FILENAME[-4:] != '.txt'):
  print(" @@@@@ Wrong file format !! Only .txt files plz !! @@@@@")
  exit(-1)


#constants
WNDW_SZ = 100   #TODO:play around w/ window sizes
GRAD_RNG = 100   #lower number results in larger gradients
NSTD = 4.5      #TODO:best criteria?
TIME_DIFF = 2.5e12   #TODO:find out units
TSTMP_BUF = 0.5e12


#defines
def removeZeroTimes(t, bp):
  '''
    input
    * t: list/array of timestamps
    * bp: list/array of beam POT values

    output
    * evttime: list of nonzero timestamps
    * beampot: list of corresponding POT values
  '''
  evttime = []
  beampot = []
  for i in range(len(t)):
    if (t[i] == 0):
      continue
    evttime.append(t[i])
    beampot.append(bp[i])
  return(evttime, beampot)


def findGrad(t, bp, width):
  '''
    input
    * t: list/array of timestamps
    * bp: list/array of beam POT values

    output
    * ts: list of timestamps (shortened by width)
    * grad: list of calculated gradients
  '''
  ts = []
  grad = []
  i = 0
  while (i < len(t)):
    if (i < width):
      i+=1
      continue
    grad.append((bp[i] - bp[i-width]) / (t[i] - t[i-width]))
    ts.append(t[i-width//2])
    i+=1
  return(ts, grad)

def mvAvgFilter(t, bp):
  '''
    input
    * t: list/array of timestamps
    * bp: list/array of beam POT values

    output
    * ts_smth: list of timestamps (shortened by WNDW_SZ)
    * pot_smth: list of averaged POT values
  '''
  ts_smth = []
  pot_smth = []
  w = 0
  while (w < len(t)-WNDW_SZ+1):
    this_wndw = bp[w:w+WNDW_SZ]
    wndw_avg = sum(this_wndw) / WNDW_SZ 
    ts_smth.append(t[w+WNDW_SZ//2])
    pot_smth.append(wndw_avg)
    w+=1
  return(ts_smth, pot_smth)

def plotTimestamps(candidate_ts):
  '''
    input
    * candidate_ts: list/array of candidate timestamps

    output
    * plot_ts: list of timestamps to plot
  '''
  plot_ts = []
  tmp_list = []
  tmp_list.append(candidate_ts[0])
  j = 1
  while (j < len(candidate_ts)):
    if ((candidate_ts[j] - candidate_ts[j-1]) > TIME_DIFF):
      if (len(tmp_list) > 1):
        #add first and last element only
        left_ts = tmp_list[0] - TSTMP_BUF
        plot_ts.append(left_ts)
        right_ts = tmp_list[-1] + TSTMP_BUF
        plot_ts.append(right_ts)
      elif (len(tmp_list) == 1):
        print(" @@@ single boi timestamp found! : " + str(tmp_list[0]))
        left_ts = tmp_list[0] - TSTMP_BUF
        plot_ts.append(left_ts)
        right_ts = tmp_list[0] + TSTMP_BUF
        plot_ts.append(right_ts)
      #reset list
      tmp_list = []
      tmp_list.append(candidate_ts[j])
      if (j == len(candidate_ts)-1 and len(tmp_list) == 1):
        left_ts = tmp_list[0] - TSTMP_BUF
        plot_ts.append(left_ts)
        right_ts = tmp_list[0] + TSTMP_BUF
        plot_ts.append(right_ts)
    elif (j == len(candidate_ts)-1):   #cluster towards end of run
      tmp_list.append(candidate_ts[j]) #add the last timestamp
      left_ts = tmp_list[0] - TSTMP_BUF
      plot_ts.append(left_ts)
      right_ts = tmp_list[-1] + TSTMP_BUF
      plot_ts.append(right_ts)
    else:
      tmp_list.append(candidate_ts[j])
    j+=1
  return(plot_ts)

########## main ##########
if __name__=='__main__':
  #load data
  ts_raw, bp_raw = np.loadtxt(FILENAME, dtype='float', comments='#', 
    delimiter=' ', unpack=True)

  #get rid of 0 evt times
  ts, bp = removeZeroTimes(ts_raw, bp_raw)

  for i in range(1,11): #DEBUG
    print(" [debug] typical time diff: " + str(ts[i] - ts[i-1]))

  #smooth data using moving average
  ts_smth, pot_smth = mvAvgFilter(ts, bp)

  #find gradient
  ts_grad, pot_grad = findGrad(ts_smth, pot_smth, GRAD_RNG)

  avg_grad = np.mean(pot_grad)
  std_grad = np.std(pot_grad)
  print("\n >>> avg_grad: " + str(avg_grad))
  print(" >>> std_grad: " + str(std_grad) + "\n")

  #TODO:figure out better way to deal with mostly stable beam data
  #keep threshold constant? minimum threshold?
  if (std_grad < 1.0):
    std_grad = 1.1  #arbitrarily chosen

  #convert to positive gradient values for peak finding
  pos_pot_grad = []
  for pg in pot_grad:
    if (pg < 0):
      pos_pot_grad.append(-pg)
    else:
      pos_pot_grad.append(pg)

  potgr_peaks, _ = find_peaks(pos_pot_grad, height=(avg_grad+NSTD*std_grad, None), distance=150)
  candidate_ts = [ts_grad[p] for p in potgr_peaks]
  for i in range(1, len(candidate_ts)):
    print(" [debug] diff in ts peaks: " + str(candidate_ts[i]-candidate_ts[i-1]))

  plot_ts = []
  tmp_list = []
  if candidate_ts:    #at least one timestamp found
    tmp_list.append(candidate_ts[0])
  if (len(candidate_ts) == 1):    #if only one timestamp found
    left_ts = tmp_list[0] - TSTMP_BUF
    plot_ts.append(left_ts)
    right_ts = tmp_list[-1] + TSTMP_BUF
    plot_ts.append(right_ts)
  j = 1
  while (j < len(candidate_ts)):
    if ((candidate_ts[j] - candidate_ts[j-1]) > TIME_DIFF):
      if (len(tmp_list) > 1):
        #add first and last element only
        left_ts = tmp_list[0] - TSTMP_BUF
        plot_ts.append(left_ts)
        right_ts = tmp_list[-1] + TSTMP_BUF
        plot_ts.append(right_ts)
      elif (len(tmp_list) == 1):
        print(" @@@ single boi timestamp found! : " + str(tmp_list[0]))
        left_ts = tmp_list[0] - TSTMP_BUF
        plot_ts.append(left_ts)
        right_ts = tmp_list[-1] + TSTMP_BUF
        plot_ts.append(right_ts)
      #reset list
      tmp_list = []
      tmp_list.append(candidate_ts[j])
      if (j == len(candidate_ts)-1 and len(tmp_list) == 1):
        left_ts = tmp_list[0] - TSTMP_BUF
        plot_ts.append(left_ts)
        right_ts = tmp_list[0] + TSTMP_BUF
        plot_ts.append(right_ts)
    elif (j == len(candidate_ts)-1):   #cluster towards end of run
      tmp_list.append(candidate_ts[j]) #add the last timestamp
      left_ts = tmp_list[0] - TSTMP_BUF
      plot_ts.append(left_ts)
      right_ts = tmp_list[-1] + TSTMP_BUF
      plot_ts.append(right_ts)
    else:
      tmp_list.append(candidate_ts[j])
    j+=1


  #find potential timestamps of potential transitions
  #TODO:figure out best criteria for choosing timestamps
  '''
  candidate_ts = []
  for i in range(len(pot_grad)):
    if ((pot_grad[i] < avg_grad-NSTD*std_grad) or (pot_grad[i] > avg_grad+NSTD*std_grad)):
      #print("candidate timestamp: " + str(ts_grad[i]))
      candidate_ts.append(ts_grad[i])
      #plt.axvline(x = ts_grad[i], color = 'k', linestyle='-.')
  '''

  print(" > num of candidate timestamps: " + str(len(candidate_ts)))
  print(" > num of plotted timestamps: " + str(len(plot_ts)))

  plt.subplot(3,1,1)
  plt.title("Run " + FILENAME[1:5])
  plt.ylabel("POT")
  plt.plot(ts, bp)
  for t in plot_ts:
    plt.axvline(x = t, color='m', linestyle='-', linewidth=1.2)
  

  plt.subplot(3,1,2)
  plt.ylabel("POT (smoothed)")
  plt.plot(ts_smth, pot_smth)
  for t in candidate_ts:
    plt.axvline(x = t, color='g', linestyle='-.')

  plt.subplot(3,1,3)
  plt.xlabel("event time")
  plt.ylabel("d(POT)/d(time)")
  plt.plot(ts_grad, pot_grad, 'g')
  #plt.plot(ts_grad, pos_pot_grad, 'g')
  for t in candidate_ts:
    plt.axvline(x = t, color='r', linestyle='-.')

  plt.show()
