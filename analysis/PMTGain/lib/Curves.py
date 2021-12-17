'''
  Script containing curvy (and non-curvy, we don't judge) functions

'''

#imports
import numpy as np

def Norm(x, av, sd, N):
  #technically this is a normal distribution w/ factor of N
  '''
    x: data
    av: mean of gaussian dist
    sd: std dev of gaussian dist
    N: normalization const
  '''
  return( N/(np.sqrt(2.*np.pi)*sd) * np.exp(-(x-av)**2 / (2.*sd**2)) )

def double_gauss(x, av1, sd1, N1, av2, sd2, N2):
  #Adds another gaussian to fitted pedestal
  '''
    x: data
    av*: mean of gaussian dist
    sd*: std dev of gaussian dist
    N*: normalization const
  '''
  return( Norm(x, av1, sd1, N1) + (N2/(np.sqrt(2.*np.pi)*sd2)) * np.exp(-(x-av2)**2/(2.*sd2**2)) )

def db_gauss(x, mu1, sigma1, n1, mu2, sigma2, n2):
  #Simultaneously fit of pedestal and SPE peak
  return( n1/(np.sqrt(2.*np.pi)*sigma1) * np.exp(-(x-mu1)**2/(2.*sigma1**2)) + (n2/(np.sqrt(2*np.pi)*sigma2))*np.exp(-(x-mu2)**2/(2*sigma2**2)) )
