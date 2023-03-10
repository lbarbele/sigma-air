#!/bin/python

import click
import inspect
import numpy as np
import pandas as pd
import pathlib
import sys
from tqdm import tqdm

src_path = str(pathlib.Path(__file__).absolute().parent.parent)
sys.path.append(src_path)
from src.data import conex_file_parser
from src.profile_functions import anormal, gaisser_hillas, gaisser_hillas_six, usp
from src.util import get_fit

def get_fcn(name: str):
  match name:
    case 'anormal':
      return anormal
    case 'gaisser-hillas':
      return gaisser_hillas
    case 'gaisser-hillas-six':
      return gaisser_hillas_six
    case 'usp':
      return usp
    case _:
      raise RuntimeError(f'Invalid required function with name "{name}"')

@click.command()
@click.option('-m', '--max-showers', type = click.IntRange(1, 4000000), required = True)
@click.option('-o', '--out-file', type = click.Path(), required = True)
@click.option('-f', '--function', type = click.Choice(['usp', 'gaisser-hillas', 'gaisser-hillas-six', 'anormal']), required = True)
@click.option('-p', '--poisson', is_flag = True, default = False)
@click.option('-t', '--threshold', type = click.FloatRange(1e-5), default = 0.3)
@click.argument('input_files', nargs = -1, type = click.Path(exists = True))
def main(input_files, out_file, max_showers, function, poisson, threshold) -> int:

  # get the fit function and read its properties
  fcn = get_fcn(function)

  par_names = inspect.getfullargspec(fcn).args[1:]
  err_names = [f'err_{s}' for s in par_names]
  col_names = par_names + err_names + ['status', 'chi2', 'ndf']
  npar = fcn.npar

  # the parser will allow to iterate over the input conex files
  parser = conex_file_parser(input_files, ['Xdep', 'dEdX'], max_showers)

  # a structure to hold fit data
  data = np.zeros((max_showers, len(col_names)))

  # loop over showers in the input files
  for i, (x, y) in tqdm(enumerate(parser), total = max_showers):
    # poissonian ansatz: sigma_i \propto sqrt(y_i)
    if poisson:
      # compute sigmas
      s = 1e-2 * np.sqrt(y * np.sum(y))
      # compute a mask to cut points below threshold
      msk = s/y <= threshold
      # apply the threshold cuts
      x = x[msk]
      y = y[msk]
      s = s[msk]
    # usual least squares: sigma_i = 1
    else:
      s = None
    # perform the fit
    par, err, sts, chi2 = get_fit(fcn, x, y, s)
    # fill the data table
    data[i, 0:npar] = par       # parameters
    data[i, npar:2*npar] = err  # errors
    data[i, -3] = int(sts)      # fit status
    data[i, -2] = chi2          # chi square
    data[i, -1] = len(x) - npar # n.d.f.

  # write data (as a DataFrame) into a csv file
  pd.DataFrame(data, columns = col_names, index = pd.Index(range(max_showers), name = 'index')).to_csv(out_file)

  return 0

if __name__ == '__main__':
  main()