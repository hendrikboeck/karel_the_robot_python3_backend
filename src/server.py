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
import threading
import errno
from socket import error as SocketError
from socket import AF_INET, SOCK_DGRAM, SOCK_STREAM, socket
from typing import NamedTuple, Tuple, Union
import atexit

# LOCAL IMPORT
import rpc
from pyadditions.types import Interface, NotInstanceable, interfacemethod
from pyadditions.io import IOM
from constants import UTF8, MAX_CONNECTIONS, UDP_MAX_PKG_SIZE, TCP_MAX_PKG_SIZE
from view.window import DebugInformationDict


class SocketAddr(NamedTuple):
  """
  Describes a socket-addr; Can be a server- or cient-addr.

  @param  ip    ip/dns of server/client
  @param  port  port of socket
  """

  ip: str
  port: int

  def __str__(self) -> str:
    return f"{self.ip}:{self.port}"

  @staticmethod
  def toStr(addr: SocketAddr) -> str:
    """
    Returns a given SocketAddr to String. SocketAddr can be None.

    @param  addr  SocketAddr that should be returned
    @return       String as "{ip/dns}:{port}"
    """
    if addr is None:
      return "none:none"
    else:
      return str(addr)

  @staticmethod
  def fromStr(addr: str) -> SocketAddr:
    """
    Generates a SocketAddr from a String.

    @param  addr  SocketAddr as String as "{ip/dns}:{port}"
    @return       coresponding SocketAddr
    """
    addr = addr.split(":")
    return SocketAddr(str(addr[0]), int(addr[1]))

  def isBound(self) -> bool:
    """
    Checks if a given SocketAddr is already bound to application. Can be used
    to check if a SocketAddr is already taken.

    @return   True is SocketAddr is already bound
    """
    bound = True
    sock = socket(AF_INET, SOCK_STREAM)
    try:
      sock.bind(self)
      bound = False
    except SocketError as e:
      if e.errno == errno.EADDRINUSE:
        IOM.error("socket-address already in use")
      else:
        IOM.error("other SocketError: " + e)
    sock.close()
    return bound


class IServerInterface(Interface):

  @interfacemethod
  def start(self) -> None:
    raise NotImplementedError

  @interfacemethod
  def stop(self) -> None:
    raise NotImplementedError

  @interfacemethod
  def recv(self) -> Tuple[str, Union[SocketAddr, None]]:
    raise NotImplementedError

  @interfacemethod
  def send(self, data: str, addr: SocketAddr = None) -> None:
    raise NotImplementedError


class UDPServerINET(IServerInterface):

  sock: socket
  addr: SocketAddr

  def __init__(self, addr: str) -> None:
    self.addr = SocketAddr.fromStr(addr)
    self.sock = socket(AF_INET, SOCK_DGRAM)
    self.sock.bind(self.addr)
    DebugInformationDict().update(
        SERVER_ADDR=f"udp://{self.addr}", SERVER_STATUS="up"
    )
    IOM.out(f"server started at udp://{self.addr}")

  def start(self) -> None:
    pass

  def stop(self) -> None:
    self.sock.close()
    IOM.out(f"server stopped at udp://{self.addr}")
    DebugInformationDict().update(SERVER_STATUS="down")
    del self

  def recv(self) -> Tuple[str, Union[SocketAddr, None]]:
    try:
      (data, addr) = self.sock.recvfrom(UDP_MAX_PKG_SIZE)
      data = data.decode(UTF8)
      addr = SocketAddr._make(addr)
      IOM.debug(f"RECV udp://{self.addr} <- {addr}: {data}")
      return (data, addr)
    except:
      IOM.error(
          f"udp://{self.addr}: could not recv data; client not found or invalid"
      )
      return (None, None)

  def send(self, data: str, addr: SocketAddr = None) -> None:
    try:
      if addr is None:
        raise ConnectionError()
      self.sock.sendto(data.encode(UTF8), addr)
      IOM.debug(f"SEND udp://{self.addr} -> {addr}: {data}")
    except:
      IOM.error(
          f"udp://{self.addr}: could not send data; client {addr} not found or invalid"
      )


class TCPServerINET(IServerInterface):

  sock: socket
  addr: SocketAddr
  clientSock: socket
  clientAddr: SocketAddr
  _sockErrCount: int

  def __init__(self, addr: str) -> None:
    self.sock = socket(AF_INET, SOCK_STREAM)
    self.addr = SocketAddr.fromStr(addr)
    self.sock.bind(self.addr)
    self.clientSock = None
    self.clientAddr = None
    self._sockErrCount = 0
    DebugInformationDict().update(
        SERVER_ADDR=f"tcp://{self.addr}", SERVER_STATUS="down"
    )

  def start(self) -> None:
    self.sock.listen(MAX_CONNECTIONS)
    DebugInformationDict().update(SERVER_STATUS="up")
    IOM.out(f"server started at tcp://{self.addr}")

  def stop(self) -> None:
    self._disconnectClient()
    self.sock.close()
    DebugInformationDict().update(SERVER_STATUS="down")
    IOM.out(f"server stopped at tcp://{self.addr}")
    del self

  def _disconnectClient(self) -> None:
    try:
      self.clientSock.close()
      IOM.debug(f"disconnected client {self.clientAddr}")
    except:
      pass
    self.clientSock = None
    self.clientAddr = None

  def _renewClient(self) -> None:
    try:
      self._disconnectClient()
      (sock, addr) = self.sock.accept()
      self.clientSock = sock
      self.clientAddr = SocketAddr._make(addr)
    except:
      pass

  def recv(self) -> Tuple[str, Union[SocketAddr, None]]:
    try:
      data = self.clientSock.recv(TCP_MAX_PKG_SIZE)
      data = data.decode(UTF8)
      if data == "":
        self._disconnectClient()
        return self.recv()
      else:
        IOM.debug(f"RECV tcp://{self.addr} <- {self.clientAddr}: {data}")
        self._sockErrCount = 0
        return (data, None)
    except:
      if self._sockErrCount > 0:
        IOM.error(
            f"tcp://{self.addr}: could not recv data; client {self.clientAddr} not found or invalid"
        )
        return (None, None)
      else:
        self._renewClient()
        self._sockErrCount = 1
        return self.recv()

  def send(self, data: str, addr: SocketAddr = None) -> None:
    try:
      if addr is None or addr == self.clientAddr:
        self.clientSock.sendall(data.encode(UTF8))
        IOM.debug(f"SEND tcp://{self.addr} -> {self.clientAddr}: {data}")
      else:
        raise ConnectionError()
    except:
      IOM.error(
          f"tcp://{self.addr}: could not send data; client {addr} not found or invalid"
      )


class ServerFactory(NotInstanceable):

  @staticmethod
  def create(protocol: str, port: int) -> IServerInterface:

    if protocol == "tcp":
      return TCPServerINET(f"localhost:{port}")
    elif protocol == "udp":
      return UDPServerINET(f"localhost:{port}")
    else:
      # Program should break here, if unkown protocol
      raise RuntimeError(f"unkown protocol type: '{protocol}'")


class ServerThread(threading.Thread):

  _server: IServerInterface

  def __init__(self, protocol: str, port: int) -> None:
    super().__init__(daemon=True)
    self._server = ServerFactory.create(protocol, port)

  def run(self) -> None:
    self._server.start()
    atexit.register(self._server.stop)

    running = True
    while running:
      (data, sender) = self._server.recv()
      if data:
        command = rpc.createCommandFromStr(data)
        resultStr = rpc.createRPCStrFromCommandResult(command.execute())
        self._server.send(resultStr, sender)
      else:
        running = False
