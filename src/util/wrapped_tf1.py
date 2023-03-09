import numpy as np

from inspect import signature
from ROOT import TF1

class WrappedTF1(TF1):
  def __init__(self, fcn, xmin, xmax, npar = -1):
    self.npar = len(signature(fcn).parameters) - 1 if npar == -1 else npar
    self.fcn = fcn
    self.wrapped_fcn = lambda x, p: fcn(x[0], *[p[i] for i in range(self.npar)])
    super().__init__('', self.wrapped_fcn, xmin, xmax, self.npar)

  def __call__(self, x):
    return self.fcn(x, *np.frombuffer(self.GetParameters(), np.float64, self.npar))
  
  def parameters(self):
    return np.frombuffer(self.GetParameters(), np.float64, self.npar)
  
  def errors(self):
    return np.frombuffer(self.GetParErrors(), np.float64, self.npar)