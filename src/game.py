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
from __future__ import annotations
from typing import Dict, Any, List, Tuple, Union, NamedTuple
from time import sleep
import ast

# LIBRARY IMPORT
from pygame import Surface, Rect, SRCALPHA
import pygame as pg

# LOCAL IMPORT
from pyadditions.io import IOM
from pyadditions.types import EnumLike, SingletonMeta, Vector2f, promiseList
import assets
from assets.color import HexColor
from constants import GAME_CONTINUE_EVENT, GAME_ERROR_EVENT, GAME_FONT, GAME_START_EVENT, INFINITY
from view.window import DebugInformationDict


def createMapConfigFromXML(xml_: Dict[str, Any]) -> Dict[str, Any]:
  """
  Takes a dictonary read from a world.xml file and creates a dictonary, which
  will be used to configure Karel, World, Tiles, Level

  @param  xml_  dictonary read from a world.xml file
  @return       configuration for World, Karel, Tiles, Level as dict
  """
  conf = {}

  conf["world"] = {}

  conf["world"]["size"] = Vector2f(*ast.literal_eval(xml_["size"]))
  metadata = xml_.get("metadata", {})
  conf["world"]["metadata"] = dict(
      name=metadata.get("name", "unkown"),
      version=metadata.get("version", "unkown"),
      author=metadata.get("author", "unkown"),
      speed=xml_.get("speed", "1.0")
  )

  walls = promiseList(xml_.get("wall", []))
  for wall in walls:
    wall["start"] = Vector2f(*ast.literal_eval(wall["start"]))
    wall["length"] = abs(int(wall.get("length", "1")))
    wall["orientation"] = KarelOrientation.fromString(wall["orientation"])
  conf["world"]["walls"] = walls

  beepers = promiseList(xml_.get("beeper", []))
  for beeper in beepers:
    beeper["position"] = Vector2f(*ast.literal_eval(beeper["position"]))
    beeper["n"] = abs(int(float(beeper.get("n", "1"))))
  conf["world"]["beepers"] = beepers

  karel = xml_.get("karel", {})
  conf["karel"] = {}
  conf["karel"]["position"] = Vector2f(
      *ast.literal_eval(karel.get("position", "(1, 1)"))
  )
  conf["karel"]["orientation"] = KarelOrientation.fromString(
      karel.get("orientation", "EAST")
  )
  conf["karel"]["beeperbag"] = float(karel.get("beeperbag", "inf"))

  conf["speed"] = abs(float(xml_.get("speed", "1.0")))

  return conf


class ActionExecutionError(RuntimeError):
  """
  This error is produced, when an error occured on the execution of a command
  (e.g. 'Karel hit a wall'). This error will be passed through to frontend.

  @extends  RuntimeError
  """

  def __init__(self, *args: object) -> None:
    pg.event.post(GAME_ERROR_EVENT)
    IOM.debug(f"POSTED '{GAME_ERROR_EVENT.attr1}'")
    super().__init__(*args)


class MapLoadingError(RuntimeError):
  """
  This error is produced, when an error of any type (e.g. MapFile not found) was
  caught while loading the map. This error will be passed through to frontend.

  @extends  RuntimeError
  """

  def __init__(self, e: Exception, *args: object) -> None:
    IOM.error(f"MapLoadingError: (ex) {e}")
    super().__init__(*args)


class UnallowedActionError(RuntimeError):
  """
  This error is produced, when the Game is in a non-playable state, but a action
  is called on it. This error will be passed through to frontend.

  @extends  RuntimeError
  """

  def __init__(self, actionDescr: str, *args: object) -> None:
    IOM.error(f"caputured unallowed action: {actionDescr}")
    super().__init__(*args)


