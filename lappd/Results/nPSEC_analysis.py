"""
  original file: PSEC_analysis
  written by: M. Breisch

  purpose: calibrate pedestal in data and reorder
           samples per event

  modified by: J. He

  usage: python nPSEC_analysis.py [datafile] [savefolder] [pedfile1]
         [pedfile2]

"""

import os, sys
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

OFFSET = 100 # offset for wrap-around
N_SAMPLE = 256 # Number of samples per waveform
N_CHANNEL = 30 # Number of channels per acdc board
N_BOARDS = 8 # Maximum number of acdc boards
SIGN = -1 # Setting for the expected sign of the pulse
THRESHOLD = 500 # Setting for the threshold to count a pulse as a pulse
WIDTH_NS = 5 # Setting for the expected width of a puse

# Function to load a set of events from one acdc board at a time
def load_board_data(filename, offset):
    # Loads 30 channels with an offset that is determined by the board number 
	raw_data = np.loadtxt(filename, delimiter=" ", usecols = range(0+offset,30+offset))
    # Return a matrix of data with the dimensions [N*256,30], 
    # where n is the number of available events in the file
	return raw_data

# Function to get the amount of read-out acdc boards from the amount 
# of available channels
def get_board_number(filename):
    # Read the first line of the file and split it on every ' '
    f = open(filename, "r").readline()
    # Then count the amount of entries
    connectedBoards = len(f.split())
    # Return the number of acd boards
    return connectedBoards

# Function to determine the pedestal of the current PSEC chip
def getPedestal(channel, evt_meta):
    # Depending on the current channels corresponding PSEC chip
    # read the metadata coloumn to get the set pedestal value
    if ch>=0 and ch<=5:
        pedestal = int(evt_meta[21],16)
    elif ch>=6 and ch<=11:
        pedestal = int(evt_meta[22],16)
    elif ch>=12 and ch<=17:
        pedestal = int(evt_meta[24],16)
    elif ch>=18 and ch<=23:
        pedestal = int(evt_meta[25],16)
    elif ch>=24 and ch<=29:
        pedestal = int(evt_meta[26],16)
    else:
        print("Pedestal error")
    # Return the pedestal value
    return pedestal

# Function to restructure the data of an acdc board given by the clockcycle 
# the trigger happend in 
def restructure(yd, cycleBit):
  # The cycleBit is given by the metadata and determines which of the 8
  # 320 MHz clockcycles the trigger happend in 32 samples * this bit is 
  # then the actual first sample 
  cycleSample = 32 * cycleBit
  print("DEBUG: cycleSample = " + str(cycleSample))
#  print(yd)

  reorder = []
  for i in range(cycleSample, N_SAMPLE):
    reorder.append(i)
  for i in range(cycleSample):
    reorder.append(i)

  new_vector = yd.reindex(reorder)

  # Retrun this new restructured array
  return new_vector

# Function to check the waveform for the sign of its pulse, if the sign matches the expected sign
# return true. If it does not match return false
def checkSign(data, pedestal):
    # Look for the global maximum and minimum in the samples of the waveform
    max_data = np.amax(data)
    min_data = np.amin(data)
    # Calculate the difference between the glomal extrema and the pedestal
    delta_max = abs(max_data-pedestal)
    delta_min = abs(min_data-pedestal)
    # Create an empty sign to be set
    sign = 0
    # Compare the threshold set to determine peaks with the gloabal extrema
    # Depending on the result choose a sign or thow an error
    if delta_max>THRESHOLD and delta_min>THRESHOLD:
        sign = 2
    elif delta_max>THRESHOLD and delta_min<THRESHOLD:
        sign = 1
    elif delta_max<THRESHOLD and delta_min>THRESHOLD:
        sign = -1
    # Catch the sign just being empty
    if sign==0 or sign==2:
        print("ERROR sign is " + str(sign))
    # Compare the calculated sign with the expected sign
    if sign==SIGN:
        return True
    else:
        return False

# Function to check if the pulse height is enough to be counted as a pulse
def checkHeight(data,pedestal):
    checkMark = False
    # Depending on the expected sign switch between minima and maxima search
    if SIGN==1:
        max_data = np.amax(data)
    elif SIGN==-1:
        max_data = np.amin(data)
    else:
        print("SIGN error") 
    # Calculate the difference between the glomal extrema and the pedestal
    delta = abs(max_data-pedestal)
    # If the difference between pedestal and max/min pulse height is enough
    # return either false or true
    if delta > THRESHOLD:
        checkMark = True
    return checkMark
    
# Function to check pulse length
def checkWidth(data, pedestal):
    checkMark = False   
    x = range(0,N_SAMPLE)
    i_r = 0
    i_l = 0
    # Depending on the expected sign switch between minima and maxima search
    if SIGN==1:
        max_data = np.amax(data)
    elif SIGN==-1:
        max_data = np.amin(data)
    else:
        print("SIGN error") 
    pos_max = np.argmax(data)
    for i in range(1,N_SAMPLE-pos_max):
        if abs(data[pos_max+i]-pedestal) < max_data-0.9*(max_data-pedestal) and i_r==0:
            i_r = i
        if abs(data[pos_max-i]-pedestal) < max_data-0.9*(max_data-pedestal) and i_l==0:  
            i_l = i
        if i_r!=0 and i_l!=0:
            break
    bins = 25/256
    width = (i_l+i_r)*bins
    
    if width/2 < WIDTH_NS/2+0.34*WIDTH_NS or width/2 > WIDTH_NS/2-0.34*WIDTH_NS:
        checkMark = True
    return checkMark
    

