import numpy as np

def gaisser_hillas(x, nmax, xmax, x0, l):
  xx = np.maximum((x - x0) / l, 1e-5)
  yy = np.maximum((xmax - x0) / l, 1e-5)
  return nmax * np.exp(-xx + yy*(1 + np.log(xx/yy)))

def guess(x, y):
  return [y.max(), x[y.argmax()], -100, 80]

gaisser_hillas.guess = guess
gaisser_hillas.npar = 4