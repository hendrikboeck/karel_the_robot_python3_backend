################################################################################
# python_backend_karel_the_robot                                               #
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

# LIBRARY IMPORT
from pygame import Surface, Rect, SRCALPHA
import pygame as pg

# LOCAL IMPORT
from beans.io import IOM
from beans.types import EnumLike, SingletonMeta, Vector2f, promiseList
import assets
from assets.color import HexColor
from constants import GAME_ERROR_EVENT, GAME_FONT, GAME_START_EVENT
from view.window import DebugInformationDict


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
  """
  Enum of all the compass-directions as _KarelOrientationTuple
  """

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
    """
    Rebuilds the render-surface of Tile.
    """
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
      beeperRect = beeperSurf.get_rect()
      if self.rect.width != beeperRect.width:
        beeperSurf = pg.transform.smoothscale(
            beeperSurf, (self.rect.width, self.rect.height)
        )
      self.surf.blit(beeperSurf, (0, 0))
    if self._beepers > 1:
      beeperNumFont = assets.load.font(GAME_FONT, 14)
      beeperNumSurf = beeperNumFont.render(
          str(self._beepers), True, HexColor("#000000")
      )
      beeperNumRect = beeperNumSurf.get_rect()
      beeperNumRect.center = self.rect.center
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
    """
    Rebuilds the render-surface of Karel.
    """
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
    """
    Rotates Karel by 90deg.
    """
    self.setOrientation(
        KarelOrientation.fromAngle((self.orientation.angle + 90) % 360)
    )


class World():

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
    for row in self.tiles:
      for tile in row:
        self.surf.blit(tile.surf, tile.rect)

  def render(self, surf: Surface) -> None:
    surf.blit(self.surf, self.rect)

  # KCS - Karel Cordinate System
  def getTileAtKCS(
      self, pos: Union[Tuple[float, float], List[float], Vector2f]
  ) -> Tile:
    return self.tiles[int(pos[1]) - 1][int(pos[0]) - 1]

  def isOutOfBoundsKCS(
      self, pos: Union[Tuple[float, float], List[float], Vector2f]
  ) -> bool:
    pos = Vector2f._make(pos)
    return pos < (1, 1) or pos > self.size

  def rebuildTileAt(
      self, pos: Union[Tuple[float, float], List[float], Vector2f]
  ) -> None:
    tile = self.getTileAt(pos)
    tile.rebuild()
    self.surf.blit(tile.surf, tile.rect)


def createMapConfigFromXML(xml_: Dict[str, Any]) -> Dict[str, Any]:
  conf = {}

  conf["world"] = {}

  conf["world"]["size"] = Vector2f(*eval(xml_["size"]))
  metadata = xml_.get("metadata", {})
  conf["world"]["metadata"] = {
      "name": metadata.get("name", "unkown"),
      "version": metadata.get("version", "unkown"),
      "author": metadata.get("author", "unkown"),
      "speed": xml_.get("speed", "1.0")
  }

  walls = promiseList(xml_.get("wall", []))
  for wall in walls:
    wall["start"] = Vector2f(*eval(wall["start"]))
    wall["length"] = abs(int(wall.get("length", "1")))
    wall["orientation"] = KarelOrientation.fromString(wall["orientation"])
  conf["world"]["walls"] = walls

  beepers = promiseList(xml_.get("beeper", []))
  for beeper in beepers:
    beeper["position"] = Vector2f(*eval(beeper["position"]))
    beeper["n"] = abs(int(float(beeper.get("n", "1"))))
  conf["world"]["beepers"] = beepers

  karel = xml_.get("karel", {})
  conf["karel"] = {}
  conf["karel"]["position"] = Vector2f(*eval(karel.get("position", "(1, 1)")))
  conf["karel"]["orientation"] = KarelOrientation.fromString(
      karel.get("orientation", "EAST")
  )
  conf["karel"]["beeperbag"] = float(karel.get("beeperbag", "inf"))

  conf["speed"] = abs(float(xml_.get("speed", "1.0")))

  return conf


class LevelState(EnumLike):

  INIT = 1
  RUNNING = 2
  ERROR = 3
  FINISHED = 4

  @staticmethod
  def toStr(state: int) -> str:
    if state == LevelState.INIT:
      return "LevelState.INIT"
    elif state == LevelState.RUNNING:
      return "LevelState.RUNNING"
    elif state == LevelState.ERROR:
      return "LevelState.ERROR"
    elif state == LevelState.FINISHED:
      return "LevelState.FINISHED"


