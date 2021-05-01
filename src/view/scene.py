from abc import ABC, abstractmethod
from typing import Any, Union
import importlib

import pygame as pg
from pygame import Color, Rect, Surface
from pygame.constants import KEYUP, K_SPACE, K_q, K_w
from pygame.event import Event
from pygame_gui.ui_manager import UIManager
import assets
from beans.io import IOM

from constants import *
from game import Level, LevelManager
from view.menu import Sidemenu


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


## class SceneFactory(ABC):
##
##   @staticmethod
##   def create(classname: str, args: list) -> ISceneInterface:
##     Class = getattr(importlib.import_module("view.scene"), classname)
##     return Class(*args)


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
  level: Level

  def __init__(self) -> None:
    self.backgroundSurf = Surface(tuple(WINDOW_DIMENSIONS))
    self.backgroundSurf.fill(SCREEN_BACKGROUND_COLOR)
    self.uiManager = assets.load.uimanager("theme/Sidemenu.json")
    self.sidemenu = Sidemenu(self.uiManager, 300)
    windowDimension = pg.display.get_surface().get_size()
    self.level = Level("BeeperPicking", (windowDimension[0] - 320, windowDimension[1] - 20))
    LevelManager().setCurrentLevel(self.level)

  def render(self, screen: Surface) -> None:
    screen.blit(self.backgroundSurf, (0, 0))
    self.uiManager.draw_ui(screen)
    windowDimension = pg.display.get_surface().get_size()
    self.level.rect.center = ((windowDimension[0] + 300) / 2, windowDimension[1] / 2)
    self.level.render(screen)

  def proccessEvent(self, event: Event) -> Union[Any, None]:
    self.uiManager.process_events(event)
    self.level.proccessEvent(event)

    if event.type == KEYUP:
      if event.key == K_w:
        self.level.karelMove()
      elif event.key == K_q:
        self.level.karelTurnLeft()

  def update(self, **kwargs) -> Union[Any, None]:
    self.uiManager.update(kwargs["time_delta"])
    self.level.update()