class _KarelOrientationTuple(NamedTuple):
  """
  This class specifies a Set of values, which specify a compass-direction in the
  Game. It is used to specify the orientation Karel is looking at and how Walls 
  are placed. (The different compass-directions are specified in the EnumLike 
  KarelOrientation-class)

  @extends  NamedTuple
  @param    name    the compass-direction name
  @param    angle   the angle in deg of compass-direction with EAST beeing 0
  @param    vector  the movement-vector Karel will use on 'move()'
  """

  name: str
  angle: float
  vector: Vector2f

  def __str__(self) -> str:
    """
    Stringifies the Object

    @return   str(self)
    """
    return f"KarelOrientationSet(name='{self.name}', angle={self.angle}, vector={self.vector})"

  def isHorizontal(self) -> bool:
    """
    Checks if a compass-direction of a _KarelOrientationTuple is horizontally 
    aligned

    @return   True if 'EAST' or 'WEST'
    """
    return self.name == "EAST" or self.name == "WEST"

  def isVertical(self) -> bool:
    """
    Checks if a compass-direction of a _KarelOrientationTuple is vertically 
    aligned

    @return   True if 'SOUTH' or 'NORTH'
    """
    return not self.isHorizontal()


class KarelOrientation(EnumLike):
  """Enum of all the compass-directions as _KarelOrientationTuple"""

  NORTH = _KarelOrientationTuple("NORTH", 90.0, Vector2f(0, 1))
  EAST = _KarelOrientationTuple("EAST", 0.0, Vector2f(1, 0))
  SOUTH = _KarelOrientationTuple("SOUTH", 270.0, Vector2f(0, -1))
  WEST = _KarelOrientationTuple("WEST", 180.0, Vector2f(-1, 0))

  def fromString(key: str) -> _KarelOrientationTuple:
    """
    Returns the coresponding _KarelOrientationTuple for a given compass-
    direction out of the Enum

    @return   coresponding _KarelOrientationTuple
    """
    return KarelOrientation.__dict__[key]

  def fromAngle(angle: float) -> _KarelOrientationTuple:
    """
    Returns the coresponding _KarelOrientationTuple for a given Karel-rotation-
    angle out of the Enum

    @return   coresponding _KarelOrientationTuple
    """
    if angle == KarelOrientation.NORTH.angle: return KarelOrientation.NORTH
    elif angle == KarelOrientation.EAST.angle: return KarelOrientation.EAST
    elif angle == KarelOrientation.SOUTH.angle: return KarelOrientation.SOUTH
    elif angle == KarelOrientation.WEST.angle: return KarelOrientation.WEST


class Tile():
  """
  This class represents a Tile of the Karel-World. A Tile can have up to 1 walls
  in eighter compass-direction and has n Beepers on it, which can be picked up 
  by Karel. A Tile has no information about its position in the Map.

  @param  surf      render-surface as pygame.Surface
  @param  rect      bounds of surf as pygame.Rect
  @param  _walls    List of wall-angles present on Tile
  @param  _beepers  number of Beepers present on Tile
  """

  surf: Surface
  rect: Rect
  _walls: List[float]
  _beepers: int

  def __init__(
      self, pos: Tuple[float, float], walls: List[float], beepers: int
  ) -> None:
    self.surf = assets.load.image("64x/tile.png")
    self.rect = self.surf.get_rect()
    self._walls = walls
    self._beepers = beepers

    (self.rect.x, self.rect.y) = pos
    self.rebuild()

  def rebuild(self) -> None:
    """Rebuilds the render-surface of Tile."""
    self.surf = assets.load.image("64x/tile.png")
    for angle in self._walls:
      self._buildWall(angle)
    self._buildBeepers()

  def _buildWall(self, angle: float) -> None:
    """
    Creates a Wall-surface and renders it in position onto the render-surface
    of Tile.

    @param  angle    angle of the wall, relative to 0 at EAST
    """
    wallSurf = Surface((self.rect.width, self.rect.height), SRCALPHA)
    pg.draw.rect(
        wallSurf, HexColor("#000000"),
        Rect(self.rect.width - 1, 0, 1, self.rect.height)
    )
    wallSurf = pg.transform.rotate(wallSurf, angle)
    self.surf.blit(wallSurf, (0, 0))

  def _buildBeepers(self) -> None:
    """
    Creates a Beeper-surface with a counter on top if more than one Beeper are
    present and then renders it onto the render-surface of Tile.
    """
    if self._beepers > 0:
      beeperSurf = assets.load.image("64x/beeper.png")
      self.surf.blit(beeperSurf, (0, 0))
    if self._beepers > 1:
      beeperNumFont = assets.load.font(GAME_FONT, 14)
      beeperNumSurf = beeperNumFont.render(
          str(self._beepers), True, HexColor("#000000")
      )
      beeperNumRect = beeperNumSurf.get_rect()
      beeperNumRect.center = (self.rect.width / 2, self.rect.height / 2)
      self.surf.blit(beeperNumSurf, beeperNumRect)

  def addWall(self, angle: float) -> None:
    """
    Adds a Wall to the Tile and rerenders the Tile.

    @param  angle   angle of the wall, relative to 0 at EAST
    """
    if angle not in self._walls:
      self._walls.append(angle)
      self.rebuild()

  def setBeepers(self, n: int) -> None:
    """
    Sets the number of Beepers and rerenders the Tile.

    @param  n   number of Beepers
    """
    if self._beepers != n:
      self._beepers = n
      self.rebuild()

  def getBeepers(self) -> int:
    """
    Returns the number of Beepers present on Tile.

    @return   number of Beepers
    """
    return self._beepers

  def incrBeepers(self) -> None:
    """
    Increments the number of Beepers on Tile by one and rerenders the Tile.
    """
    self.setBeepers(self._beepers + 1)

  def decrBeepers(self) -> None:
    """
    Decrements the number of Beepers on Tile by one and rerenders the Tile.
    """
    self.setBeepers(self._beepers - 1)

  def wallAt(self, angle: float) -> bool:
    """
    Checks if a wall is present on Tile at specified angle.

    @param  angle   angle of the wall, relative to 0 at EAST
    @return         True if Wall is at angle
    """
    return angle in self._walls


