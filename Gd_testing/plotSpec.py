'''
  This script is used to plot spectra data from 
  a Shimadzu spectrometer

  written by: J. He
  date: 16 Dec 2021
  last updated: 06 Jan 2022
'''

#imports
import argparse
from parse import parse
import sys, os
import numpy as np
import matplotlib.pyplot as plt
import pandas as pd

#defines
DATADIR = "./data/"
NPLOTS = 5


#main
if __name__=='__main__':
  #load data
  flist = os.listdir(DATADIR)
  flist.sort()
  print(flist)  #debug

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

  print(bl_files)   #debug
  print(gd_files)
  print(mat_files)
  print(msc_files)

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
  for (mf,dt) in mat_files:
    raw = pd.read_csv(DATADIR+mf, sep=',', header=0, skiprows=1)
    df = raw[raw["Abs."] != ' ']
    ax.plot(df["Wavelength nm."], pd.to_numeric(df["Abs."]), label=dt)

  raw = pd.read_csv(DATADIR+"File_211215_121946_macartney_bluecable_1pct_Gd.txt", sep=',', header=0, skiprows=1)
  df1 = raw[raw["Abs."] != ' ']


  raw = pd.read_csv(DATADIR+"File_211216_121210_macartney_bluecable_1pct_Gd.txt", sep=',', header=0, skiprows=1)
  df2 = raw[raw["Abs."] != ' ']

  raw = pd.read_csv(DATADIR+"File_200811_103147_falmat_undersea_1pct_Gd.txt", sep=',', header=0, skiprows=1)
  df3 = raw[raw["Abs."] != ' ']

#  fig, ax = plt.subplots(1,1, sharex=True, sharey=True)
#  ax.plot(df_bl["Wavelength nm."], pd.to_numeric(df_bl["Abs."]), label='DI H2O baseline')
#  ax.plot(df_Gd["Wavelength nm."], pd.to_numeric(df_Gd["Abs."]), label='1% Gd soln')
#  ax.plot(df1["Wavelength nm."], pd.to_numeric(df1["Abs."]), label='after 15 mins')
#  ax.plot(df2["Wavelength nm."], pd.to_numeric(df2["Abs."]), label='after 24 hrs')
  ax.legend()
  ax.set_title("blue MacArtney 13-pin cable")
  ax.set_xlabel("Wavelength [nm]")
  ax.set_ylabel("Abs [a.u.]")
  plt.savefig("MA_blue13p_cable.png", dpi=300)
  ax.plot(df3["Wavelength nm."], pd.to_numeric(df3["Abs."]), label='Falmat after ~1 yr')
  ax.legend()
  plt.savefig("MA_blue13p_cable_wFalmat.png", dpi=300)
  plt.show()

