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
from abc import ABC, abstractmethod
from typing import Any, Dict, NamedTuple

# LIBRARY-IMPORT
import pygame as pg

# LOCAL-IMPORT
from beans.types import SingletonMeta, Vector2f, classname
from game import Level, LevelManager, LevelState
from view.scene import GameScene, SceneManager


class CommandResult(NamedTuple):
  """
  Describes a result for a command

  @extends  NamedTuple
 
  @param  id_   id of parent-command
  @param  data  returned data of command
  """

  id_: int
  data: Any


class Command(ABC):
  """
  GoF Command-Pattern, that describes a Command to executed over the pipe.

  @extends  abc.ABC

  @param  id_   numeric id of command (set by frontend, for identification of
    reply)
  @param  args  dict of commands, somewhat like 'kwargs'
  """

  id_: int
  args: Dict[str, Any]

  def __init__(self, id_: int, args: Dict[str, Any]) -> None:
    self.id_ = id_
    self.args = args

  @abstractmethod
  def execute(self) -> CommandResult:
    """
    abstract function 'execute' for specifing the execution of a given command.
    MUST be overwritten by child-class.

    @return   result and id of execution
    """
    raise NotImplementedError()


class KarelMoveCommand(Command):

  def execute(self) -> CommandResult:
    try:
      level = LevelManager().getCurrentLevel()
      level.waitOnRunning()
      level.karelMove()
      level.pause()
      return CommandResult(self.id_, None)
    except RuntimeError as err:
      return CommandResult(self.id_, classname(err))


class KarelTurnLeftCommand(Command):

  def execute(self) -> CommandResult:
    try:
      level = LevelManager().getCurrentLevel()
      level.waitOnRunning()
      level.karelTurnLeft()
      level.pause()
      return CommandResult(self.id_, None)
    except RuntimeError as err:
      return CommandResult(self.id_, classname(err))


class KarelPickBeeperCommand(Command):

  def execute(self) -> CommandResult:
    try:
      level = LevelManager().getCurrentLevel()
      level.waitOnRunning()
      level.karelPickBeeper()
      level.pause()
      return CommandResult(self.id_, None)
    except RuntimeError as err:
      return CommandResult(self.id_, classname(err))


class KarelPutBeeperCommand(Command):

  def execute(self) -> CommandResult:
    try:
      level = LevelManager().getCurrentLevel()
      level.waitOnRunning()
      level.karelPutBeeper()
      level.pause()
      return CommandResult(self.id_, None)
    except RuntimeError as err:
      return CommandResult(self.id_, classname(err))


class KarelFrontIsClearCommand(Command):

  def execute(self) -> CommandResult:
    try:
      level = LevelManager().getCurrentLevel()
      level.waitOnRunning()
      result = level.karelFrontIsClear()
      return CommandResult(self.id_, result)
    except RuntimeError as err:
      return CommandResult(self.id_, classname(err))


class KarelRightIsClearCommand(Command):

  def execute(self) -> CommandResult:
    try:
      level = LevelManager().getCurrentLevel()
      level.waitOnRunning()
      result = level.karelRightIsClear()
      return CommandResult(self.id_, result)
    except RuntimeError as err:
      return CommandResult(self.id_, classname(err))


class KarelLeftIsClearCommand(Command):

  def execute(self) -> CommandResult:
    try:
      level = LevelManager().getCurrentLevel()
      level.waitOnRunning()
      result = level.karelLeftIsClear()
      return CommandResult(self.id_, result)
    except RuntimeError as err:
      return CommandResult(self.id_, classname(err))


class KarelBeeperInBagCommand(Command):

  def execute(self) -> CommandResult:
    try:
      level = LevelManager().getCurrentLevel()
      level.waitOnRunning()
      result = level.karelBeeperInBag()
      return CommandResult(self.id_, result)
    except RuntimeError as err:
      return CommandResult(self.id_, classname(err))


class KarelBeeperPresentCommand(Command):

  def execute(self) -> CommandResult:
    try:
      level = LevelManager().getCurrentLevel()
      level.waitOnRunning()
      result = level.karelBeeperPresent()
      return CommandResult(self.id_, result)
    except RuntimeError as err:
      return CommandResult(self.id_, classname(err))


class KarelFacingNorthCommand(Command):

  def execute(self) -> CommandResult:
    try:
      level = LevelManager().getCurrentLevel()
      level.waitOnRunning()
      result = level.karelFacingNorth()
      return CommandResult(self.id_, result)
    except RuntimeError as err:
      return CommandResult(self.id_, classname(err))


class KarelFacingEastCommand(Command):

  def execute(self) -> CommandResult:
    try:
      level = LevelManager().getCurrentLevel()
      level.waitOnRunning()
      result = level.karelFacingEast()
      return CommandResult(self.id_, result)
    except RuntimeError as err:
      return CommandResult(self.id_, classname(err))


class KarelFacingSouthCommand(Command):

  def execute(self) -> CommandResult:
    try:
      level = LevelManager().getCurrentLevel()
      level.waitOnRunning()
      result = level.karelFacingSouth()
      return CommandResult(self.id_, result)
    except RuntimeError as err:
      return CommandResult(self.id_, classname(err))


class KarelFacingWestCommand(Command):

  def execute(self) -> CommandResult:
    try:
      level = LevelManager().getCurrentLevel()
      level.waitOnRunning()
      result = level.karelFacingWest()
      return CommandResult(self.id_, result)
    except RuntimeError as err:
      return CommandResult(self.id_, classname(err))


class GameLoadWorldCommand(Command):

  def execute(self) -> CommandResult:
    try:
      bounds = Vector2f._make(pg.display.get_surface().get_size())
      bounds.x -= 320
      bounds.y -= 20
      LevelManager().setCurrentLevel(Level(self.args["map"], bounds))
      SceneManager().setScene(GameScene())
      return CommandResult(self.id_, None)
    except RuntimeError as err:
      return CommandResult(self.id_, classname(err))


class GameCloseCommand(Command):

  def execute(self) -> CommandResult:
    LevelManager().getCurrentLevel()._changeLevelState(LevelState.FINISHED)
    return CommandResult(self.id_, None)


##
# CommandFactory
#
# @extends beans.types.SingletonMeta
#
# @param  COMMAND_TABLE   Map of API-names to Command-child-classes
#
class CommandFactory(metaclass=SingletonMeta):

  COMMAND_TABLE: Dict[str, Command] = {
      "move": KarelMoveCommand,
      "turnLeft": KarelTurnLeftCommand,
      "pickBeeper": KarelPickBeeperCommand,
      "putBeeper": KarelPutBeeperCommand,
      "frontIsClear": KarelFrontIsClearCommand,
      "rightIsClear": KarelRightIsClearCommand,
      "leftIsClear": KarelLeftIsClearCommand,
      "beeperInBag": KarelBeeperInBagCommand,
      "beeperPresent": KarelBeeperPresentCommand,
      "facingNorth": KarelFacingNorthCommand,
      "facingEast": KarelFacingEastCommand,
      "facingSouth": KarelFacingSouthCommand,
      "facingWest": KarelFacingWestCommand,
      "loadWorld": GameLoadWorldCommand,
      "close": GameCloseCommand
  }

  def create(
      self, functionName: str, id_: int, args: Dict[str, Any]
  ) -> Command:
    return self.COMMAND_TABLE[functionName](id_, args)
