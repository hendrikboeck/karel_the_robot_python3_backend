################################################################################
# karel_the_robot_python3_backend                                              #
# Copyright (C) 2021  Hendrik Boeck <hendrikboeck.dev@protonmail.com>          #
#                                                                              #
# This program is free software: you can redistribute it and/or modify         #
# it under the terms of the GNU General Public License as published by         #
# the Free Software Foundation, either version 3 of the License, or            #
# (at your option) any later version.                                          #
#                                                                              #
# This program is distributed in the hope that it will be useful,              #
# but WITHOUT ANY WARRANTY; without even the implied warranty of               #
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the                #
# GNU General Public License for more details.                                 #
#                                                                              #
# You should have received a copy of the GNU General Public License            #
# along with this program.  If not, see <http://www.gnu.org/licenses/>.        #
################################################################################

# STL IMPORT
from typing import NoReturn
import sys
import os

# LOCAL IMPORT
from .io import IOM

EXIT_SUCCESS = 0
EXIT_FAILURE = 1


def exitc(e_code: int = EXIT_SUCCESS) -> NoReturn:
  """
  """
  sys.exit(e_code)


def errorExit(text: str = None, e_code: int = EXIT_FAILURE) -> NoReturn:
  """
  """
  if text is not None: IOM.error(text)
  exitc(e_code)


def fileExists(path: str) -> bool:
  """
  """
  return os.path.exists(path)
