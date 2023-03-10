import numpy as np
import scipy.optimize as opt

def get_fit(f, x, y, s = None):
  try:
    # perform the fit
    popt, pcov, info, mesg, ierr = opt.curve_fit(f, x, y, p0 = f.guess(x, y), full_output = True, sigma = s)
    # compute parameter errors from the cov. matrix
    perr = np.sqrt(pcov.diagonal())
    # status flag
    status = 1 <= ierr and ierr <= 4
    # compute chi2
    chi2 = ((y - f(x, *popt))**2).sum() if s is None else (((y - f(x, *popt))/s)**2).sum()
    # return parameters, errors, and status
    return popt, perr, status, chi2
  except RuntimeError:
    # in case of error, return some spurious values
    return np.zeros(f.npar), np.zeros(f.npar), False, -1