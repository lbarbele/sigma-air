import numpy as np
import scipy.optimize as opt

def get_fit(f, x, y):
  # perform the fit
  popt, pcov, info, mesg, ierr = opt.curve_fit(f, x, y, p0 = f.guess(x, y), full_output = True)
  # compute parameter errors from the cov. matrix
  perr = np.sqrt(pcov.diagonal())
  # status flag
  status = 1 <= ierr and ierr <= 4
  # return parameters, errors, and status
  return popt, perr, status