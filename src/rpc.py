from typing import Any

import json

from command import Command, CommandResult, CommandFactory


def createCommandFromStr(data: str) -> Command:
  data = json.loads(data)
  return CommandFactory().create(
      functionName=data["function"], id=data["id"], args=data["args"]
  )


def createRPCStrFromCommandResult(res: CommandResult) -> str:

  return json.dumps({"id": res.id, "result": res.data})
