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

# LIBRARY IMPORT
import pygame as pg

# LOCAL IMPORT
from constants import GAME_FONT, WINDOW_TOP_RIGHT
import assets
from assets.color import HexColor


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
