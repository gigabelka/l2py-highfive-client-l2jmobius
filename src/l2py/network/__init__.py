# -*- coding: utf-8 -*-
"""Сетевой слой l2py.

Содержит классы для TCP-соединений с Login и Game серверами.
"""

from l2py.network.game_connection import GameConnection
from l2py.network.login_connection import LoginConnection

__all__ = [
    "LoginConnection",
    "GameConnection",
]
