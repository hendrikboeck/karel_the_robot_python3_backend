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

# STL-IMPORT
from typing import Union, Dict

# LIBRARY-IMPORT
import pygame as pg
from pygame_gui.elements import UILabel
from pygame_gui.core import ObjectID
from pygame_gui.core.interfaces import IContainerLikeInterface, IUIManagerInterface
from pygame_gui.core import UIElement


class GLabel(UILabel):
  """
  Is a UILabel that dynamicaly sizes to text, if bounds of rect is (0, 0), else
  it is a normal UILabel.

  @extends  UILabel

  @param  dynamicSize   flag that makes UILable dynamic.
  """

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
    """
    constructor

    @param  relative_rect   rect relative to/in container
    @param  manager         uimanager
    @param  text            text of label
    @param  container       container of label
    @param  parent_element  parent element of label
    @param  object_id       id of gui-object
    @param  anchors         anchors of gui-object
    @param  visible         sets, if label will be visible on create
    """
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
    """
    Sets text of label. If label is dynamic-flag, then it will also resize the
    label.

    @overwrite

    @param  text  text to be shown on label
    """
    if text != self.text:
      self.text = text
      if self.dynamicSize:
        self.set_dimensions(self.font.size(text))  # rebuilds in proccess
      else:
        self.rebuild()
