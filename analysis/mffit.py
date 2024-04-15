# script to find difference btwn fit and truth info

#imports
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt


truth = pd.read_csv("truetrack/true_track_len_wcsim_0-999.txt", sep=",", header=None)
truth = truth.rename(columns={0:"event", 1:"track_len", 2:"left_avg", 3:"right_avg"})

fit = pd.read_csv("fitbyeye_wcsim_0-999.txt", sep=",", header=None)
#fit = pd.read_csv("fitbyeye_Paul_wcsim_0-999.txt", sep=",", header=None)
fit = fit.rename(columns={0:"event", 1:"track_len"})

#print(type(truth['track_len']))
#print(fit)

ldiff = []

print("events where track len diff > 500cm")
for i in range(len(truth)):
  for j in range(len(fit)):
    if (fit['event'][j] == truth['event'][i]):
      diff = fit['track_len'][j] - truth['track_len'][i]
      if (abs(diff) > 500.):
        print(fit['event'][j], truth['event'][i])
        continue
      #ldiff.append(abs(diff))
      ldiff.append(diff)

#print(ldiff)

plt.hist(ldiff, density=False, bins=100, range=(-300,300), color="blue")  #orange:P, green:G
plt.xlabel("diff(fit-truth) [cm]", fontsize=20)
plt.ylabel("num events", fontsize=20)
plt.show()

print("Mean (w/o outliers): ", np.mean(ldiff))
print("SD (w/o outliers): ", np.std(ldiff))
print("RMS: ", np.sqrt(np.mean(np.array(ldiff)**2)))