####################################################################
# Main execution:::::::::
if __name__ == "__main__":
  # Set the filename from an input argument
  print("syntax: python nPSEC_analysis.py [datafile] [savefolder] [pedfile1] [pedfile2] ...")
  filename = sys.argv[1] # .txt data file
  fname = os.path.basename(filename)
  savefolder = sys.argv[2] # save directory

  # Load pedestal data
  ped_ctr = 0
  ped = pd.DataFrame([])
  for p in range(3, len(sys.argv)):
    pedfile = sys.argv[p] # .txt pedestal file for calibration
    tmp = pd.read_csv(pedfile, sep=' ', header=None)
    ped = ped.append(tmp, ignore_index=True)
    ped_ctr += 1

  ped = ped.iloc[:, 0:30] # get rid of last col NaN; cols are labeled 0-29
  print("Num of pedestal files loaded: " + str(ped_ctr))

  df = pd.read_csv(filename, sep=' ', header=None)
  ncols = len(df.columns)-1
#  print("DEBUG: total num of columns: " + str(ncols))
  df = df.iloc[:, 0:ncols] # get rid of last col (NaN); cols labeled 0-ncols

  # Get the number of acdc boards that were read out
  num_boards = int((ncols-1)/31) # num cols per event is 31 (30+1) with 0th col being sample number; HARDCODED
  print("Num of boards: " + str(num_boards))

  # Get the num of recorded evts
  number_of_events = int(len(df.index)/N_SAMPLE)
  print("Total num of evts: " + str(number_of_events))

  # Loop ober all the read out acdc boards
  for nb in range(num_boards): # for each board
    # get correct ped data
    ped_df = ped.iloc[nb*256:(nb+1)*256]
    ped_df.index = range(256)

    for ev in range(number_of_events): # for each event
      # define a temporary df for the event block
      tdf = df.iloc[ev*N_SAMPLE:(ev+1)*N_SAMPLE, (nb*(N_CHANNEL+1)+1):((nb+1)*(N_CHANNEL+1)+1)] # includes metadata col
      tdf.columns = range(N_CHANNEL+1) # relabel cols 0-30

      # get metadata for event
      evt_meta = tdf.iloc[:, 30] # HARDCODED metadata col
      # extract clockcycle bit
      bit = int(evt_meta.iloc[26], 16) # CHECK DATA & README

      # adjust pedestal
      tdf.index = range(N_SAMPLE) # relabel indices to match ped df
      tdf = tdf.iloc[:, 0:N_CHANNEL] # get rid of metadata column
#      tdf.columns = range(N_CHANNEL) # relabel columns to match ped
      tdf = tdf - ped_df

      # reorder events based on clockcycle bit
      sampleT0 = bit*32
      print("DEBUG: sampleT0: " + str(sampleT0))

      reorder = []
      for i in range(sampleT0, N_SAMPLE):
        reorder.append(i)
      for i in range(sampleT0):
        reorder.append(i)

      tdf = tdf.reindex(reorder)
      tdf.index = range(N_SAMPLE) # relabel the indices 0-256

      # account for wrap-around
      if (OFFSET != 0):
        reorder = []
        for i in range(OFFSET, N_SAMPLE):
          reorder.append(i)
        for i in range(OFFSET):
          reorder.append(i)

        tdf = tdf.reindex(reorder)
        tdf.index = range(N_SAMPLE)

      if (ev == 0): # define new df for first event
        ndf = tdf
#        hdf = tdf.max().to_frame().T # hist of max pulse per chn per ev
#        rms_df = np.sqrt((tdf**2).sum()/len(tdf)).to_frame().T
        rms_df = tdf.var().to_frame().T
#        print("DEBUG: len of tdf: " + str(len(tdf)))
        print("DEBUG: len of first restructured evt: " + str(len(ndf)))
      else: # append calibrated and reordered events for the rest
        ndf = ndf.append(tdf, ignore_index=True)
#        hdf = hdf.append(tdf.max().to_frame().T, ignore_index=True)
#        rms_df = rms_df.append(np.sqrt((tdf**2).sum()/len(tdf)).to_frame().T, ignore_index=True)
        rms_df = rms_df.append(tdf.var().to_frame().T, ignore_index=True)
        print("DEBUG: len of appending ndf: " + str(len(ndf)))

    # after all events processed, save ndf, hdf
    ndfname = savefolder + 'rs_bd' + str(nb) + '_' + fname
    print("restructured data found in: " + ndfname)
    ndf.to_csv(ndfname, sep=' ', header=False, index=True)

#    hdfname = savefolder + 'pulse' + fname
#    print("max pulse height per chn per evt found in: " + hdfname)
#    hdf.to_csv(hdfname, sep=' ', header=False, index=True)

    rms_dfname = savefolder + 'rms_bd' + str(nb) + '_' + fname
    print("rms data found in: " + rms_dfname)
    rms_df.to_csv(rms_dfname, sep=' ', header=False, index=True)

    # Get the pedestal value from the metadata
#    pedestal = getPedestal(ch, evt_meta) # ???
    # Check the waveform for a pulse by checking on the 
    # correct sign as well as pulse height
####################################################################
# From this point on you have x and y available as arrays to work with 
## x is a set arrays from 0 to 255 representing the samples
## y is the array containing the data of one waveform (which is already 
# restructured by correcting the clockcycle with the trigger in it)
# Right here is within 3 for loops going over boards>channels>events to 
# allow for event to event evaluation.
# Additional information available for one event:
## pedestal which reads the set pedestal value from the metadata
## evt_meta which is the entire array of metadata available
# The following evaluation is just a quick example/test evaluation to count
### pulses per channel and represent them.
####################################################################
####################################################################