class Karel():
  """
  Represents Karel (Player). Karel can not execute actions own,because every
  action is bound to World/Level conditions.

  @param  surf          render-surface as pygame.Surface
  @param  rect          bounds of surf as pygame.Rect
  @param  beeperbag     num of beepers available to Karel
  @param  orientation   compass-direction, Karel is looking at
  @param  position      Coordinates of position of Karel (starts at (1, 1))
  """

  surf: Surface
  rect: Rect
  beeperbag: float
  orientation: _KarelOrientationTuple
  position: Vector2f

  def __init__(self, conf: Dict[str, Any]) -> None:
    self.surf = assets.load.image("64x/karel.png")
    self.rect = self.surf.get_rect()
    self.orientation = KarelOrientation.EAST
    self.beeperbag = conf["beeperbag"]
    self.position = conf["position"]

    self.setOrientation(conf["orientation"])

  def rebuild(self) -> None:
    """Rebuilds the render-surface of Karel."""
    self.surf = assets.load.image("64x/karel.png")
    oldOrientation = self.orientation
    self.orientation = KarelOrientation.EAST
    self.setOrientation(oldOrientation)

  def render(self, surf: Surface) -> None:
    """
    Renders render-surface on destination-surface.

    @param  surf  destination-surface
    """
    x = self.rect.x + (self.position - 1) * self.rect.width
    y = self.rect.y + (self.position - 1) * self.rect.height
    surf.blit(self.surf, (x, y))

  def setOrientation(self, orientation: _KarelOrientationTuple) -> None:
    """
    Sets the compass-direction Karel is looking at and rotates render-surface.

    @param  orientation   new compass-direction as _KarelOrientationTuple
    """
    if self.orientation != orientation:
      self.surf = pg.transform.rotate(
          self.surf, orientation.angle - self.orientation.angle
      )
      self.orientation = orientation

  def rotate90(self) -> None:
    """Rotates Karel by 90deg."""
    self.setOrientation(
        KarelOrientation.fromAngle((self.orientation.angle + 90) % 360)
    )

  def incrBeeperbag(self) -> None:
    if self.beeperbag != INFINITY:
      self.beeperbag += 1

  def decrBeeperbag(self) -> None:
    if self.beeperbag != INFINITY:
      self.beeperbag -= 1

  def beeperbagIsEmpty(self) -> None:
    if self.beeperbag == INFINITY:
      return False
    else:
      return self.beeperbag > 0.0


