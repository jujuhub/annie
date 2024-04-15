import numpy as np
import os, sys


f_nopi = open("fitbyeye_wcsim_0-999.txt", "r")
l_nopi = f_nopi.readlines()
f_wpi = open("fitbyeye_wcsim_0-999_wpion.txt", "r")
l_wpi = f_wpi.readlines()

for ev_id_wpi in l_wpi:
  found_ev = False
  #print("out",ev_id_wpi[:-1])
  for ev_id_nopi in l_nopi:
    #print("in",ev_id_nopi[:-1])
    if (ev_id_wpi[:-1] in ev_id_nopi):
      print(ev_id_nopi[:-1])
      found_ev = True
  if (not found_ev):
    print(ev_id_wpi[:-1])
