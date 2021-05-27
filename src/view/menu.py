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

# LIBRARY IMPORT
import pygame as pg
from pygame_gui import UIManager
from pygame_gui.core.ui_container import UIContainer
from pygame_gui.elements import UIPanel, UIButton, UIHorizontalSlider

# LOCAL IMPORT
import assets
from pyadditions.io import IOM
from pyadditions.types import Vector2f, promiseList
from constants import WINDOW_DIMENSIONS, WINDOW_TOP_LEFT, GAME_START_EVENT, GAME_FINISHED_EVENT
from .elements import GLabel


class ClickButtonMenu(UIPanel):
  """
  Dropdown-style menu that gets shown on Rightclick.
 
  @param  menuitems   ordered dict of menuitems
  @param  dim         ordered dict of menuitems
  """

  BUTTON_PADDING = Vector2f(15, 5)

  menuitems: OrderedDict[str, UIButton]
  dim: Vector2f  # super().dimensions exists!

  ##
  # constructor
  #
  # @param  manager                 UIManager for pygame_gui elements
  # @param  assetsPath [optional]   path to .xml-file containing menu-config
  #
  def __init__(self, manager: UIManager, assetsPath: str = None) -> None:
    super().__init__(pg.Rect(0, 0, 0, 0), 0, manager, visible=False)
    self.dim = Vector2f(0, 0)
    self.menuitems = OrderedDict()

    if assetsPath:
      items = promiseList(assets.load.xml(assetsPath)["item"])
      for i in items:
        self.addListItem(i["key"], i["text"])

  ##
  # Can be overridden, also handle resizing windows. Gives UI Windows access to pygame events.
  # Currently just blocks mouse click down events from passing through the panel.
  #
  # @param  event   the event to process
  # @return         should return True if this element consumes this event
  #
  def process_event(self, event: pg.event.Event) -> bool:
    if event.type == pg.MOUSEBUTTONDOWN:
      if event.button == 3:  # Rechtsklick
        self.set_position(pg.mouse.get_pos())
        self.show()
        return False
      elif event.button == 1:  # Linksklick
        self.hide()
        return False
    for item in self.menuitems.values():
      item.process_event(event)
    return super().process_event(event)

  ##
  # Adds a new listitem, which is identified by a key, to the menu.  The item will be returned
  # or can be accessed through function 'getListItem'.
  #
  # @param  key   key for identification of object inside menu
  # @param  text  the text of the menuitem
  # @return       newly created listitem (UIButton)
  #
  def addListItem(self, key: str, text: str) -> UIButton:
    button = self.menuitems[key] = UIButton(
        relative_rect=pg.Rect(0, self.dim.y, 0, 0),
        text=text,
        manager=self.ui_manager,
        container=self
    )
    # calculate size of button-label
    labelDim = Vector2f._make(button.font.size(text))

    # create button-size
    minButtonSize = Vector2f(
        labelDim.x + 2 * self.BUTTON_PADDING.x,
        labelDim.y + 2 * self.BUTTON_PADDING.y
    )

    # update width for all buttons in menu
    if self.dim.x < minButtonSize.x:
      for item in self.menuitems.values():
        size = item.get_relative_rect()
        item.set_dimensions((minButtonSize.x, size.height))
      self.dim.x = minButtonSize.x

    # update new dimensions of button
    button.set_dimensions((self.dim.x, minButtonSize.y))

    # update dimensions of panel
    self.dim.y += minButtonSize.y
    self.set_dimensions(tuple(self.dim))

    # return newly created Button
    return self.menuitems[key]

  ##
  # Returns the listitem to a given key inside menu.  If key dos not exist None will be
  # returned.
  #
  # @param  key   key for identification of object inside menu
  # @return       coresponding listitem (UIButton) for key
  #
  def getListItem(self, key: str) -> UIButton:
    return self.menuitems.get(key)


class Sidemenu(UIPanel):

  _container: UIContainer
  startBtn: UIButton
  speedSlider: UIHorizontalSlider
  speedLabel: GLabel

  def __init__(self, manager: UIManager, width: float) -> None:
    if width < 1:
      width *= WINDOW_DIMENSIONS.x
    super().__init__(
        relative_rect=pg.Rect(
            tuple(WINDOW_TOP_LEFT), (width, WINDOW_DIMENSIONS.y)
        ),
        starting_layer_height=0,
        manager=manager
    )
    containerRect = pg.Rect(0, 0, 200, 70)
    containerRect.center = (
        self.relative_rect.width * 0.5, self.relative_rect.height * 0.35
    )
    self._container = UIContainer(
        relative_rect=containerRect,
        manager=self.ui_manager,
        starting_height=0,
        container=self
    )
    padding = 3  # px
    self.startBtn = UIButton(
        relative_rect=pg.Rect(
            padding, padding, containerRect.width - 2*padding,
            (containerRect.height - 3*padding) / 2
        ),
        text="start",
        manager=self.ui_manager,
        container=self._container
    )
    self.speedSlider = UIHorizontalSlider(
        relative_rect=pg.Rect(
            padding, 2*padding + self.startBtn.relative_rect.height,
            0.7 * (containerRect.width - 2*padding),
            (containerRect.height - 3*padding) / 2
        ),
        start_value=1.0,
        value_range=(0.5, 15.0),
        manager=self.ui_manager,
        container=self._container
    )
    self.speedLabel = GLabel(
        relative_rect=pg.Rect(
            padding + self.speedSlider.relative_rect.width,
            2*padding + self.startBtn.relative_rect.height,
            containerRect.width - 2*padding -
            self.speedSlider.relative_rect.width,
            (containerRect.height - 3*padding) / 2
        ),
        text=f"{self.speedSlider.current_value:.2f}",
        manager=self.ui_manager,
        container=self._container
    )

  def process_event(self, event: pg.event.Event) -> bool:
    if event == GAME_START_EVENT:
      self.startBtn.disable()
    elif event == GAME_FINISHED_EVENT:
      self.startBtn.enable()
    return super().process_event(event)

  def update(self, time_delta: float) -> None:
    self.speedLabel.set_text(f"{self.speedSlider.current_value:.2f}")
    if self.startBtn.check_pressed():
      pg.event.post(GAME_START_EVENT)
      IOM.debug(f"POSTED '{GAME_START_EVENT.attr1}'")
    return super().update(time_delta)
