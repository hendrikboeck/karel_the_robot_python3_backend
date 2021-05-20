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
from sys import stdout, stderr
from typing import Any, Dict, NamedTuple, TextIO
import inspect


class CLIFormat(object):
  ENDF = "\033[0m"
  BOLD = "\033[1m"
  RST_BOLD = "\033[21m"
  DIM = "\033[2m"
  RST_DIM = "\033[22m"
  ULINE = "\033[4m"
  RST_ULINE = "\033[24m"
  BLINK = "\033[5m"
  RST_BLINK = "\033[25m"
  REVSD = "\033[7m"
  RST_REVSD = "\033[27m"
  HIDDN = "\033[8m"
  RST_HIDDN = "\033[28m"


class CLIColors(object):
  DEFAULT = "\033[39m"
  BLACK = "\033[30m"
  RED = "\033[31m"
  GREEN = "\033[32m"
  YELLOW = "\033[33m"
  BLUE = "\033[34m"
  MAGENTA = "\033[35m"
  CYAN = "\033[36m"
  LGRAY = "\033[37m"
  DGRAY = "\033[90m"
  LRED = "\033[91m"
  LGREEN = "\033[92m"
  LYELLOW = "\033[93m"
  LBLUE = "\033[94m"
  LMAGENTA = "\033[95m"
  LCYAN = "\033[96m"
  WHITE = "\033[97m"


class _IOTuple(NamedTuple):
  out: Any
  debug: Any
  error: Any


##
# The IOManager defines a interface for human-interaction.  And serializes this interface for
# easy access and manipulation and control over amount of information which the user/developer
# can get.
#
class IOManager():

  _streams: _IOTuple
  _labelColors: _IOTuple

  SHOW_CALLER_INFORMATION: bool
  SHOW_LABEL_OUT_MESSAGES: bool
  SHOW_DEBUG_MESSAGES: bool

  ##
  # constructor
  #
  # @param  conf  Dictionary, which describes a IOManager and enables the specification over a
  #               global configuration-file, which specifies the Flags.  The default Flags can
  #               be viewed by calling the Function 'createIOManagerDefaultConfig'.
  #
  def __init__(self, conf: Dict[str, Any]) -> None:
    self._streams = None
    self._labelColors = None
    self.SHOW_CALLER_INFORMATION = None
    self.SHOW_LABEL_OUT_MESSAGES = None
    self.SHOW_DEBUG_MESSAGES = None

    self._load(conf)

  ##
  # TODO: _load-descrition
  #
  # @param  conf  Dictionary, which describes a IOManager and enables the specification over a
  #               global configuration-file, which specifies the Flags.  The default Flags can
  #               be viewed by calling the Function 'createIOManagerDefaultConfig'.
  #
  def _load(self, conf: Dict[str, Any]) -> None:
    self._streams = _IOTuple(
        out=conf["OUT_STREAM"], debug=conf["DEBUG_STREAM"], error=conf["ERROR_STREAM"]
    )
    self._labelColors = _IOTuple(
        out=conf["OUT_LABEL_COLOR"],
        debug=conf["DEBUG_LABEL_COLOR"],
        error=conf["ERROR_LABEL_COLOR"]
    )

    self.SHOW_CALLER_INFORMATION = bool(conf["SHOW_CALLER_INFORMATION"])
    self.SHOW_LABEL_OUT_MESSAGES = bool(conf["SHOW_LABEL_OUT_MESSAGES"])
    self.SHOW_DEBUG_MESSAGES = bool(conf["SHOW_DEBUG_MESSAGES"])

  ##
  # Prints the caller-information. Farmated as 'function' or 'Class.function', if
  # memberfunction
  #
  # @param  stream  stream the information should be print to
  #
  def _printCallerInformation(self, stream: TextIO) -> None:
    # only print caller-information, if 'SHOW_CALLER_INFORMATION' flag is set
    if self.SHOW_CALLER_INFORMATION:
      caller = ""
      try:
        # adds the class of the function, if memberfunction ('Class.')
        caller += str(inspect.stack()[2].frame.f_locals['self'].__class__.__name__) + "."
      except:
        pass
      # adds the function name ('function')
      caller += str(inspect.stack()[2].function)
      print(f"{caller} :: ", end="", file=stream)

  ##
  # Prints the label onto the stream.
  #
  # @param  streamLabel   name of the stream as str
  # @param  labelColor    color of the label as str (e.g. '\033[97m')
  # @param  stream        stream the label should be print to
  #
  def _printLabel(self, streamLabel: str, labelColor: str, stream: TextIO) -> None:
    if labelColor != "":
      label = f"{CLIFormat.BOLD}{labelColor}{streamLabel} |{CLIFormat.ENDF} "
    else:
      label = f"{streamLabel} | "
    print(label, end="", file=stream)

  ##
  # Gets an input from the commandline.
  #
  # @param  text  prompt for input
  # @return       read string from the commandline
  #
  @staticmethod
  def input(text: str = "") -> str:
    return input(text)

  ##
  # Wrapper for default print-function.  Should not be used, use 'out' instead.
  #
  # @param  values  objects to print onto default stream
  #
  @staticmethod
  def print(*values: object) -> None:
    print(*values, end="")

  def out(self, *values: object) -> None:
    if self.SHOW_LABEL_OUT_MESSAGES:
      self._printLabel('OUT  ', self._labelColors.out, self._streams.out)
    print(*values, file=self._streams.out)

  def error(self, *values: object) -> None:
    self._printLabel('ERROR', self._labelColors.error, self._streams.error)
    self._printCallerInformation(self._streams.error)
    print(*values, file=self._streams.error)

  def debug(self, *values: object) -> None:
    if self.SHOW_DEBUG_MESSAGES:
      self._printLabel('DEBUG', self._labelColors.debug, self._streams.error)
      self._printCallerInformation(self._streams.debug)
      print(*values, file=self._streams.debug)


def createIOManagerDefaultConfig() -> Dict[str, Any]:
  return dict(
      OUT_STREAM=stdout,
      DEBUG_STREAM=stderr,
      ERROR_STREAM=stderr,
      DEBUG_LABEL_COLOR="",
      ERROR_LABEL_COLOR="",
      OUT_LABEL_COLOR="",
      SHOW_DEBUG_MESSAGES=False,
      SHOW_LABEL_OUT_MESSAGES=False,
      SHOW_CALLER_INFORMATION=False
  )


def createIOManagerConfigFromDict(conf: Dict[str, Any]) -> Dict[str, Any]:
  result = createIOManagerDefaultConfig()
  for (key, value) in conf.items():
    uKey = key.upper()
    if uKey in result.keys():
      result[uKey] = value
    else:
      raise Exception(f"unkown key {key} as {uKey}")
  return result


IOM = IOManager(createIOManagerDefaultConfig())