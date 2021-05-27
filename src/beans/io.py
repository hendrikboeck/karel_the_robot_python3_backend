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

# LOCAL IMPORT
from beans.types import EnumLike


class CLIFormat(EnumLike):
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


class CLIColors(EnumLike):
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
  NULL = ""

  def getFromStr(colorName: str) -> str:
    return CLIColors.__dict__.get(colorName, CLIColors.NULL)


class _IOTuple(NamedTuple):
  out: Any
  debug: Any
  error: Any


class IOManager():
  """
  The IOManager defines a interface for human-interaction.  And serializes this
  interface for easy access and manipulation and control over amount of 
  information which the user/developer can get.

  @param  _streams            _IOTuple of all streams
  @param  _labelColors        tuple of colors corresponding to 
  @param  show_caller_info    
  @param  show_label_out_msgs
  @param  show_debug_msgs
  """

  _streams: _IOTuple
  _labelColors: _IOTuple

  show_caller_info: bool
  show_label_out_msgs: bool
  show_debug_msgs: bool

  def __init__(self, conf: Dict[str, Any]) -> None:
    """
    constructor
   
    @param  conf  Dictionary, which describes a IOManager and enables the 
        specification over a global configuration-file, which specifies the 
        Flags.  The default Flags can be viewed by calling the Function 
        'createIOManagerDefaultConfig'.
    """
    self._streams = None
    self._labelColors = None
    self.show_caller_info = None
    self.show_label_out_msgs = None
    self.show_debug_msgs = None

    self.load(conf)

  def load(self, conf: Dict[str, Any]) -> None:
    """
    TODO: load-descrition
        
    @param  conf  Dictionary, which describes a IOManager and enables the 
        specification over a global configuration-file, which specifies the 
        Flags.  The default Flags can be viewed by calling the Function 
        'createIOManagerDefaultConfig'.
    """
    self._streams = _IOTuple(
        out=conf["OUT_STREAM"],
        debug=conf["DEBUG_STREAM"],
        error=conf["ERROR_STREAM"]
    )
    self._labelColors = _IOTuple(
        out=CLIColors.getFromStr(conf["OUT_LABEL_COLOR"]),
        debug=CLIColors.getFromStr(conf["DEBUG_LABEL_COLOR"]),
        error=CLIColors.getFromStr(conf["ERROR_LABEL_COLOR"])
    )

    self.show_caller_info = bool(conf["SHOW_CALLER_INFORMATION"])
    self.show_label_out_msgs = bool(conf["SHOW_LABEL_OUT_MESSAGES"])
    self.show_debug_msgs = bool(conf["SHOW_DEBUG_MESSAGES"])

  def _printCallerInformation(self, stream: TextIO) -> None:
    """
    Prints the caller-information. Farmated as 'function' or 'Class.function', 
    if memberfunction
   
    @param  stream  stream the information should be print to
    """
    # only print caller-information, if 'show_caller_info' flag is set
    if self.show_caller_info:
      caller = ""
      try:
        # adds the class of the function, if memberfunction ('Class.')
        caller += str(
            inspect.stack()[2].frame.f_locals['self'].__class__.__name__
        ) + "."
      except:
        pass
      # adds the function name ('function')
      caller += str(inspect.stack()[2].function)
      print(f"{caller} :: ", end="", file=stream)

  def _printLabel(
      self, streamLabel: str, labelColor: str, stream: TextIO
  ) -> None:
    """
    Prints the label onto the stream.
   
    @param  streamLabel   name of the stream as str
    @param  labelColor    color of the label as str (e.g. '\033[97m')
    @param  stream        stream the label should be print to
    """
    if labelColor != "":
      label = f"{CLIFormat.BOLD}{labelColor}{streamLabel} |{CLIFormat.ENDF} "
    else:
      label = f"{streamLabel} | "
    print(label, end="", file=stream)

  @staticmethod
  def input(text: str = "") -> str:
    """
    Gets an input from the commandline.
   
    @param  text  prompt for input
    @return       read string from the commandline
    """
    return input(text)

  @staticmethod
  def print(*values: object) -> None:
    """
    Wrapper for default print-function.  Should not be used, use 'out' instead.
   
    @param  values  objects to print onto default stream
    """
    print(*values, end="")

  def out(self, *values: object) -> None:
    if self.show_label_out_msgs:
      self._printLabel('OUT  ', self._labelColors.out, self._streams.out)
    print(*values, file=self._streams.out)

  def error(self, *values: object) -> None:
    self._printLabel('ERROR', self._labelColors.error, self._streams.error)
    self._printCallerInformation(self._streams.error)
    print(*values, file=self._streams.error)

  def debug(self, *values: object) -> None:
    if self.show_debug_msgs:
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