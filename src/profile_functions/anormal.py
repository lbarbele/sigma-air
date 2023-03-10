import numpy as np

def anormal(x, nmax, xmax, l, r):
  s = (l * (x < xmax) + r * (x >= xmax))
  z = (x - xmax) / s
  return nmax * np.exp(-0.5 * z * z)

def guess(x, y):
  return [y.max(), x[y.argmax()], 80, 100]

anormal.guess = guess