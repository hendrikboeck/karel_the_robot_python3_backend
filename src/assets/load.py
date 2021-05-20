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
from io import BytesIO
from xml.etree import cElementTree as ElementTree
from xml.etree.ElementTree import Element
import sys
import functools

# LIBRARY IMPORT
import pygame
from pygame import Surface
from pygame.font import Font
from pygame_gui.ui_manager import UIManager

# LOCAL IMPORT
from constants import FUNC_CACHE_SIZE, ASSETS_FOLDER

# for packaging assets into .exe
def __resource_path(relativePath: str) -> str:
  try:
    basePath = sys._MEIPASS
  except Exception:
    basePath = os.path.abspath(".")
  return os.path.join(basePath, relativePath)


def __get_assetpath(relativePath: str) -> str:
  try:
    localPath = os.path.join(ASSETS_FOLDER, relativePath)
    with open(localPath) as f:
      pass
    return localPath
  except IOError:
    return os.path.join(__resource_path(ASSETS_FOLDER), relativePath)


# @functools.lru_cache(maxsize=FUNC_CACHE_SIZE)
# TODO: pygame.image.load already cached? -> weird artifacts
def image(filepath: str) -> Surface:
  filepath = __get_assetpath(filepath)
  return pygame.image.load(filepath).convert_alpha()


# @functools.lru_cache(maxsize=FUNC_CACHE_SIZE)
# TODO: pygame.image.load already cached? -> weird artifacts
def binaryImage(bin_: bytes) -> Surface:
  return pygame.image.load(BytesIO(bin_)).convert_alpha()


@functools.lru_cache(maxsize=FUNC_CACHE_SIZE)
def font(name: str, size: int) -> Font:
  filepath = __get_assetpath(name)
  return Font(filepath, size)


def __xmlnode_to_tuple(node: Element) -> tuple:
  nodeData = None

  for subNode in node:
    nodeData = nodeData or {}
    (tag, items) = __xmlnode_to_tuple(subNode)
    if nodeData.get(tag):
      if type(nodeData[tag]) == list:
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


# @functools.lru_cache(maxsize=FUNC_CACHE_SIZE)
def xml(filepath: str) -> dict:
  tree = ElementTree.parse(__get_assetpath(filepath))
  (key, value) = __xmlnode_to_tuple(tree.getroot())

  if type(value) == dict: return value
  else: return {key: value}


def xmls(data: str) -> dict:
  (key, value) = __xmlnode_to_tuple(ElementTree.fromstring(data))
  return {key: value}


def uimanager(theme: str) -> UIManager:
  return UIManager(
      pygame.display.get_surface().get_size(),
      theme_path=__get_assetpath(theme)
  )
