import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from mpl_toolkits import mplot3d

# Load in MRD geometry
geo_df = pd.read_csv("/Users/juhe/annie/analysis/FullMRDGeometry_09_29_20.csv", skiprows=6, header=0, sep=',')
geo_df.head(3)
geo_df.columns


mrd_df = geo_df[geo_df['detector_system'] == 1]
print("num mrd pmts: " + str(len(mrd_df)))
mrd_df.head(3)

fmv_df = geo_df[geo_df['detector_system'] == 0]
print("num fmv pmts: " + str(len(fmv_df)))
fmv_df.head(3)

# Plot PMT positions
mrds_hit = [240, 184, 130, 70, 14, 218, 164, 110, 50]
pmts_hit_df = mrd_df[mrd_df.channel_num.isin(mrds_hit)]
fmv_df[fmv_df.channel_num.isin([71.,18.,150.,94.,38.])]


fig, ax = plt.subplots()
ax = plt.axes(projection = '3d')
#fig.set_size_inches(20,20)

ax.set_xlabel('X')
ax.set_ylabel('Y')
ax.set_zlabel('Z')

ax.scatter(mrd_df['x_center'], mrd_df['y_center'], mrd_df['z_center'], label='mrd', color='green')
ax.scatter(fmv_df['x_center'], fmv_df['y_center'], fmv_df['z_center'], label='fmv', color='orange')
ax.scatter(pmts_hit_df['x_center'], pmts_hit_df['y_center'], pmts_hit_df['z_center'], label='hit', color='red', s=150)

ax.legend()
plt.show()

# Check distances between MRD PMTs
'''
mrd_df['z_center'].unique()
l_zctr = list(mrd_df['z_center'].unique())

i=0
while i < len(l_zctr)-1:
    z_diff = l_zctr[i+1] - l_zctr[i]
    print("diff: " + str(z_diff))
    i+=1


mrd_df['y_center'].unique()
l_yctr = list(mrd_df['y_center'].unique())

i=0
while i < len(l_yctr)-1:
    y_diff = l_yctr[i+1] - l_yctr[i]
    print("diff: " + str(y_diff))
    i+=1


mrd_df['x_center'].unique()
l_xctr = list(mrd_df['x_center'].unique())

i=0
while i < len(l_xctr)-1:
    x_diff = l_xctr[i+1] - l_xctr[i]
    print("diff: " + str(x_diff))
    i+=1
'''
