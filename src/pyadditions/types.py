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
from __future__ import annotations
from abc import ABC, ABCMeta, abstractmethod
from typing import Any, Dict, Iterable, Union, List


def promiseList(val: Any) -> List[Any]:
  """
  Promises the value to be list. If it is already a list the function will just
  return the value, if not the function will return val as a list.

  @param  val   value that should be promised as a list
  @return       val, now as list, if it was not
  """
  if isinstance(val, list): return val
  else: return [val]


def classname(obj: object) -> str:
  """
  Returns the classname of an object as a string.

  @param  obj   object
  @return       classname of object as string
  """
  return obj.__class__.__name__


def defaultOnError(func: function, alt_val: Any) -> Any:
  """
  Returns a default value, if function fails to execute and throws Exception.

  @param  func    function
  @param  alt_val default value
  @return         return of function or on error alt_val
  """
  try:
    return func()
  except:
    return alt_val


def defaultOnNone(val: Any, alt_val: Any) -> Any:
  """
  Returns a default value, if val is None.

  @param  val     value to be checked
  @param  alt_val default value
  @return         val if not None, else alt_val
  """
  if val is None:
    return alt_val
  else:
    return val

# Interface declaration (just renaming of ABC in python)
InterfaceMeta = ABCMeta
Interface = ABC
interfacemethod = abstractmethod

# NotInstanceable declaration
NotInstanceable = ABC


class EnumLikeMeta(type):
  """
  Enumlike class that prevents a object of class to be instanciated and just
  function as a wrapper for static values and static functions.

  @extends  type
  """

  def __call__(cls, *args: List[Any], **kwargs: Dict[str, Any]) -> Any:
    raise TypeError(
        f"{cls.__module__}.{cls.__qualname__} has no public constructor"
    )


class EnumLike(metaclass=EnumLikeMeta):
  """Class wrapper for EnumLikeMeta"""
  pass


class SingletonMeta(type):
  """
  Metaclass for Singleton GoF pattern.

  @param  _INSTANCES  dict of instances of class
  """

  _INSTANCES: dict = {}

  def __call__(cls, *args, **kwargs):
    if not cls._INSTANCES.get(cls):
      cls._INSTANCES[cls] = super(SingletonMeta, cls).__call__(*args, **kwargs)
    return cls._INSTANCES.get(cls)


class SingletonFactoryMeta(type):
  """
  Metaclass for Singletons that are identified through a string.

  @param  _INSTANCES  dict of instances of class
  """

  _INSTANCES: dict = {}

  def __call__(cls, *args: Any, **kwargs: Any) -> Any:
    if not cls._INSTANCES.get(args[0]):
      cls._INSTANCES[args[0]] = \
        super(SingletonFactoryMeta, cls).__call__(*args, **kwargs)
    return cls._INSTANCES.get(args[0])


class Flag(metaclass=SingletonFactoryMeta):

  key: str = None
  value: bool = None

  def __init__(self, key: str, value: bool) -> None:
    self.key = key
    self.value = value

  def set(self, value: bool) -> None:
    self.value = value

  def get(self) -> bool:
    return self.value


class Vector2f():

  x: float = None
  y: float = None

  def __init__(self, x: float, y: float) -> None:
    self.x = x
    self.y = y

  def __iter__(self):
    yield self.x
    yield self.y

  def __str__(self) -> str:
    return f"Vector2f(x={self.x}, y={self.y})"

  def __getitem__(self, i: int) -> float:
    return list(self)[i]

  def __list__(self) -> list:
    return [self.x, self.y]

  def __add__(self, other: Iterable) -> Vector2f:
    return Vector2f(self.x + other[0], self.y + other[1])

  def __sub__(self, other: Iterable) -> Vector2f:
    return Vector2f(self.x - other[0], self.y - other[1])

  def __mul__(self, other: Union[Iterable, float]) -> Vector2f:
    if isinstance(other, (float, int)):
      return Vector2f(self.x * other, self.y * other)
    else:
      return Vector2f(self.x * other[0], self.y * other[1])

  def __truediv__(self, other: Union[Iterable, float]) -> Vector2f:
    if isinstance(other, (float, int)):
      return Vector2f(self.x / other, self.y / other)
    else:
      return Vector2f(self.x / other[0], self.y / other[1])

  def __floordiv__(self, other: Union[Iterable, float]) -> Vector2f:
    if isinstance(other, (float, int)):
      return Vector2f(self.x // other, self.y // other)
    else:
      return Vector2f(self.x // other[0], self.y // other[1])

  def __mod__(self, other: Union[Iterable, float]) -> Vector2f:
    if isinstance(other, (float, int)):
      return Vector2f(self.x % other, self.y % other)
    else:
      return Vector2f(self.x % other[0], self.y % other[1])

  def __pow__(self, n: float) -> Vector2f:
    return Vector2f(self.x**n, self.y**n)

  def __rshift__(self, other: Union[Iterable, float]) -> Vector2f:
    if isinstance(other, (float, int)):
      return Vector2f(self.x >> other, self.y >> other)
    else:
      return Vector2f(self.x >> other[0], self.y >> other[1])

  def __lshift__(self, other: Union[Iterable, float]) -> Vector2f:
    if isinstance(other, (float, int)):
      return Vector2f(self.x << other, self.y << other)
    else:
      return Vector2f(self.x << other[0], self.y << other[1])

  def __lt__(self, other: Iterable) -> bool:
    return self.x < other[0] or self.y < other[1]

  def __gt__(self, other: Iterable) -> bool:
    return self.x > other[0] or self.y > other[1]

  def __le__(self, other: Iterable) -> bool:
    return self < other or self == other

  def __ge__(self, other: Iterable) -> bool:
    return self > other or self == other

  def __eq__(self, other: Iterable) -> bool:
    return self.x == other[0] and self.y == other[1]

  def __ne__(self, other: Iterable) -> bool:
    return not (self == other)

  def __isub__(self, other: Iterable) -> Vector2f:
    self = self.__sub__(other)
    return self

  def __iadd__(self, other: Iterable) -> Vector2f:
    self = self.__add__(other)
    return self

  def __imul__(self, other: Union[Iterable, float]) -> Vector2f:
    self = self.__mul__(other)
    return self

  def __idiv__(self, other: Union[Iterable, float]) -> Vector2f:
    self = self.__div__(other)
    return self

  def __ifloordiv__(self, other: Union[Iterable, float]) -> Vector2f:
    self = self.__floordiv__(other)
    return self

  def __imod__(self, other: Union[Iterable, float]) -> Vector2f:
    self = self.__mod__(other)
    return self

  def __ipow__(self, n: float) -> Vector2f:
    self = self.__pow__(n)
    return self

  def __irshift__(self, other: Union[Iterable, float]) -> Vector2f:
    self = self.__rshift__(other)
    return self

  def __ilshift__(self, other: Union[Iterable, float]) -> Vector2f:
    self = self.__lshift__(other)
    return self

  def asTuple(self) -> tuple:
    return tuple(self)

  def asStr(self) -> str:
    return str(self)

  @staticmethod
  def _make(i: Iterable) -> Vector2f:
    return Vector2f(float(i[0]), float(i[1]))
