from typing import NoReturn
import sys

from .io import IOM

EXIT_SUCCESS = 0
EXIT_FAILURE = 1


def Exit(e_code: int = EXIT_SUCCESS) -> NoReturn:
  sys.exit(e_code)


def ErrorExit(text: str = None, e_code: int = EXIT_FAILURE) -> NoReturn:
  if text is not None: IOM.error(text)
  Exit(e_code)