class World():
  """
  Represents the World Karel is playing on. This class only represents the 
  dataclass and specifies the rendering of the World-object. This class has no
  information on any game-logic or karel.

  @param  tiles   a 2D-array of all tiles in the map KCS(1, 1) is INDEX(0, 0)
  @param  size    the size of the world in measured in Tiles
  @param  surf    render-surface as pygame.Surface
  @param  rect    bounds of surf as pygame.Rect   
  """

  tiles: List[List[Tile]]
  size: Vector2f
  surf: Surface
  rect: Rect

  def __init__(self, conf: Dict[str, Any]) -> None:
    metadata = conf["metadata"]
    DebugInformationDict().update(
        MAP_NAME=metadata["name"],
        MAP_SIZE=conf["size"],
        MAP_VERSION=metadata["version"],
        MAP_COMMAND_RATIO=metadata["speed"]
    )

    self.size = conf["size"]
    self.tiles = []
    for i in range(self.size.y):
      self.tiles.append([])
      for j in range(self.size.x):
        self.tiles[i].append(Tile((i, j), [], 0))

    for wall in conf["walls"]:
      wallPosition = wall["start"]
      wallOrientation = wall["orientation"]
      for i in range(wall["length"]):
        self.tiles[wallPosition.y - 1][wallPosition.x -
                                       1].addWall(wallOrientation.angle)
        if wallOrientation.isHorizontal():
          wallPosition.y += 1
        else:
          wallPosition.x += 1

    for beeper in conf["beepers"]:
      beeperPosition = beeper["position"]
      self.tiles[beeperPosition.y - 1][beeperPosition.x -
                                       1].setBeepers(beeper["n"])

    tileDimension = Vector2f._make(self.tiles[0][0].surf.get_size())
    self.surf = Surface(tuple(self.size * tileDimension))
    self.rect = self.surf.get_rect()
    for i, row in enumerate(reversed(self.tiles)):
      for j, tile in enumerate(row):
        tile.rect.x = j * tileDimension.x
        tile.rect.y = i * tileDimension.y

    self.rebuild()

  def rebuild(self) -> None:
    """Rebuilds the render-surface of World."""
    for row in self.tiles:
      for tile in row:
        self.surf.blit(tile.surf, tile.rect)

  def render(self, destSurf: Surface) -> None:
    """
    Renders render-surface on destination-surface.

    @param  destSurf  destination-surface
    """
    destSurf.blit(self.surf, self.rect)

  def getTileAtKCS(
      self, pos: Union[Tuple[float, float], List[float], Vector2f]
  ) -> Tile:
    """
    Returns the coresponding Tile for a cordinate in the KCS (Karel Cordinate
    System).

    @param  pos   cordinate in the KCS (Karel Cordinate System)
    @return       coresponding tile as Tile
    """
    return self.tiles[int(pos[1]) - 1][int(pos[0]) - 1]

  def isOutOfBoundsKCS(
      self, pos: Union[Tuple[float, float], List[float], Vector2f]
  ) -> bool:
    """
    Checks if a cordinate in KCS is out of bounds of the World.

    @param  pos   cordinate in the KCS (Karel Cordinate System)
    @return       True if out of bounds of the World
    """
    pos = Vector2f._make(pos)
    return pos < (1, 1) or pos > self.size

  def rebuildTileAtKCS(
      self, pos: Union[Tuple[float, float], List[float], Vector2f]
  ) -> None:
    """
    Rebuilds Tile at a scpecific cordinate in KCS.

    @param  pos   cordinate in the KCS (Karel Cordinate System)
    """
    tile = self.getTileAtKCS(pos)
    tile.rebuild()
    self.surf.blit(tile.surf, tile.rect)

  def repaintTileAtKCS(
      self, pos: Union[Tuple[float, float], List[float], Vector2f]
  ) -> None:
    tile = self.getTileAtKCS(pos)
    self.surf.blit(tile.surf, tile.rect)


