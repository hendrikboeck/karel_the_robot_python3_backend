import pygame as pg
from abc import ABC, abstractmethod
from typing import Iterable
from assets.color import HexColor
from beans.types import Vector2f

from constants import GAME_FONT, WINDOW_DIMENSIONS, WINDOW_TOP_RIGHT
import assets
from beans.io import IOM
from copy import copy


class Overlay(pg.Surface, ABC):

  visible: bool

  def __init__(self, visible: bool) -> None:
    self.visible = visible

  @abstractmethod
  def render(self, surf: pg.Surface) -> None:
    raise NotImplementedError()

  def proccessEvent(self, event: pg.event.Event) -> None:
    pass

  def toggle(self) -> None:
    self.visible = not self.visible

  def show(self) -> None:
    self.visible = True

  def hide(self) -> None:
    self.visible = False


class FPSOverlay(Overlay):

  lastFps: int
  textFont: pg.font.Font
  textSurf: pg.Surface

  def __init__(self, visible: bool = False) -> None:
    super().__init__(visible)

    self.textFont = assets.load.font(GAME_FONT, 16)
    self.textSurf = None
    self.lastFps = None

  def proccessEvent(self, event: pg.event.Event) -> None:
    if event.type == pg.KEYUP:
      if event.key == pg.K_F3:
        self.toggle()

  def update(self, fps: int) -> None:
    fps = int(fps)
    if fps != self.lastFps:
      text = f"{fps}"
      self.textSurf = self.textFont.render(text, True, HexColor("#ff0000"))
      self.lastFps = fps

  def render(self, surf: pg.Surface) -> None:
    if self.visible:
      labelRect = self.textSurf.get_rect()
      labelRect.topright = tuple(WINDOW_TOP_RIGHT + (-5, 5))
      surf.blit(self.textSurf, labelRect)
