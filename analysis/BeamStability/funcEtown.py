'''
  orphan functions
'''

import numpy as np
import matplotlib.pyplot as plt


candidate_ts = []
for i in range(len(pot_grad)):
  if ((pot_grad[i] < avg_grad-NSTD*std_grad) or (pot_grad[i] > avg_grad+NSTD*std_grad)):
    #print("candidate timestamp: " + str(ts_grad[i]))
    candidate_ts.append(ts_grad[i])
    #plt.axvline(x = ts_grad[i], color = 'k', linestyle='-.')

#plotting
plot_ts = []
tmp_list = []
plot_ts.append(candidate_ts[0]) #add first timestamp
tmp_list.append(candidate_ts[0])

j = 1
while (j < len(candidate_ts)):
  if ((candidate_ts[j] - candidate_ts[j-1]) > TIME_DIFF):
#    print(" [DEBUG] tmp_list length: " + str(len(tmp_list)))
    if (len(tmp_list) > 4):
      #add first and last element only
      plot_ts.append(tmp_list[0])
      plot_ts.append(tmp_list[-1])
    elif (len(tmp_list) == 1):
      #plot_ts.append(tmp_list[0])
      print(" @@@ single boi timestamp found! : " + str(tmp_list[0]))
    #reset list
    tmp_list = []
    tmp_list.append(candidate_ts[j])
  elif (j == len(candidate_ts)-1):
#    print(" [DEBUG] last set!")
#    print(" [DEBUG] tmp_list length: " + str(len(tmp_list)))
    plot_ts.append(tmp_list[0])
    plot_ts.append(tmp_list[-1])
  else:
    tmp_list.append(candidate_ts[j])
  j+=1


