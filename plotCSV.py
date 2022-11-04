#!/opt/local/bin/python2.7

# This is a preliminary PMT pulse distribution script.

from matplotlib import pyplot as plt
import numpy as np

FILE = 'pmt_waveforms001.csv'
PEAK_VOLTAGE = 0.003 # V ; peak value of the blip
#dT = 2E-10 # s
dT = 1E-9 # s
IMPEDANCE = 50 # Ohms


def main():
    # open data file
    print "Reading file..."

    with open(FILE) as f:
        data = np.loadtxt(f, delimiter=',', dtype='string', comments='#',
                          skiprows=7, # ignore header rows
                          usecols=None)

    print "Creating charge distributions..."
    # initialize variables
    charge = []
    time = 0
    voltage = 0.0
    frameStart = 0
    frameCounter = 0

    voltage += float(data[0][4]) # store first sample to avoid out of bounds j-1 below
    for j in range (1, len(data)): # for each sample

        # if we're not at the end of the frame
        if float(data[j][3]) > float(data[j-1][3]):
            voltage += float(data[j][4]) # add to the area of the frame
            time = time+1 # increment time

        # else we're at the end of the frame
        else:
            skip_frame = False # Initialize skip frame variable
            frameCounter += 1 # increment frame count

            # sum pedestal over first 5% of the frame
            pedestal = 0
            DC = 0
            max_value = 0
            c = 0
            for k in range(frameStart, frameStart + (j - frameStart)/20):
                # Set relative DC level for checking for any voltages past a certain threshold
                DC = (float(DC*(k - frameStart)) + float(data[k][4]))/(float(k - frameStart + 1))
                # Check for any voltages past threshold
                if abs(float(data[k+1][4]) - DC) > PEAK_VOLTAGE:
                    # skip the entire frame
                    skip_frame = True
                else: # If no peaks, add to pedestal
                    pedestal += float(data[k][4])
            pedestal *= ((j - frameStart) / (k - frameStart)) # scale pedestal to full frame width

#            # Try to plot ONLY 1 p.e.
#            frameStart = frameStart + (j - frameStart)/20
#            c = frameStart
#            while skip_frame == False and c in range(frameStart, j):
#                DC = (float(DC*(c- frameStart)) + float(data[c][4]))/(float(c - frameStart + 1))
#                # Check for any voltages past threshold
#                if abs(float(data[c][4]) - DC) > 0.002:
#                    break
#                c += 1
#            else:
#                skip_frame = True

            if skip_frame == True:
                print 'skipped frame:', frameCounter + 1
            else: # store the pulse's charge
                charge.append( (-(voltage - pedestal) * dT) / IMPEDANCE) # V*s/Ohm
            
            # prepare for next frame
            time = 0
            voltage = 0.0
            DC = 0
            frameStart = j

    np.savetxt('charge_data_001.txt', charge)
#
#    # plot the charge distribution
#    fig = plt.figure()
#    ax1 = fig.add_subplot(111)
#
#
#    n, bins, patches = ax1.hist(charge, bins=100, facecolor='orange') #  range = [-1E-12, 6E-12], weights=np.ones_like(charge)/len(charge)
#    plt.yscale('log', nonposy='clip')
#    plt.xlabel('Coulombs')
#    plt.ylabel('Counts')
#    plt.show()
#
#    np.savetxt('~/y_data_900.txt', n)
#    np.savetxt('~/x_data_900.txt', bins)
    return


# Plotting the time and voltage data from input file
def plot(frame):
    # open data file
    with open(FILE) as f:
        data = np.loadtxt(f, delimiter=',', dtype='string', comments='#',
                          skiprows=7, # ignore header rows
                          usecols=None)
    f.close()

    i = 0 
    frame_length = 0
    xdata = []
    ydata = []

    for j in range(len(data)):
        frame_length += 1

        if float(data[j][3]) < float(data[j-1][3]): # then we're on a new frame: check if desired frame
            if i == (frame - 1): # plot the frame
                i += 1
                for k in range((j+1) - frame_length, (j+1)):
                    xdata.append(data[k][3])
                    ydata.append(data[k][4])

                plt.plot(xdata, ydata)
                plt.xlabel('Time(s)')
                plt.ylabel('Voltage(V)')
                plt.show()
                plt.clf()
                break

            else:
                i += 1
                frame_length = 0

if __name__ == '__main__':
    main()


#def peak_detector():
#    # open data file
#    with open(FILE) as f:
#        data = np.loadtxt(f, delimiter=',', dtype='string', comments='#',
#                          skiprows=7, # ignore header rows
#                          usecols=None)
#    f.close()
#
#    peak_detected = []
#    frameStart = 0
#
#    for j in range(len(data)):
#        DC = 0
#        time = 0
#        if j == 0 or float(data[j][3]) < float(data[j-1][3]): # then we're on a new frame: check if peak detected
#            peak = False
# 
#            for k in range(frameStart, j):
#                # Set relative DC level for checking for any voltages past a certain threshold
#                DC = (float(DC*(k- frameStart)) + float(data[k][4]))/(float(k - frameStart + 1))
#                # Check for any voltages past threshold
#                if abs(float(data[k][4]) - DC) > PEAK_VOLTAGE:
#                    peak = True
#                    time = data[k][3]
#                    break
#
#
#            if peak == True:
#                peak_detected.append([True, time])
#            else:
#                peak_detected.append([False, 'none'])
#
#            frameStart = j
#            DC = 0
#
#    print 'Peaks detected for:'
#    for i in range(len(peak_detected)):
#        if peak_detected[i][0]:
#            print 'Frame ', i+1
#            print peak_detected[i][1]
#
#                    