class LevelState(EnumLike):
  """Enum which describes the different states for the level."""

  INIT = 1
  RUNNING = 2
  PAUSE = 3
  ERROR = 4
  FINISHED = 5

  @staticmethod
  def toStr(state: int) -> str:
    """
    Converts a LevelState to str.

    @param  state   state as LevelState
    @return         state as str
    """
    if state == LevelState.INIT:
      return "LS_INIT"
    elif state == LevelState.PAUSE:
      return "LS_PAUSE"
    elif state == LevelState.RUNNING:
      return "LS_RUNNING"
    elif state == LevelState.ERROR:
      return "LS_ERROR"
    elif state == LevelState.FINISHED:
      return "LS_FINISHED"


class Level():
  """
  The main datastructure that describes the game-world. It holds all information
  about the logic of the game. It also holds all game-objects and is responsible
  for rendering and scaling the World and Karel.

  @param  surf        render-surface as pygame.Surface
  @param  rect        bounds of surf as pygame.Rect   
  @param  state       state of the Level as LevelState
  @param  speed       current Karel-Actions per seconds
  @param  world       World-object
  @param  karel       Karel-object
  @param  scaledSurf  scaled surface, if world is to big for bounds, else None
  @param  scaledRatio ratio in which the world is scaled, default: 1.0
  @param  isScaled    True if world is in scaled mode
  """

  surf: Surface
  rect: Rect

  state: int
  speed: float
  world: World
  karel: Karel

  scaledSurf: Surface
  scaledRatio: float
  isScaled: bool

  def __init__(
      self, mapname: str, bounds: Union[Tuple[float, float], List[float],
                                        Vector2f]
  ) -> None:
    """
    constructor

    @param  mapname   name of map
    @param  bounds    bounds of surface
    """
    try:
      mapXml = assets.load.xml(f"map/{mapname}.xml")
      map_ = createMapConfigFromXML(mapXml)
    except Exception as e:
      raise MapLoadingError(e)

    self.world = World(map_["world"])
    self.karel = Karel(map_["karel"])
    self.speed = map_["speed"]
    self.surf = Surface((self.world.rect.width + 2, self.world.rect.height + 2))
    self.rect = self.surf.get_rect()
    self.state = LevelState.INIT

    # scaling
    self.isScaled = False
    self.scaledRatio = 1.0
    self.scaledSurf = None

    scaledRatio = min(bounds[0] / self.rect.width, bounds[1] / self.rect.height)
    if scaledRatio < 1.0:
      self.setScaledRect(scaledRatio)

    self.repaint()

  def playable(self) -> bool:
    """
    Checks, wether the level is currently playable or not.

    @return   True if level is playable
    """
    return (self.state == LevelState.RUNNING)

  def pause(self) -> None:
    self._changeLevelState(LevelState.PAUSE)
    pg.time.set_timer(GAME_CONTINUE_EVENT, int(1000 / self.speed), 1)

  def setScaledRect(self, scaledRatio: float) -> None:
    """
    Rescales the rect of Level using scaledRatio, initializes scaledSurf and
    sets the level in scaled mode.

    @param  scaledRatio   ratio the surf should be scaled to
    """
    self.isScaled = True
    self.scaledRatio = scaledRatio
    self.rect.width = self.rect.width * self.scaledRatio
    self.rect.height = self.rect.height * self.scaledRatio

    self.scaledSurf = Surface((self.rect.width, self.rect.height))

  def repaint(self) -> None:
    """Repaint the game surface (scaled surface to if in scaled mode)."""
    self.surf.fill(HexColor("#000000"))
    self.surf.blit(self.world.surf, (1, 1))

    karelAbsolutePosition = self.world.getTileAtKCS(self.karel.position).rect
    self.surf.blit(
        self.karel.surf,
        (karelAbsolutePosition.x + 1, karelAbsolutePosition.y + 1)
    )

    # render scaled-version onto scaledSurf, if in scaled mode
    if self.isScaled:
      self.scaledSurf.blit(
          pg.transform.smoothscale(
              self.surf, (self.rect.width, self.rect.height)
          ), (0, 0)
      )

  def update(self, speed: float) -> None:
    """Update level and information about level"""
    self.speed = speed
    DebugInformationDict().update(
        KAREL_POSITION=self.karel.position,
        KAREL_ORIENTATION=
        f"{self.karel.orientation.name} / {self.karel.orientation.angle}",
        KAREL_BEEPER_BAG=self.karel.beeperbag,
        MAP_RENDER_SCALE=self.scaledRatio
    )

  def render(self, destSurf: Surface) -> None:
    """
    Renders render-surface on destination-surface.

    @param  destSurf  destination-surface
    """
    if self.isScaled:
      destSurf.blit(self.scaledSurf, self.rect)
    else:
      destSurf.blit(self.surf, self.rect)

  def proccessEvent(self, event: pg.event.Event) -> None:
    """
    Processes a pygame event.

    @param  event   pygame event
    """
    if event == GAME_ERROR_EVENT:
      self._changeLevelState(LevelState.ERROR)
    if event == GAME_START_EVENT:
      self._changeLevelState(LevelState.RUNNING)
    if event == GAME_CONTINUE_EVENT:
      self._changeLevelState(LevelState.RUNNING)

  def _changeLevelState(self, state: int) -> None:
    """
    Changes the current level state.

    @param  state   new level state
    """
    IOM.debug(
        f"levelstate changed from '{LevelState.toStr(self.state)}' to '{LevelState.toStr(state)}'"
    )
    self.state = state

  def startLevel(self) -> None:
    """
    Starts the level and makes it playable. It will only start the level, if
    it was in the init state before.
    """
    if self.state == LevelState.INIT:
      self.state = LevelState.RUNNING
    else:
      IOM.error(
          f"can not start level: wrong state '{LevelState.toStr(self.state)}'"
      )

  def waitOnRunning(self) -> None:
    """Stops the thread, till the level has been started."""
    if self.state == LevelState.INIT or self.state == LevelState.PAUSE:
      # IOM.out(f"WAIT FOR '{GAME_START_EVENT.attr1}' or '{GAME_CONTINUE_EVENT.attr1}'")
      while self.state == LevelState.INIT or self.state == LevelState.PAUSE:
        sleep(0.07)

  def karelMove(self) -> None:
    """
    is a Karel-Action. Makes Karel move 1 tile forward in the direction he is
    looking at. If Karel can not execute move a Error is raised.
    """
    if self.playable():
      if self.karelFrontIsClear():
        self.world.rebuildTileAtKCS(self.karel.position)
        self.karel.position += self.karel.orientation.vector
        self.repaint()
      else:
        raise ActionExecutionError()
    else:
      raise UnallowedActionError("karelMove")

  def karelTurnLeft(self) -> None:
    """
    is a Karel-Action. Makes Karel turn left. If Karel can not execute turnLeft
    a Error is raised.
    """
    if self.playable():
      self.world.rebuildTileAtKCS(self.karel.position)
      self.karel.rotate90()
      self.repaint()
    else:
      raise UnallowedActionError("karelTurnLeft")

  def karelPickBeeper(self) -> None:
    """
    is a Karel-Action. Makes Karel pick a beeper from current position. If Karel
    can not execute pickBeeper a Error is raised.
    """
    if self.playable():
      if self.karelBeeperPresent():
        self.world.getTileAtKCS(self.karel.position).decrBeepers()
        self.karel.incrBeeperbag()
        self.world.repaintTileAtKCS(self.karel.position)
        self.repaint()
      else:
        raise ActionExecutionError()
    else:
      raise UnallowedActionError("karelPickBeeper")

  def karelPutBeeper(self) -> None:
    """
    is a Karel-Action. Makes Karel put a beeper at current position. If Karel 
    can not execute putBeeper a Error is raised.
    """
    if self.playable():
      if self.karelBeeperInBag():
        self.world.getTileAtKCS(self.karel.position).incrBeepers()
        self.karel.decrBeeperbag()
        self.world.repaintTileAtKCS(self.karel.position)
        self.repaint()
      else:
        raise ActionExecutionError()
    else:
      raise UnallowedActionError("karelPutBeeper")

  def _karelIsOrientationBlocked(
      self, orientation: _KarelOrientationTuple
  ) -> bool:
    """
    Returns wether a wall exists in a given orientation of Karel.

    @param  orientation   orientation that should be checked
    @return               True if wall exists at orientation of Karel
    """
    nextTileKCSPoint = self.karel.position + orientation.vector

    outOfBounds = self.world.isOutOfBoundsKCS(nextTileKCSPoint)
    return outOfBounds or self.world.getTileAtKCS(self.karel.position).wallAt(
        orientation.angle
    ) or self.world.getTileAtKCS(nextTileKCSPoint).wallAt(
        (orientation.angle + 180) % 360
    )

  def karelFrontIsClear(self) -> bool:
    """
    is a Karel-Question. Returns wether there is a wall in front of Karel.

    @return   True if there is no wall in front of Karel
    """
    if self.playable():
      return not self._karelIsOrientationBlocked(self.karel.orientation)
    else:
      raise UnallowedActionError("karelFrontIsClear")

  def karelLeftIsClear(self) -> bool:
    """
    is a Karel-Question. Returns wether there is a wall to the left of Karel.

    @return   True if there is no wall to the left of Karel
    """
    if self.playable():
      return not self._karelIsOrientationBlocked(
          KarelOrientation.fromAngle((self.karel.orientation.angle + 90) % 360)
      )
    else:
      raise UnallowedActionError("karelLeftIsClear")

  def karelRightIsClear(self) -> bool:
    """
    is a Karel-Question. Returns wether there is a wall to the right of Karel.

    @return   True if there is no wall to the right of Karel
    """
    if self.playable():
      return not self._karelIsOrientationBlocked(
          KarelOrientation.fromAngle(
              (self.karel.orientation.angle + 270) % 360
          )
      )
    else:
      return UnallowedActionError("karelLeftIsClear")

  def karelBeeperInBag(self) -> bool:
    """
    is a Karel-Question. Returns wether Karel has at least one beeper left in
    his bag.

    @return   True if Karel has at least one beeper in bag
    """
    if self.playable():
      return not self.karel.beeperbagIsEmpty()
    else:
      raise UnallowedActionError("karelBeeperInBag")

  def karelBeeperPresent(self) -> bool:
    """
    is a Karel-Question. Returns wether at least one beeper is present on the
    position Karel is at.

    @return   True if at least one beeper is present on Karel's current position
    """
    if self.playable():
      return self.world.getTileAtKCS(self.karel.position).getBeepers() > 0.0
    else:
      raise UnallowedActionError("karelBeeperPresent")

  def karelFacingNorth(self) -> bool:
    """
    is a Karel-Question. Returns wether Karel is currently facing north.

    @return   True if Karel is facing north
    """
    if self.playable():
      return self.karel.orientation == KarelOrientation.NORTH
    else:
      raise UnallowedActionError("karelFacingNorth")

  def karelFacingEast(self) -> bool:
    """
    is a Karel-Question. Returns wether Karel is currently facing east.

    @return   True if Karel is facing east
    """
    if self.playable():
      return self.karel.orientation == KarelOrientation.EAST
    else:
      raise UnallowedActionError("karelFacingEast")

  def karelFacingSouth(self) -> bool:
    """
    is a Karel-Question. Returns wether Karel is currently facing south.

    @return   True if Karel is facing south
    """
    if self.playable():
      return self.karel.orientation == KarelOrientation.SOUTH
    else:
      raise UnallowedActionError("karelFacingSouth")

  def karelFacingWest(self) -> bool:
    """
    is a Karel-Question. Returns wether Karel is currently facing west.

    @return   True if Karel is facing west
    """
    if self.playable():
      return self.karel.orientation == KarelOrientation.WEST
    else:
      raise UnallowedActionError("karelFacingWest")


class LevelManager(metaclass=SingletonMeta):
  """
  Singleton that manages the current level.

  @extends  SingletonMeta

  @param  currentLevel  current level
  """

  currentLevel: Level

  def __init__(self, level: Level = None) -> None:
    self.currentLevel = level

  def setCurrentLevel(self, level: Level) -> None:
    """
    Setter for currentLevel

    @param  level   new level
    """
    self.currentLevel = level

  def getCurrentLevel(self) -> Level:
    """
    Returns current level.

    @return   current level
    """
    return self.currentLevel
