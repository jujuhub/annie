'''
  This script is used to plot spectra data from 
  a Shimadzu spectrometer

  written by: J. He
  date: 16 Dec 2021
  last updated: 06 Jan 2022
'''

#imports
import argparse
from datetime import datetime
from parse import parse
import sys, os
import numpy as np
import matplotlib.pyplot as plt
import pandas as pd

#defines
DATADIR = "./data/"
NPLOTS = 3


#main
if __name__=='__main__':
  #load data
  flist = os.listdir(DATADIR)
  flist.sort()
  print("sorted files:\n", flist)  #debug

  pattern = "File_{date}_{time}_{matname}.txt"
  bl_files = []   #assumes files are named consistently
  gd_files = []   #just Gd soln
  mat_files = []  #soak material
  msc_files = []
  for f in flist:
    tmp = parse(pattern, f)
    if (tmp['matname'] == "dih2o_bl"):  #TODO:make it user-defined
      bl_files.append((f,tmp['date']))
    if (tmp['matname'] == "1pct_hipurity_Gd"):
      gd_files.append((f,tmp['date']))
    if (tmp['matname'] == "macartney_bluecable_1pct_Gd"):
      mat_files.append((f,tmp['date']))
    if (tmp['matname'] == "falmat_undersea_1pct_Gd"):
      msc_files.append((f,tmp['date']))

  print("baseline:\n", bl_files)   #debug
  print("Gd:\n", gd_files)
  print("material:\n", mat_files)
  print("misc:\n", msc_files)

  fig, ax = plt.subplots(1,1, sharex=True, sharey=True)

  #plot baseline
  raw = pd.read_csv(DATADIR+bl_files[0][0], sep=',', header=0, skiprows=1)
  df_bl = raw[raw["Abs."] != ' ']
  ax.plot(df_bl["Wavelength nm."], pd.to_numeric(df_bl["Abs."]), label='DI H2O baseline')

  #plot initial gd soln
  raw = pd.read_csv(DATADIR+gd_files[0][0], sep=',', header=0, skiprows=1)
  df_Gd = raw[raw["Abs."] != ' ']
  ax.plot(df_Gd["Wavelength nm."], pd.to_numeric(df_Gd["Abs."]), label='1% Gd soln')
  
  #plot material
  for (mf,dt) in mat_files[-NPLOTS:]:
    raw = pd.read_csv(DATADIR+mf, sep=',', header=0, skiprows=1)
    df = raw[raw["Abs."] != ' ']
    dtlabel = datetime.strptime(dt, '%y%m%d').date().isoformat()
    ax.plot(df["Wavelength nm."], pd.to_numeric(df["Abs."]), label=dtlabel)

  ax.legend()
  ax.set_title("blue MacArtney 13-pin cable")
  ax.set_xlabel("Wavelength [nm]")
  ax.set_ylabel("Abs [a.u.]")
  ax.set_ylim(ymax=1.25)
  plt.savefig("MA_blue13p_cable.png", dpi=300)
  ax.set_xlim(194.,420.)
  plt.savefig("MA_blue13p_cable_zoomx.png", dpi=300)

  #plot misc
  raw = pd.read_csv(DATADIR+msc_files[0][0], sep=',', header=0, skiprows=1)
  df_msc = raw[raw["Abs."] != ' ']
  ax.plot(df_msc["Wavelength nm."], pd.to_numeric(df_msc["Abs."]), label='Falmat after ~1 yr')

  ax.legend()
  plt.savefig("MA_blue13p_cable_wFalmat.png", dpi=300)
  plt.show()

