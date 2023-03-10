import numpy as np
from ROOT import TChain

from ..util import get_file_list

scalar_branch_names = ['lgE', 'zenith', 'azimuth', 'Seed2', 'Seed3', 'Xfirst', 'Hfirst', 'XfirstIn', 'altitude', 'X0', 'Xmax', 'Nmax', 'p1', 'p2', 'p3', 'chi2', 'Xmx', 'Nmx', 'XmxdEdX', 'dEdXmx', 'cpuTime', 'nX']
array_branch_names = ['X', 'N', 'H', 'D', 'Mu', 'Gamma', 'Electrons', 'Hadrons', 'dMu', 'EGround']
spec_branch_names = ['Xdep', 'dEdX']

def get_conex_tree(
  files: str | list[str]
) :
  shower_tree = TChain('Shower', 'Shower')
  file_list = get_file_list(files)
  for file in file_list:
    shower_tree.Add(file)
  return shower_tree

def get_branch_data(
  shower,
  branch_name: str,
) :
  # scalar branches
  if branch_name in scalar_branch_names:
    return getattr(shower, branch_name)
  
  # array branches
  elif branch_name in array_branch_names:
    return np.array(getattr(shower, branch_name), dtype = np.float32)
  
  # special-case branches
  elif branch_name in spec_branch_names:
    # depths of the energy deposit profile
    if branch_name == 'Xdep':
      x = np.array(getattr(shower, 'X'), dtype = np.float32)
      return 0.5*(x[:-1] + x[1:])
    # energy deposit values
    elif branch_name == 'dEdX':
      y = np.array(getattr(shower, 'dEdX'), dtype = np.float32)
      return y[:-1]
    # if the branch is not implemented yet
    else:
      raise RuntimeError(f'get_branch_data: unimplemented special branch "{branch_name}"')
  
  # anything else is invalid
  else:
    raise RuntimeError(f'get_branch_data: bad branch "{branch_name}"')
  
def conex_file_parser(
  files: str | list[str],
  branches: str | list[str] = [],
  max_showers: int = 0,
  transform: dict = {},
) :
  shower_tree = get_conex_tree(files)

  for ishower, shower in enumerate(shower_tree):
    if max_showers > 0 and ishower >= max_showers: break
    yield [get_branch_data(shower, s) for s in branches] + [tr(shower) for tr in transform.values()]