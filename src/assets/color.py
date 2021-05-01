from pygame import Color


def HexColor(code: str) -> Color:
  return Color(code)


class Basics(object):
  WHITE = HexColor("#ffffff")
  BLACK = HexColor("#000000")
  RED = HexColor("#ff0000")
  GREEN = HexColor("#00ff00")
  BLUE = HexColor("#0000ff")
