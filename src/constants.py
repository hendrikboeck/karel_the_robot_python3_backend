from pygame import USEREVENT
from pygame.event import Event

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
WINDOW_TITLE = "karel the robot x64 - tcp://localhost:1234"

# PYGAME_GUI FONT SETTINGS
GAME_FONT = "font/FiraCode-Regular.ttf"

# SCREEN PROPERTIES
WINDOW_TITLE = "Karel the robot - Server (x64)"
FRAME_RATE = 144
SCREEN_BACKGROUND_COLOR = HexColor("#dddddd")

# CONFIG
DEFAULTPATH_CONFIG = "assets/pbe.yaml"

# THEMES, ASSETS
NO_SHADOW_THEME = "theme/no_shadow.json"
