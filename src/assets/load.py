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
import os
import sys
from io import BytesIO
from xml.etree import cElementTree as ElementTree
from xml.etree.ElementTree import Element

# LIBRARY IMPORT
import pygame
from pygame import Surface
from pygame.font import Font
from pygame_gui.ui_manager import UIManager

# LOCAL IMPORT
from constants import ASSETS_FOLDER, WINDOW_DIMENSIONS
from pyadditions.sys import fileExists


def _getResourcePath(relativePath: str) -> str:
  """
  Returns a relative path for resource loading. If app is run as executable the
  resources will be loaded from exe. When run as python, local files will be
  used

  @param  relativePath  relative path in ASSETS_FOLDER
  @return               absolute path in pwd
  """
  localPath = os.path.join(ASSETS_FOLDER, relativePath)
  if fileExists(localPath):
    return localPath
  else:
    return os.path.join(sys._MEIPASS, ASSETS_FOLDER, relativePath)


def image(filepath: str) -> Surface:
  """
  Loads image from ASSETS_FOLDER.

  @param  filepath  filepath to image in ASSETS_FOLDER
  @return           pg.Surface of image
  """
  filepath = _getResourcePath(filepath)
  return pygame.image.load(filepath).convert_alpha()


def binaryImage(bin_: bytes) -> Surface:
  """
  Loads image from bytes-array.

  @param  bin_  image as bytes-array
  @return       pg.Surface of binary-image
  """
  return pygame.image.load(BytesIO(bin_)).convert_alpha()


def font(filepath: str, size: int) -> Font:
  """
  Loads font from assets.

  @param  filepath  filepath to font in ASSETS_FOLDER
  @param  size      fontsize
  @return           pg.Font of font
  """
  filepath = _getResourcePath(filepath)
  return Font(filepath, size)


def _xmlnodeToTuple(node: Element) -> tuple:
  """
  Converts xmlnode to tuple.

  @param  node  xmlnode
  @return       xmlnode as tuple
  """
  nodeData = None

  for subNode in node:
    nodeData = nodeData or {}
    (tag, items) = _xmlnodeToTuple(subNode)
    if nodeData.get(tag):
      if isinstance(nodeData[tag], list):
        nodeData[tag].append(items)
      else:
        nodeData[tag] = [nodeData[tag], items]
    else:
      nodeData[tag] = items

  if node.items() != []:
    nodeData = nodeData or {}
    for (key, value) in node.items():
      nodeData[key] = value

  return (node.tag, nodeData)


def xml(filepath: str) -> dict:
  """
  Loads .xml-file from assets.

  @param  filepath  filepath to .xml-file in ASSETS_FOLDER
  @return           xml as dict
  """
  tree = ElementTree.parse(_getResourcePath(filepath))
  (key, value) = _xmlnodeToTuple(tree.getroot())

  if isinstance(value, dict): return value
  else: return {key: value}


def xmls(data: str) -> dict:
  """
  Loads xml from string.

  @param  data  xml as string
  @return       xml as dict
  """
  (key, value) = _xmlnodeToTuple(ElementTree.fromstring(data))
  return {key: value}


def uimanager(themeFilepath: str) -> UIManager:
  """
  Loads a uimanager with the specified theme from ASSETS_FOLDER.

  @param  themeFilepath  filepath to theme.json for uimanager
  @return                uimanager with theme
  """
  return UIManager(
      tuple(WINDOW_DIMENSIONS), theme_path=_getResourcePath(themeFilepath)
  )
