import glob

def get_file_list(
  globs: str | list[str] | tuple[str]
) -> list[str]:
  if isinstance(globs, str):
    fs = glob.glob(globs)
    if len(fs) == 0:
      raise RuntimeError(f'bad path "{globs}"')
    return fs
  elif isinstance(globs, list) or isinstance(globs, tuple):
    return [f for g in globs for f in get_file_list(g)]
  else:
    raise RuntimeError(f'get_file_list: bad input "{globs}"')