# STL-IMPORT
from typing import Any, Iterable, List, Union, Dict
from abc import ABC, abstractmethod

# LIBRARY-IMPORT
import pygame as pg
from pygame_gui import elements
from pygame_gui.elements import UILabel
from pygame_gui.core import ObjectID
from pygame_gui.core.interfaces import IContainerLikeInterface, IUIManagerInterface
from pygame_gui.core import UIElement


class GLabel(UILabel):

  dynamicSize: bool

  def __init__(
      self,
      relative_rect: pg.Rect,
      manager: IUIManagerInterface,
      text: str = None,
      container: Union[IContainerLikeInterface, None] = None,
      parent_element: UIElement = None,
      object_id: Union[ObjectID, str, None] = None,
      anchors: Dict[str, str] = None,
      visible: int = 1
  ) -> None:
    super().__init__(
        relative_rect=relative_rect,
        text="",
        manager=manager,
        container=container,
        parent_element=parent_element,
        object_id=object_id,
        anchors=anchors,
        visible=visible
    )
    self.dynamicSize = (relative_rect.width == 0 and relative_rect.height == 0)
    self.set_text(text or "")

  def set_text(self, text: str) -> None:
    if text != self.text:
      self.text = text
      if self.dynamicSize:
        self.set_dimensions(self.font.size(text))  # rebuilds in proccess
      else:
        self.rebuild()
