import numpy as np

from .gaisser_hillas import gaisser_hillas

def gaisser_hillas_six(x, nmax, xmax, x0, p0, p1 = 0, p2 = 0):
  l = np.maximum(1, p0 + x*(p1 + x*p2))
  return gaisser_hillas(x, nmax, xmax, x0, l)

def guess(x, y):
  return [y.max(), x[y.argmax()], -155, 93, -0.06, 0.00003]

gaisser_hillas_six.guess = guess
gaisser_hillas_six.npar = 6