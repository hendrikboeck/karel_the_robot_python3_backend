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
from abc import ABC, abstractmethod
from typing import Any, Union

# LIBRARY IMPORT
from pygame import Rect, Surface
from pygame.event import Event
from pygame_gui.ui_manager import UIManager

# LOCAL IMPORT
from constants import WINDOW_DIMENSIONS, WINDOW_CENTER, SCREEN_BACKGROUND_COLOR
from game import LevelManager
from view.menu import Sidemenu
import assets
from assets.color import HexColor
from pyadditions.types import SingletonMeta


class ISceneInterface(ABC):

  @abstractmethod
  def render(self, screen: Surface) -> None:
    raise NotImplementedError()

  @abstractmethod
  def update(self, **kwargs) -> Union[Any, None]:
    raise NotImplementedError()

  @abstractmethod
  def proccessEvent(self, event: Event) -> Union[Any, None]:
    raise NotImplementedError()


class SceneManager(metaclass=SingletonMeta):

  _cur: ISceneInterface

  def __init__(self) -> None:
    self._cur = WelcomeScene()

  def setScene(self, newScene: ISceneInterface) -> None:
    self._cur = newScene

  def getScene(self) -> ISceneInterface:
    return self._cur


class WelcomeScene(ISceneInterface):

  TEXT = "Welcome to 'Karel the robot'!"

  backgroundSurf: Surface
  textSurf: Surface
  textRect: Rect

  def __init__(self) -> None:
    self.backgroundSurf = Surface(tuple(WINDOW_DIMENSIONS))
    self.backgroundSurf.fill(HexColor("#dddddd"))
    textFont = assets.load.font("font/FiraCode-Bold.ttf", 48)
    self.textSurf = textFont.render(self.TEXT, True, HexColor("#bdbdbd"))
    self.textRect = self.textSurf.get_rect()
    self.textRect.center = tuple(WINDOW_CENTER)

  def render(self, screen: Surface) -> None:
    screen.blit(self.backgroundSurf, (0, 0))
    screen.blit(self.textSurf, self.textRect)

  def update(self, **kwargs) -> Union[Any, None]:
    pass

  def proccessEvent(self, event: Event) -> Union[Any, None]:
    pass


class GameScene(ISceneInterface):

  backgroundSurf: Surface
  uiManager: UIManager
  sidemenu: Sidemenu

  def __init__(self) -> None:
    if LevelManager().getCurrentLevel() is None:
      raise Exception("A Level has to loded, before GameScene in initialized")

    self.backgroundSurf = Surface(tuple(WINDOW_DIMENSIONS))
    self.backgroundSurf.fill(SCREEN_BACKGROUND_COLOR)
    self.uiManager = assets.load.uimanager("theme/Sidemenu.json")
    self.sidemenu = Sidemenu(self.uiManager, 300)

  def render(self, screen: Surface) -> None:
    level = LevelManager().getCurrentLevel()

    screen.blit(self.backgroundSurf, (0, 0))
    self.uiManager.draw_ui(screen)
    level.rect.center = (
        (WINDOW_DIMENSIONS.x + 300) / 2, WINDOW_DIMENSIONS.y / 2
    )
    level.render(screen)

  def proccessEvent(self, event: Event) -> Union[Any, None]:
    level = LevelManager().getCurrentLevel()

    self.uiManager.process_events(event)
    level.proccessEvent(event)

  def update(self, **kwargs) -> Union[Any, None]:
    self.uiManager.update(kwargs["time_delta"])
    LevelManager().getCurrentLevel().update(
        self.sidemenu.speedSlider.current_value
    )
