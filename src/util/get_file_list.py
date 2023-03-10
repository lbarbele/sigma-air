import glob

def get_file_list(
  globs: str | list[str] | tuple[str],
  sort: bool = True,
) -> list[str]:
  if isinstance(globs, str):
    fs = glob.glob(globs)
    if len(fs) == 0:
      raise RuntimeError(f'bad path "{globs}"')
    if sort:
      fs.sort()
    return fs
  elif isinstance(globs, list) or isinstance(globs, tuple):
    fs = [f for g in globs for f in get_file_list(g, sort = False)]
    if sort:
      fs.sort()
    return fs
  else:
    raise RuntimeError(f'get_file_list: bad input "{globs}"')