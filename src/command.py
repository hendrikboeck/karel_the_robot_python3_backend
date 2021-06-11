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

# LOCAL-IMPORT
from pyadditions.types import SingletonMeta, classname
from game import ActionExecutionError, Level, LevelManager, LevelState
from view.scene import GameScene, SceneManager
from constants import WINDOW_DIMENSIONS


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

  def pushErrorWindow(
      self, error: RuntimeError, problem: str, p_solution: str
  ) -> None:
    scene = SceneManager().getScene()
    if isinstance(scene, GameScene):
      scene.showErrorWindow(
          classname(error), f"<b>PROBLEM:</b><br/>{problem}<br/> <br/>"
          f"<b>POSSIBLE SOLUTION:</b><br/>{p_solution}"
      )


class KarelMoveCommand(Command):
  """
  is a Karel-Action. Makes Karel move 1 tile forward in the direction he is
  looking at. If Karel can not execute move a the name of Error is returned.

  @extends  Command
  """

  def execute(self) -> CommandResult:
    try:
      level = LevelManager().getCurrentLevel()
      level.waitOnRunning()
      level.karelMove()
      level.pause()
      return CommandResult(self.id_, None)
    except RuntimeError as err:
      if isinstance(err, ActionExecutionError):
        self.pushErrorWindow(
            err, "Karel hit a wall, while trying to <i>move</i>.",
            "Try to run function <i>frontIsClear</i> before moving. The result "
            "of this function will tell you, if Karel can <i>move</i>."
        )
      return CommandResult(self.id_, classname(err))


class KarelTurnLeftCommand(Command):
  """
  is a Karel-Action. Makes Karel turn left. If Karel can not execute turnLeft a
  the name of Error is returned.

  @extends  Command
  """

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
  """
  is a Karel-Action. Makes Karel pick a beeper from current position. If Karel
  can not execute pickBeeper the name of Error is returned.

  @extends  Command
  """

  def execute(self) -> CommandResult:
    try:
      level = LevelManager().getCurrentLevel()
      level.waitOnRunning()
      level.karelPickBeeper()
      level.pause()
      return CommandResult(self.id_, None)
    except RuntimeError as err:
      if isinstance(err, ActionExecutionError):
        self.pushErrorWindow(
            err,
            "Karel was not able to <i>pickPicker</i>, because no Beeper exists "
            "at Karels current position.",
            "Try to run function <i>beeperPresent</i> before picking a Beeper. "
            "The result of this function will tell you, if at least one Beeper "
            "is present at Karels current position."
        )
      return CommandResult(self.id_, classname(err))


class KarelPutBeeperCommand(Command):
  """
  is a Karel-Action. Makes Karel put a beeper at current position. If Karel can
  not execute putBeeper the name of Error is returned.

  @extends  Command
  """

  def execute(self) -> CommandResult:
    try:
      level = LevelManager().getCurrentLevel()
      level.waitOnRunning()
      level.karelPutBeeper()
      level.pause()
      return CommandResult(self.id_, None)
    except RuntimeError as err:
      if isinstance(err, ActionExecutionError):
        self.pushErrorWindow(
            err,
            "Karel was not able to <i>putPicker</i>, because Karel has no "
            "Beepers left in his bag.",
            "Try to run function <i>beeperInBag</i> before putting a Beeper. "
            "The result of this function will tell you, if at least one Beeper "
            "is left in Karels bag."
        )
      return CommandResult(self.id_, classname(err))


class KarelFrontIsClearCommand(Command):
  """
  is a Karel-Question. Returns wether there is a wall in front of Karel.

  @extends  Command
  """

  def execute(self) -> CommandResult:
    try:
      level = LevelManager().getCurrentLevel()
      level.waitOnRunning()
      result = level.karelFrontIsClear()
      return CommandResult(self.id_, result)
    except RuntimeError as err:
      return CommandResult(self.id_, classname(err))


class KarelRightIsClearCommand(Command):
  """
  is a Karel-Question. Returns wether there is a wall to the right of Karel.

  @extends  Command
  """

  def execute(self) -> CommandResult:
    try:
      level = LevelManager().getCurrentLevel()
      level.waitOnRunning()
      result = level.karelRightIsClear()
      return CommandResult(self.id_, result)
    except RuntimeError as err:
      return CommandResult(self.id_, classname(err))


class KarelLeftIsClearCommand(Command):
  """
  is a Karel-Question. Returns wether there is a wall to the left of Karel.

  @extends  Command
  """

  def execute(self) -> CommandResult:
    try:
      level = LevelManager().getCurrentLevel()
      level.waitOnRunning()
      result = level.karelLeftIsClear()
      return CommandResult(self.id_, result)
    except RuntimeError as err:
      return CommandResult(self.id_, classname(err))


