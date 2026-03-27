# -*- coding: utf-8 -*-
"""Модели для игровых серверов."""

from dataclasses import dataclass


@dataclass(frozen=True, slots=True)
class GameServer:
    """Информация об игровом сервере.

    Attributes:
        id: ID сервера.
        ip: IP-адрес сервера.
        port: Порт для подключения.
        online: Текущее количество игроков.
        max_online: Максимальное количество игроков.
        status: Статус сервера (True = доступен).
        is_pvp: Является ли сервер PvP.
        age_limit: Ограничение по возрасту.
    """

    id: int
    ip: str
    port: int
    online: int
    max_online: int
    status: bool = True
    is_pvp: bool = False
    age_limit: bool = False


__all__ = ["GameServer"]
