# STL-IMPORT
from abc import ABC, abstractmethod
from typing import Any, Dict, NamedTuple

# LIBRARY-IMPORT
import pygame as pg

# LOCAL-IMPORT
from beans.types import SingletonMeta, Vector2f, classname
from game import Level, LevelManager, LevelState


##
# CommandResult; FinalStruct for Result of executed Command
#
# @param  id    id of parent-command
# @param  data  returned data of command
#
class CommandResult(NamedTuple):
  id_: int
  data: Any


##
# Command; GoF Command-Pattern
#
# @extends  abc.ABC
#
# @param  id    numeric id of command (set by frontend, for identification of reply)
# @param  args  dict of commands, somewhat like 'kwargs'
#
class Command(ABC):

  id_: int
  args: Dict[str, Any]

  def __init__(self, id_: int, args: Dict[str, Any]) -> None:
    self.id_ = id_
    self.args = args

  ##
  # abstract function 'execute' for specifing the execution of a given command. MUST be
  # overwritten by child-class.
  #
  # @return   result and id of execution
  #
  @abstractmethod
  def execute(self) -> CommandResult:
    raise NotImplementedError()


class KarelMoveCommand(Command):

  def execute(self) -> CommandResult:
    try:
      level = LevelManager().getCurrentLevel()
      level.waitOnStart()
      level.karelMove()
      return CommandResult(self.id_, None)
    except RuntimeError as err:
      return CommandResult(self.id_, classname(err))


class KarelTurnLeftCommand(Command):

  def execute(self) -> CommandResult:
    try:
      level = LevelManager().getCurrentLevel()
      level.waitOnStart()
      level.karelTurnLeft()
      return CommandResult(self.id_, None)
    except RuntimeError as err:
      return CommandResult(self.id_, classname(err))


class KarelPickBeeperCommand(Command):

  def execute(self) -> CommandResult:
    try:
      level = LevelManager().getCurrentLevel()
      level.waitOnStart()
      level.karelPickBeeper()
      return CommandResult(self.id_, None)
    except RuntimeError as err:
      return CommandResult(self.id_, classname(err))


class KarelPutBeeperCommand(Command):

  def execute(self) -> CommandResult:
    try:
      level = LevelManager().getCurrentLevel()
      level.waitOnStart()
      level.karelPutBeeper()
      return CommandResult(self.id_, None)
    except RuntimeError as err:
      return CommandResult(self.id_, classname(err))


class KarelFrontIsClearCommand(Command):

  def execute(self) -> CommandResult:
    try:
      level = LevelManager().getCurrentLevel()
      level.waitOnStart()
      result = level.karelFrontIsClear()
      return CommandResult(self.id_, result)
    except RuntimeError as err:
      return CommandResult(self.id_, classname(err))


class KarelRightIsClearCommand(Command):

  def execute(self) -> CommandResult:
    try:
      level = LevelManager().getCurrentLevel()
      level.waitOnStart()
      result = level.karelRightIsClear()
      return CommandResult(self.id_, result)
    except RuntimeError as err:
      return CommandResult(self.id_, classname(err))


class KarelLeftIsClearCommand(Command):

  def execute(self) -> CommandResult:
    try:
      level = LevelManager().getCurrentLevel()
      level.waitOnStart()
      result = level.karelLeftIsClear()
      return CommandResult(self.id_, result)
    except RuntimeError as err:
      return CommandResult(self.id_, classname(err))


class KarelBeeperInBagCommand(Command):

  def execute(self) -> CommandResult:
    try:
      level = LevelManager().getCurrentLevel()
      level.waitOnStart()
      result = level.karelBeeperInBag()
      return CommandResult(self.id_, result)
    except RuntimeError as err:
      return CommandResult(self.id_, classname(err))


class KarelBeeperPresentCommand(Command):

  def execute(self) -> CommandResult:
    try:
      level = LevelManager().getCurrentLevel()
      level.waitOnStart()
      result = level.karelBeeperPresent()
      return CommandResult(self.id_, result)
    except RuntimeError as err:
      return CommandResult(self.id_, classname(err))


class KarelFacingNorthCommand(Command):

  def execute(self) -> CommandResult:
    try:
      level = LevelManager().getCurrentLevel()
      level.waitOnStart()
      result = level.karelFacingNorth()
      return CommandResult(self.id_, result)
    except RuntimeError as err:
      return CommandResult(self.id_, classname(err))


class KarelFacingEastCommand(Command):

  def execute(self) -> CommandResult:
    try:
      level = LevelManager().getCurrentLevel()
      level.waitOnStart()
      result = level.karelFacingEast()
      return CommandResult(self.id_, result)
    except RuntimeError as err:
      return CommandResult(self.id_, classname(err))


class KarelFacingSouthCommand(Command):

  def execute(self) -> CommandResult:
    try:
      level = LevelManager().getCurrentLevel()
      level.waitOnStart()
      result = level.karelFacingSouth()
      return CommandResult(self.id_, result)
    except RuntimeError as err:
      return CommandResult(self.id_, classname(err))


class KarelFacingWestCommand(Command):

  def execute(self) -> CommandResult:
    try:
      level = LevelManager().getCurrentLevel()
      level.waitOnStart()
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