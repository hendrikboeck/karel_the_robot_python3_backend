from abc import ABC, abstractmethod
from typing import Any, Union
import importlib

import pygame as pg
from pygame import Color, Rect, Surface
from pygame.constants import KEYUP, K_SPACE, K_h, K_j, K_q, K_w
from pygame.event import Event
from pygame_gui.ui_manager import UIManager
import assets
from beans.io import IOM
from beans.types import SingletonMeta

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

    windowDimension = pg.display.get_surface().get_size()

  def render(self, screen: Surface) -> None:
    level = LevelManager().getCurrentLevel()
    
    screen.blit(self.backgroundSurf, (0, 0))
    self.uiManager.draw_ui(screen)
    windowDimension = pg.display.get_surface().get_size()
    level.rect.center = ((windowDimension[0] + 300) / 2, windowDimension[1] / 2)
    level.render(screen)

  def proccessEvent(self, event: Event) -> Union[Any, None]:
    level = LevelManager().getCurrentLevel()

    self.uiManager.process_events(event)
    level.proccessEvent(event)

    # if event.type == KEYUP:
    #   if event.key == K_w:
    #     level.karelMove()
    #   elif event.key == K_q:
    #     level.karelTurnLeft()
    #   elif event.key == K_h:
    #     level.karelPickBeeper()
    #   elif event.key == K_j:
    #     level.karelPutBeeper()

  def update(self, **kwargs) -> Union[Any, None]:
    self.uiManager.update(kwargs["time_delta"])
    LevelManager().getCurrentLevel().update(self.sidemenu.speedSlider.current_value)
