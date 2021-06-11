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
import json

# LOCAL IMPORT
from command import Command, CommandResult, CommandFactory


def createCommandFromStr(data: str) -> Command:
  """
  Creates a executable command form string received from RPC.

  @param  data  command fromated as string
  @result       command as executable Command
  """
  data = json.loads(data)
  return CommandFactory().create(
      functionName=data["function"], id_=data["id"], args=data["args"]
  )


def createRPCStrFromCommandResult(res: CommandResult) -> str:
  """
  Creates a string of RPC-Command.

  @param  res   result of a command
  @return       result as a string
  """
  return json.dumps({"id": res.id_, "result": res.data})
