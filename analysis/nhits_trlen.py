import numpy as np, pandas as pd, matplotlib.pyplot as plt

#data
raw_2630 = pd.read_csv("nhits_trlen_r2630.txt", sep=",")
raw_2633 = pd.read_csv("nhits_trlen_r2633.txt", sep=",")
raw_data = pd.concat([raw_2630, raw_2633], ignore_index=True) 
raw_data = raw_data[raw_data['track_fit'] > 0]

#mc
raw_mc = pd.read_csv("nhits_trlen_wcsim.txt", sep=",")
raw_mc = raw_mc[raw_mc['track_fit'] > 0]

# total nhits vs fitted track length
plt.scatter(raw_data['track_fit'], raw_data['nhits'], alpha=0.8, label='data')
plt.scatter(raw_mc['track_fit'], raw_mc['nhits'], c='orange', marker='^', alpha=0.8, label='wcsim')
plt.xlabel("fitted track length [cm]", fontsize=14)
plt.ylabel("total num hits", fontsize=14)
plt.title("Total Number of Hits in Event", fontsize=18)
plt.legend()
plt.show()

# nhits in cone vs fitted track length
plt.scatter(raw_data['track_fit'], raw_data['nhits_incone'], alpha=0.8, label='data')
plt.scatter(raw_mc['track_fit'], raw_mc['nhits_incone'], c='orange', marker='^', alpha=0.8, label='wcsim')
plt.xlabel("fitted track length [cm]", fontsize=14)
plt.ylabel("total num hits", fontsize=14)
plt.title("Number of Hits Inside Cone in Event", fontsize=18)
plt.legend()
plt.show()

# total pe vs fitted track length
plt.scatter(raw_data['track_fit'], raw_data['totpe'], alpha=0.8, label='data')
plt.scatter(raw_mc['track_fit'], raw_mc['totpe'], c='orange', marker='^', alpha=0.8, label='wcsim')
plt.xlabel("fitted track length [cm]", fontsize=14)
plt.ylabel("total pe", fontsize=14)
plt.title("Total Number of PE in Event", fontsize=18)
plt.legend()
plt.show()

# pe in cone vs fitted track length
plt.scatter(raw_data['track_fit'], raw_data['totpe_incone'], alpha=0.8, label='data')
plt.scatter(raw_mc['track_fit'], raw_mc['totpe_incone'], c='orange', marker='^', alpha=0.8, label='wcsim')
plt.xlabel("fitted track length [cm]", fontsize=14)
plt.ylabel("total pe", fontsize=14)
plt.title("Number of PE Inside Cone in Event", fontsize=18)
plt.legend()
plt.show()

