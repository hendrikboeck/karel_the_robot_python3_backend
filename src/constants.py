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
from pygame import USEREVENT
from pygame.event import Event

# LOCAL IMPORT
from beans.types import Vector2f
from assets.color import HexColor

# Math
INFINITY = float("inf")

# Server/Networking constants
TCP_MAX_PKG_SIZE = 65535
UDP_MAX_PKG_SIZE = 65535
MAX_CONNECTIONS = 1
UTF8 = "utf-8"

# Events
PYGAME_USEREVENT = USEREVENT + 1
GAME_START_EVENT = Event(PYGAME_USEREVENT, attr1="game_start_event")
GAME_CONTINUE_EVENT = Event(PYGAME_USEREVENT, attr1="game_continue_event")
GAME_ERROR_EVENT = Event(PYGAME_USEREVENT, attr1="game_error_event")
GAME_FINISHED_EVENT = Event(PYGAME_USEREVENT, attr1="game_finished_event")

# WINDOW GEOMETRY AND ANCHORS
WINDOW_DIMENSIONS = Vector2f(1200, 850)
WINDOW_CENTER = WINDOW_DIMENSIONS / 2
WINDOW_CENTER_LEFT = Vector2f(0, WINDOW_DIMENSIONS.y / 2)
WINDOW_CENTER_RIGHT = Vector2f(WINDOW_DIMENSIONS.x, WINDOW_DIMENSIONS.y / 2)
WINDOW_TOP_LEFT = Vector2f(0, 0)
WINDOW_TOP_RIGHT = Vector2f(WINDOW_DIMENSIONS.x, 0)
WINDOW_BOTTOM_LEFT = Vector2f(0, WINDOW_DIMENSIONS.y)
WINDOW_BOTTOM_RIGHT = WINDOW_DIMENSIONS

# PYGAME_GUI FONT SETTINGS
GAME_FONT = "font/FiraCode-Regular.ttf"

# SCREEN PROPERTIES
WINDOW_TITLE = "Karel the robot - Server (x64)"
MAXFPS = 144
SCREEN_BACKGROUND_COLOR = HexColor("#dddddd")

# CONFIG
ASSETS_FOLDER = "assets"
CONFIGPATH = "assets/pbe."
