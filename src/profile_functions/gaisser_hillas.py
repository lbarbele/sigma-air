import numpy as np

def gaisser_hillas(x, nmax, xmax, x0, p0, p1 = 0, p2 = 0):
  l = p0 + x*(p1 + x*p2)
  xx = np.maximum((x - x0) / l, 1e-5)
  yy = np.maximum((xmax - x0) / l, 1e-5)
  return nmax * np.power(xx/yy, yy) * np.exp(yy - xx)