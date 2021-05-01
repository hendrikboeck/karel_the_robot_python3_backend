from collections import OrderedDict
from typing import Any, Dict, Union
import pygame as pg
from pygame.mouse import get_visible
from pygame_gui.elements import UIWindow
from pygame_gui.ui_manager import UIManager
import assets
from beans.io import IOM

from beans.types import Vector2f, SingletonMeta, promiseList
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
