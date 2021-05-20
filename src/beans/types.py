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
  if isinstance(val, list): return val
  else: return [val]


def classname(obj: object) -> str:
  return obj.__class__.__name__


def defaultOnError(func: function, alt_val: Any) -> Any:
  try:
    return func()
  except:
    return alt_val


def defaultOnNone(val: Any, alt_val: Any) -> Any:
  return val or alt_val


InterfaceMeta = ABCMeta
Interface = ABC
interfacemethod = abstractmethod


class EnumLikeMeta(type):

  def __call__(cls, *args: List[Any], **kwargs: Dict[str, Any]) -> Any:
    raise TypeError(f"{cls.__module__}.{cls.__qualname__} has no public constructor")


class EnumLike(metaclass=EnumLikeMeta):
  pass


class SingletonMeta(type):

  _instances: dict = {}

  def __call__(cls, *args, **kwargs):
    if not cls._instances.get(cls):
      cls._instances[cls] = super(SingletonMeta, cls).__call__(*args, **kwargs)
    return cls._instances.get(cls)


class SingletonFactoryMeta(type):

  _instances: dict = {}

  def __call__(cls, *args: Any, **kwargs: Any) -> Any:
    if not cls._instances.get(args[0]):
      cls._instances[args[0]] = \
        super(SingletonFactoryMeta, cls).__call__(*args, **kwargs)
    return cls._instances.get(args[0])


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
