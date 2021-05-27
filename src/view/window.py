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
from collections import OrderedDict
from typing import Any, Dict

# LIBRARY IMPORT
import pygame as pg
from pygame_gui.elements import UIWindow
from pygame_gui.ui_manager import UIManager

# LOCAL IMPORT
import assets
from pyadditions.types import Vector2f, SingletonMeta, promiseList
from .elements import GLabel


class DebugInformationDict(metaclass=SingletonMeta):

  _internal: Dict[str, Any]

  def __init__(self) -> None:
    self._internal = {}

  def update(self, **kwargs: Dict[str, Any]) -> None:
    for key, value in kwargs.items():
      self._internal[str(key)] =  value
  
  def get(self, key: str) -> Any:
    return self._internal.get(key)


class DebugWindow(UIWindow):

  MARGIN = 3

  _labelPos: Vector2f
  labelDict: OrderedDict[str, GLabel]

  def __init__(self, manager: UIManager, resizable: bool):
    super().__init__(pg.Rect(0, 0, 0, 0), manager, "Debug", resizable=resizable, visible=False)
    self.labelDict = OrderedDict()
    self._labelPos = Vector2f(self.MARGIN, self.MARGIN)

  def process_event(self, event: pg.event.Event) -> bool:
    return super().process_event(event)

  def loadView(self, view: str) -> None:
    self.labelDict = OrderedDict()
    self._labelPos = Vector2f(self.MARGIN, self.MARGIN)

    viewDict = assets.load.xml(view)
    self.set_display_title(f"Debug ({viewDict['name']})")
    self.set_dimensions((int(viewDict["width"]), int(viewDict["height"])))

    for block in promiseList(viewDict["block"]):
      self._createSpacer(10)
      title = block.get("descriptor")
      if title: self._printLabel(title)
      for item in promiseList(block["item"]):
        self._printLabel(item["descriptor"], item.get("id"))

  def _createSpacer(self, height: int) -> None:
    if self._labelPos.y > self.MARGIN:
      self._labelPos.y += 10

  def _printLabel(self, text: str, id_: str = None) -> None:
    label = GLabel(
        relative_rect=pg.Rect(self._labelPos.x, self._labelPos.y, 0, 0),
        manager=self.ui_manager,
        text=text,
        container=self
    )
    if id_:
      self.labelDict[id_] = GLabel(
          relative_rect=pg.Rect(
              label.get_relative_rect().width + self._labelPos.x, self._labelPos.y, 0, 0
          ),
          manager=self.ui_manager,
          container=self
      )
    self._labelPos.y += label.get_relative_rect().height

  def getLabel(self, key: str) -> GLabel:
    return self.labelDict[key]

  def update(self, timedelta: float) -> None:
    dinfo = DebugInformationDict()
    for key in self.labelDict:
      self.labelDict[key].set_text(str(dinfo.get(key)))
    super().update(timedelta)

  def toggle(self) -> None:
    self.hide() if self.visible else self.show()

  def kill(self) -> None:
    self.hide()

  def _kill(self) -> None:
    super().kill()
