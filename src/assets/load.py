# STL IMPORT
import os
from io import BytesIO
from xml.etree import cElementTree as ElementTree
from xml.etree.ElementTree import Element
import sys

# LIBRARY IMPORT
import pygame
from pygame import Surface
from pygame.font import Font
from pygame_gui.ui_manager import UIManager


# for packaging assets into .exe
def __resource_path(relativePath: str) -> str:
  try:
    basePath = sys._MEIPASS
  except Exception:
    basePath = os.path.abspath(".")
  return os.path.join(basePath, relativePath)


__ASSETS_FOLDER = __resource_path("assets")


def image(filepath: str) -> Surface:
  filepath = os.path.join(__ASSETS_FOLDER, filepath)
  return pygame.image.load(filepath).convert_alpha()


def binaryImage(bin_: bytes) -> Surface:
  return pygame.image.load(BytesIO(bin_)).convert_alpha()


def font(name: str, size: int) -> Font:
  filepath = os.path.join(__ASSETS_FOLDER, name)
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


def xml(filepath: str) -> dict:
  tree = ElementTree.parse(os.path.join(__ASSETS_FOLDER, filepath))
  (key, value) = __xmlnode_to_tuple(tree.getroot())

  if type(value) == dict: return value
  else: return {key: value}


def xmls(data: str) -> dict:
  return __xmlnode_to_dict(ElementTree.fromstring(data))


def uimanager(theme: str) -> UIManager:
  return UIManager(
      pygame.display.get_surface().get_size(), theme_path=os.path.join(__ASSETS_FOLDER, theme)
  )
