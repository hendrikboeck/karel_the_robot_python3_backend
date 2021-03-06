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

# LIBRARY IMPORT
from pygame import Color

# LOCAL IMPORT
from pyadditions.types import EnumLike

HexColor = Color


class Basics(EnumLike):
  """Enum of basic colors"""

  WHITE = HexColor("#ffffff")
  BLACK = HexColor("#000000")
  RED = HexColor("#ff0000")
  GREEN = HexColor("#00ff00")
  BLUE = HexColor("#0000ff")