class Level():

  surf: Surface
  renderSurf: Surface
  rect: Rect

  state: int
  rFactor: float  # scale
  karelLastPosition: Vector2f
  speed: float
  world: World
  karel: Karel

  def __init__(
      self, mapName: str, bounds: Union[Tuple[float, float], List[float],
                                        Vector2f]
  ) -> None:
    try:
      mapXml = assets.load.xml(f"map/{mapName}.xml")
      map_ = createMapConfigFromXML(mapXml)
    except Exception as e:
      raise MapLoadingError(e)
      #raise e
      #raise MapLoadingError(f"XML-file not found or wrong Map-format: Excpetion: {e}")

    self.world = World(map_["world"])
    self.karel = Karel(map_["karel"])
    self.speed = map_["speed"]
    self.surf = Surface((self.world.rect.width + 2, self.world.rect.height + 2))
    self.rect = self.surf.get_rect()
    self.state = LevelState.INIT
    self.gChanged = False
    self.rFactor = 1.0

    self.repaint()

    ratio = min(bounds[0] / self.rect.width, bounds[1] / self.rect.height)
    if ratio < 1.0:
      self.scale(ratio)

  def playable(self) -> bool:
    return (self.state == LevelState.RUNNING)

  def scale(self, rFactor: float) -> None:
    self.rFactor = rFactor
    orgRect = self.surf.get_rect()
    self.rect.width = orgRect.width * self.rFactor
    self.rect.height = orgRect.height * self.rFactor
    if self.rFactor != 1.0:
      IOM.out("WARNING: slow performance, due to scaling (map to big)")

  def repaint(self) -> None:
    self.surf.fill(HexColor("#000000"))
    self.surf.blit(self.world.surf, (1, 1))
    karelRect = self.world.getTileAt(self.karel.position).rect
    self.surf.blit(self.karel.surf, (karelRect.x + 1, karelRect.y + 1))

  def update(self) -> None:
    DebugInformationDict().update(
        KAREL_POSITION=self.karel.position,
        KAREL_ORIENTATION=
        f"{self.karel.orientation.name} / {self.karel.orientation.angle}",
        KAREL_BEEPER_BAG=self.karel.beeperbag
    )

  def render(self, surf: Surface) -> None:
    if self.rFactor != 1.0:
      # TODO: bad performance in software-mode
      surf.blit(
          pg.transform.smoothscale(
              self.surf, (self.rect.width, self.rect.height)
          ), self.rect
      )
    else:
      surf.blit(self.surf, self.rect)

  def proccessEvent(self, event: pg.event.Event) -> None:
    if event == GAME_ERROR_EVENT:
      self._changeLevelState(LevelState.ERROR)
    if event == GAME_START_EVENT:
      self._changeLevelState(LevelState.RUNNING)

  def _changeLevelState(self, state: int) -> None:
    self.state = state
    IOM.debug(f"levelstate changed to '{LevelState.toStr(self.state)}'")

  def startLevel(self) -> None:
    if self.state == LevelState.INIT:
      self.state = LevelState.RUNNING
    else:
      IOM.error(
          f"can not start level: wrong state '{LevelState.toStr(self.state)}'"
      )

  def waitOnStart(self) -> None:
    if self.state == LevelState.INIT:
      IOM.out(f"waiting on '{GAME_START_EVENT.attr1}'")
      while self.state == LevelState.INIT:
        sleep(0.07)

  #
  #
  # ---------------------- KAREL-LOGIC -------------------------------
  #
  #

  def karelMove(self) -> None:
    if self.playable():
      if self.karelFrontIsClear():
        self.world.rebuildTileAt(self.karel.position)
        self.karel.position += self.karel.orientation.vector
        self.repaint()
      else:
        raise ActionExecutionError()
    else:
      raise UnallowedActionError("karelMove")

  def karelTurnLeft(self) -> None:
    if self.playable():
      self.world.rebuildTileAt(self.karel.position)
      self.karel.rotate90()
      self.repaint()
    else:
      raise UnallowedActionError("karelTurnLeft")

  def karelPickBeeper(self) -> None:
    if self.playable():
      if self.karelBeeperPresent():
        self.world.getTileAtKCS(self.karel.position).decrBeepers()
        self.karel.incrBeeperbag()
        self.world.rebuildTileAt(self.karel.position)
        self.repaint()
      else:
        raise ActionExecutionError()
    else:
      raise UnallowedActionError("karelPickBeeper")

  def karelPutBeeper(self) -> None:
    if self.playable():
      if not self.karel.beeperbagIsEmpty():
        self.world.getTileAtKCS(self.karel.position).incrBeepers()
        self.karel.decrBeeperbag()
        self.world.rebuildTileAt(self.karel.position)
        self.repaint()
      else:
        raise ActionExecutionError()
    else:
      raise UnallowedActionError("karelPutBeeper")

  def _karelIsOrientationBlocked(
      self, orientation: _KarelOrientationTuple
  ) -> bool:
    nextTileKCSPoint = self.karel.position + orientation.vector

    outOfBounds = self.world.isOutOfBoundsKCS(nextTileKCSPoint)
    hitWall = self.world.getTileAtKCS(self.karel.position).wallAt(
        orientation.angle
    ) or self.world.getTileAtKCS(nextTileKCSPoint).wallAt(
        (orientation.angle + 180) % 360
    )

    return outOfBounds or hitWall

  def karelFrontIsClear(self) -> bool:
    if self.playable():
      return not self._karelIsOrientationBlocked(self.karel.orientation)
    else:
      raise UnallowedActionError("karelFrontIsClear")

  def karelLeftIsClear(self) -> bool:
    if self.playable():
      return not self._karelIsOrientationBlocked(
          KarelOrientation.fromAngle((self.karel.orientation.angle + 90) % 360)
      )
    else:
      return UnallowedActionError("karelLeftIsClear")

  def karelRightIsClear(self) -> bool:
    if self.playable():
      return not self._karelIsOrientationBlocked(
          KarelOrientation.fromAngle(
              (self.karel.orientation.angle + 270) % 360
          )
      )
    else:
      return UnallowedActionError("karelLeftIsClear")


class LevelManager(metaclass=SingletonMeta):

  currentLevel: Level

  def __init__(self, level: Level = None) -> None:
    self.currentLevel = level

  def setCurrentLevel(self, level: Level) -> None:
    self.currentLevel = level

  def getCurrentLevel(self) -> Level:
    return self.currentLevel