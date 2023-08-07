"""
  Purpose: Check and test tank geometry

"""

### IMPORTS ###
import sys, os
import numpy as np, pandas as pd, matplotlib.pyplot as plt
from mpl_toolkits import mplot3d


### DEFINES ###
TANK_CTR_X = 0.         #[m]
TANK_CTR_Y = -0.144649  #[m]
TANK_CTR_Z = 1.681      #[m]
X0 = -0.60921       #mrdStartVtx
Y0 = -0.458123
Z0 = 3.3608
X1 = 0.657563       #mrdStopVtx
Y1 = -0.644904
Z1 = 4.5858

tankExitPointX = -45.9023
tankExitPointY = -26.1352
tankExitPointZ = 145.323

DETNUM = '385'  #'397'  #'400'

AX = -45.9253   #-45.9204   #-45.9173       #tank track
AY = -26.1393   #-26.1358   #-26.1379
AZ = -166.052   #-99.1874   #-57.5902

BX = 19.156     #-66.6787   #-53.0669       #vertex to pmt
BY = -41.9282   #86.3667    #86.3661
BZ = 53.0265    #125.527    #116.615

RX = 19.133     #-66.6967   #-53.0818
RY = -41.9323   #86.3634
RZ = -258.349   #-118.983   #-86.2976


### FUNCTIONS ###
def XYZ(x0, y0, z0, x1, y1, z1, u):
  """
    Return xyz coords of a new pt given 2 pts

  """
  x = (1.-u)*x0 + u*x1
  y = (1.-u)*y0 + u*y1
  z = (1.-u)*z0 + u*z1
  return((x,y,z))

def xyzDistance(x0, y0, z0, x1, y1, z1):
  return(np.sqrt((x1-x0)**2 + (y1-y0)**2 + (z1-z0)**2))


# initiate plotting
fig, ax = plt.subplots()
ax = plt.axes(projection='3d')

# load data
#ratpac positions
raw_rp = pd.read_csv("~/annie/analysis/ratpac_pmt_pos.txt",header=0)
print("======== RATPAC Geometry ========")
print(raw_rp.head(5))
print(raw_rp.columns)

#actual tank positions, used in toolanalysis
raw_ss = pd.read_csv("~/annie/analysis/FullTankPMTGeometry_mod.csv",header=0)
print("======== Actual Tank Geometry ========")
print(raw_ss.head(5))
print(raw_ss.columns)
raw_ss = raw_ss.drop(index=132)

# calculating potential vertices
xlist=[]; ylist=[]; zlist=[]
xlist2=[]; ylist2=[]; zlist2=[]   #switched start and stop vertices
for i in range(2,10,1):
  x,y,z = XYZ(X0,Y0,Z0,X1,Y1,Z1,i)
  xlist.append(x)
  ylist.append(y)
  zlist.append(z)

  x,y,z = XYZ(X1,Y1,Z1,X0,Y0,Z0,i)
  xlist2.append(x)
  ylist2.append(y)
  zlist2.append(z)

xyzDist=[]
for i in range(1,len(xlist),1):
  d = xyzDistance(xlist[i-1], ylist[i-1], zlist[i-1], xlist[i], ylist[i], zlist[i])
  xyzDist.append(d)
#print("distances btwn pts: ")
#print(xyzDist)

# plot TANK vs RATPAC pos; ratpac pos are in cm; in csv file pos are in m
#ax.scatter(raw_rp['x'], raw_rp['y'], raw_rp['z'], label='ratpac')
ax.scatter((raw_ss['x_pos']-TANK_CTR_X)*100., (raw_ss['y_pos']-TANK_CTR_Y)*100., (raw_ss['z_pos']-TANK_CTR_Z)*100., label='tank PMTs', s=25)
ax.scatter(0.,0.,0., label='(0,0,0)', color='red')

# plot tank pmt dir
#ax.scatter(raw_ss['x_dir']*100., raw_ss['y_dir']*100., raw_ss['z_dir']*100., label='PMT direction')
#dir_vec_origin = np.array([TANK_CTR_X*100.,TANK_CTR_Y*100.,TANK_CTR_Z*100.])
for i in range(len(raw_ss)):
  ax.quiver3D((raw_ss['x_pos'].iloc[i]-TANK_CTR_X)*100., (raw_ss['y_pos'].iloc[i]-TANK_CTR_Y)*100., (raw_ss['z_pos'].iloc[i]-TANK_CTR_Z)*100., raw_ss['x_dir'].iloc[i]*100., raw_ss['y_dir'].iloc[i]*100., raw_ss['z_dir'].iloc[i]*100., color='g', length=0.2)

# det 400 position
hitX = (raw_ss[raw_ss['detector_num'] == DETNUM]['x_pos']-TANK_CTR_X)*100. #-98.9842
hitY = (raw_ss[raw_ss['detector_num'] == DETNUM]['y_pos']-TANK_CTR_Y)*100. #60.2282
hitZ = (raw_ss[raw_ss['detector_num'] == DETNUM]['z_pos']-TANK_CTR_Z)*100. #59.0253
pmtDirX = raw_ss[raw_ss['detector_num'] == DETNUM]['x_dir']*100.
pmtDirY = raw_ss[raw_ss['detector_num'] == DETNUM]['y_dir']*100.
pmtDirZ = raw_ss[raw_ss['detector_num'] == DETNUM]['z_dir']*100.
#ax.quiver3D(0, 0, 0, hitX, hitY, hitZ, color='r', length=1.)
ax.quiver3D(hitX, hitY, hitZ, pmtDirX, pmtDirY, pmtDirZ, color='m', length=1.)

# ai vector
ax.quiver3D(0, 0, 0, AX, AY, AZ, color='b', length=1.)

# bi vector
ax.quiver3D(0, 0, 0, BX, BY, BZ, color='g', length=1.)
#ax.quiver3D(AX, AY, AZ, BX, BY, BZ, color='g', length=1.)
#ax.quiver3D(0, 0, 0, BX+AX, BY+AY, BZ+AZ, color='g', length=1.)

# Ri vector (tankExitPoint to PMT)
ax.quiver3D(tankExitPointX, tankExitPointY, tankExitPointZ, RX, RY, RZ, color='c', length=1.)

# test one pmt
dir_vec_origin = np.array([raw_ss['x_pos'].iloc[69]*100., raw_ss['y_pos'].iloc[69]*100.,raw_ss['z_pos'].iloc[69]*100.])
#ax.quiver3D(*dir_vec_origin, raw_ss['x_dir'].iloc[69]*100., raw_ss['y_dir'].iloc[69]*100., raw_ss['z_dir'].iloc[69]*100., color='r')

# plot mrd start/stop and vtx candidates
#ax.scatter(xlist, ylist, zlist, label='0,1')
#ax.scatter(xlist2, ylist2, zlist2, label='1,0')
#ax.scatter(X0, Y0, Z0, label='mrdStartVtx')
#ax.scatter(X1, Y1, Z1, label='mrdStopVtx')

ax.set_xlabel('X')
ax.set_ylabel('Y')
ax.set_zlabel('Z')
ax.legend()
plt.show()
