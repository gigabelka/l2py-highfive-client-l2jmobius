# -*- coding: utf-8 -*-
"""Конфигурационные модели для l2py клиента.

Используются стандартные dataclasses без внешних зависимостей
для валидации конфигурации подключения к L2 серверу.
"""

from dataclasses import dataclass


@dataclass(frozen=True, slots=True)
class LoginConfig:
    """Конфигурация подключения к Login Server.

    Attributes:
        host: IP-адрес или hostname Login Server.
        port: Порт для подключения (по умолчанию 2106).
    """

    host: str
    port: int = 2106


@dataclass(frozen=True, slots=True)
class Credentials:
    """Учётные данные для авторизации.

    Attributes:
        username: Логин аккаунта.
        password: Пароль аккаунта.
    """

    username: str
    password: str


@dataclass(frozen=True, slots=True)
class ConnectionConfig:
    """Конфигурация выбора сервера и персонажа.

    Attributes:
        server_id: ID игрового сервера (по умолчанию 1).
        char_slot: Индекс слота персонажа (по умолчанию 0).
    """

    server_id: int = 1
    char_slot: int = 0


__all__ = [
    "LoginConfig",
    "Credentials",
    "ConnectionConfig",
]
