# -*- coding: utf-8 -*-
"""Пакеты протокола Login Server.

Все пакеты для общения с Login Server (порт 2106).
"""

from l2py.protocol.login.client_packets import (
    AuthGameGuardPacket,
    RequestAuthLoginPacket,
    RequestServerListPacket,
    RequestServerLoginPacket,
)
from l2py.protocol.login.server_packets import (
    GGAuthPacket,
    InitPacket,
    LoginFailPacket,
    LoginOkPacket,
    PlayOkPacket,
    ServerListPacket,
)

__all__ = [
    # Client packets
    "AuthGameGuardPacket",
    "RequestAuthLoginPacket",
    "RequestServerListPacket",
    "RequestServerLoginPacket",
    # Server packets
    "InitPacket",
    "GGAuthPacket",
    "LoginOkPacket",
    "ServerListPacket",
    "PlayOkPacket",
    "LoginFailPacket",
]