class KarelBeeperInBagCommand(Command):
  """
  is a Karel-Question. Returns wether Karel has at least one beeper left in his
  bag.

  @extends  Command
  """

  def execute(self) -> CommandResult:
    try:
      level = LevelManager().getCurrentLevel()
      level.waitOnRunning()
      result = level.karelBeeperInBag()
      return CommandResult(self.id_, result)
    except RuntimeError as err:
      return CommandResult(self.id_, classname(err))


class KarelBeeperPresentCommand(Command):
  """
  is a Karel-Question. Returns wether at least one beeper is present on the
  position Karel is at.

  @extends  Command
  """

  def execute(self) -> CommandResult:
    try:
      level = LevelManager().getCurrentLevel()
      level.waitOnRunning()
      result = level.karelBeeperPresent()
      return CommandResult(self.id_, result)
    except RuntimeError as err:
      return CommandResult(self.id_, classname(err))


class KarelFacingNorthCommand(Command):
  """
  is a Karel-Question. Returns wether Karel is currently facing north.

  @extends  Command
  """

  def execute(self) -> CommandResult:
    try:
      level = LevelManager().getCurrentLevel()
      level.waitOnRunning()
      result = level.karelFacingNorth()
      return CommandResult(self.id_, result)
    except RuntimeError as err:
      return CommandResult(self.id_, classname(err))


class KarelFacingEastCommand(Command):
  """
  is a Karel-Question. Returns wether Karel is currently facing east.

  @extends  Command
  """

  def execute(self) -> CommandResult:
    try:
      level = LevelManager().getCurrentLevel()
      level.waitOnRunning()
      result = level.karelFacingEast()
      return CommandResult(self.id_, result)
    except RuntimeError as err:
      return CommandResult(self.id_, classname(err))


class KarelFacingSouthCommand(Command):
  """
  is a Karel-Question. Returns wether Karel is currently facing south.

  @extends  Command
  """

  def execute(self) -> CommandResult:
    try:
      level = LevelManager().getCurrentLevel()
      level.waitOnRunning()
      result = level.karelFacingSouth()
      return CommandResult(self.id_, result)
    except RuntimeError as err:
      return CommandResult(self.id_, classname(err))


class KarelFacingWestCommand(Command):
  """
  is a Karel-Question. Returns wether Karel is currently facing west.

  @extends  Command
  """

  def execute(self) -> CommandResult:
    try:
      level = LevelManager().getCurrentLevel()
      level.waitOnRunning()
      result = level.karelFacingWest()
      return CommandResult(self.id_, result)
    except RuntimeError as err:
      return CommandResult(self.id_, classname(err))


class GameLoadWorldCommand(Command):
  """
  loads a mapname.xml file as World into the game. (mapname.xml can eighter be
  loaded from local file in assets/map/ or from a embedded maps in the exe).

  @extends  Command
  """

  def execute(self) -> CommandResult:
    try:
      bounds = WINDOW_DIMENSIONS - (320, 20)
      LevelManager().setCurrentLevel(Level(self.args["map"], bounds))
      SceneManager().setScene(GameScene())
      return CommandResult(self.id_, None)
    except RuntimeError as err:
      return CommandResult(self.id_, classname(err))


class GameCloseCommand(Command):
  """
  terminates command sequence for backend. Has to be called as last command in
  program.

  @extends  Command
  """

  def execute(self) -> CommandResult:
    LevelManager().getCurrentLevel()._changeLevelState(LevelState.FINISHED)
    return CommandResult(self.id_, None)


class CommandFactory(metaclass=SingletonMeta):
  """
  Factory-class for commands.

  @extends  SingletonMeta

  @param  COMMAND_TABLE   Map of API-names to Command-child-classes
  """

  COMMAND_TABLE: Dict[str, Command] = dict(
      move=KarelMoveCommand,
      turnLeft=KarelTurnLeftCommand,
      pickBeeper=KarelPickBeeperCommand,
      putBeeper=KarelPutBeeperCommand,
      frontIsClear=KarelFrontIsClearCommand,
      rightIsClear=KarelRightIsClearCommand,
      leftIsClear=KarelLeftIsClearCommand,
      beeperInBag=KarelBeeperInBagCommand,
      beeperPresent=KarelBeeperPresentCommand,
      facingNorth=KarelFacingNorthCommand,
      facingEast=KarelFacingEastCommand,
      facingSouth=KarelFacingSouthCommand,
      facingWest=KarelFacingWestCommand,
      loadWorld=GameLoadWorldCommand,
      EOS=GameCloseCommand
  )

  def create(
      self, functionName: str, id_: int, args: Dict[str, Any]
  ) -> Command:
    """
    creates a Command from functionName

    @param  functionName  name of function from API
    @param  id_           numeric id of command (set by frontend, for
      identification of reply)
    @param  args          arguments of command
    @return               corresporing Command
    """
    return self.COMMAND_TABLE[functionName](id_, args)
