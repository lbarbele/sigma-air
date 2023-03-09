import numpy as np

def usp(x, nmax, xmax, l, r):
  z = np.maximum(1 + (r/l) * (x - xmax), 1e-5)
  return nmax * np.exp((1 + np.log(z) - z) / r**2)