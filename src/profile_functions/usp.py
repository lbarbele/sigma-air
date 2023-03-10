import numpy as np

def usp(x, nmax, xmax, l, r):
  z = np.maximum(1 + (r/l) * (x - xmax), 1e-5)
  return nmax * np.exp((1 + np.log(z) - z) / r**2)

def guess(x, y):
  return [y.max(), x[y.argmax()], 200, 0.25]

usp.guess = guess
usp.npar = 4