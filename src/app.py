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

# LIBRARY IMPORT
from typing import Any, Dict
import yaml
import pygame as pg

# LOCAL IMPORT
from beans.sys import EXIT_FAILURE, errorExit, exit, fileExists
from beans.types import SingletonMeta
from beans.io import IOM, createIOManagerConfigFromDict, CLIColors
import assets
from constants import *
from view.menu import ClickButtonMenu
from view.overlay import FPSOverlay
from view.scene import SceneManager
from view.window import DebugWindow, DebugInformationDict
from server import ServerThread, SocketAddr


class App():
  """
  Wrapper for the 'main' function
  """

  @staticmethod
  def main(args: list) -> None:
    """
    The 'main' fuction of the program.
   
    @param  args  list of arguments from the commandline
    @return       None
    """
    conf = Configurator()
    if conf.socketAddr.isBound(): exit(EXIT_FAILURE)

    IOM.load(conf.iomConf)
    dinfo = DebugInformationDict()

    pg.init()
    IOM.debug("INITIALIZED pygame")

    serverThread = ServerThread(conf.socketProto, conf.socketAddr.port)
    serverThread.start()

    screen = pg.display.set_mode(tuple(WINDOW_DIMENSIONS), pg.DOUBLEBUF)
    pg.display.set_caption(WINDOW_TITLE)
    dinfo.update(WINDOW_SIZE=WINDOW_DIMENSIONS)
    IOM.debug(f"created window with dimensions {WINDOW_DIMENSIONS}")

    background = pg.Surface(tuple(WINDOW_DIMENSIONS))
    background.fill(SCREEN_BACKGROUND_COLOR)

    menuManager = assets.load.uimanager("theme/ClickButtonMenu.json")
    dWindow = DebugWindow(menuManager, True)
    dWindow.loadView("view/DebugWindow_default.xml")
    rmenu = ClickButtonMenu(menuManager, "view/ClickButtonMenu.xml")

    fpsoverlay = FPSOverlay(visible=False)

    gameloop = True
    clock = pg.time.Clock()

    # ----------------------------------------------------------------------------------------
    #                                  GAMELOOP START
    # ----------------------------------------------------------------------------------------

    while (gameloop):
      scene = SceneManager().getScene()
      frametime = clock.tick(conf.framerate)
      fps = clock.get_fps()

      for event in pg.event.get():
        if event.type == pg.QUIT:
          gameloop = False
          break
        menuManager.process_events(event)
        rmenu.process_event(event)
        fpsoverlay.proccessEvent(event)
        scene.proccessEvent(event)

      menuManager.update(frametime / 1000.0)
      scene.update(time_delta=frametime / 1000.0)
      fpsoverlay.update(fps)

      if dWindow.visible:
        dinfo.update(FPS=int(fps), FRAMETIME=frametime)

      if rmenu.getListItem("fps").check_pressed():
        fpsoverlay.toggle()
      if rmenu.getListItem("debugwin").check_pressed():
        dWindow.set_position(pg.mouse.get_pos())
        dWindow.toggle()

      screen.blit(background, (0, 0))
      scene.render(screen)
      menuManager.draw_ui(screen)
      fpsoverlay.render(screen)

      pg.display.flip()

    # ----------------------------------------------------------------------------------------
    #                                   GAMELOOP END
    # ----------------------------------------------------------------------------------------

    IOM.debug("EXIT gameloop")
    serverThread.join(0.1)


##
# Mapper for configuration file.  Used to store/set all configuration variables.
#
# @param  socket      socket configuration for server
# @param  undefined   dict of unmapped configurations
#
class Configurator(metaclass=SingletonMeta):

  socketProto: str
  socketAddr: SocketAddr
  iomConf: Dict[str, Any]
  framerate: int

  def __init__(self) -> None:
    filepath = CONFIGPATH + "yaml"
    if not fileExists(CONFIGPATH + "yaml"):
      filepath = CONFIGPATH + "yml"

    try:
      with open(filepath, 'r') as stream:
        conf = yaml.load(stream, Loader=yaml.FullLoader)

        # FRAMERATE
        self.framerate = int(conf.get("framerate", FRAMERATE))

        # IOM-Configuration
        iomConf = conf.get("iomanager", {})
        iomConf = createIOManagerConfigFromDict(iomConf)
        self.iomConf = iomConf

        # PYGAME_WARNINGS
        if not conf.get("pygame_show_warnings", False):
          import warnings
          warnings.filterwarnings("ignore")

        # SOCKET
        socketKey = conf.pop("socket", "tcp/1234")
        (self.socketProto, socketPort) = tuple(socketKey.split("/"))
        self.socketAddr = SocketAddr("localhost", int(socketPort)) 
    except FileNotFoundError as err:
      errorExit(str(err))
