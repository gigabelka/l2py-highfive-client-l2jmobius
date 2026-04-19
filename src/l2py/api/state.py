"""Shared state for the external API server.

Хранит ссылку на текущий `GameSession`, кэш координат персонажа и последнего
выбранного objectId (нужны для AttackRequest / Action). Также держит множество
активных WebSocket-клиентов.
"""

from __future__ import annotations

import asyncio
from dataclasses import dataclass, field
from typing import TYPE_CHECKING, Any

from l2py.events import EventEmitter

if TYPE_CHECKING:
    from fastapi import WebSocket

    from l2py.network.game_flow import GameSession


@dataclass
class NpcRecord:
    """Кэш одной видимой NPC-сущности (из NpcInfo 0x16)."""

    object_id: int
    template_id: int
    x: int
    y: int
    z: int
    attackable: bool


@dataclass
class ApiState:
    """Mutable runtime state shared across API handlers."""

    session: "GameSession | None" = None
    emitter: EventEmitter = field(default_factory=EventEmitter)

    self_object_id: int | None = None
    self_x: int | None = None
    self_y: int | None = None
    self_z: int | None = None
    last_target_object_id: int | None = None

    # Карта action-bar: encoded_slot (slot + page*12) -> (type, id, level).
    # type: 1=ITEM, 2=SKILL, 3=ACTION, 4=MACRO, 5=RECIPE, 6=BOOKMARK.
    shortcuts: dict[int, tuple[int, int, int]] = field(default_factory=dict)

    # Видимые NPC: object_id -> NpcRecord. Обновляется из NpcInfo/DeleteObject.
    visible_npcs: dict[int, NpcRecord] = field(default_factory=dict)

    # Снимок последнего UserInfo (все распарсенные поля).
    last_user_info: dict[str, Any] | None = None
    # attr_id -> value из последних StatusUpdate для self_object_id.
    stats: dict[int, int] = field(default_factory=dict)
    # object_id -> item record (см. docs/INVENTORY.md §On-wire item record).
    inventory: dict[int, dict[str, Any]] = field(default_factory=dict)
    # Скиллы из SkillList (0x5F).
    skills: list[dict[str, Any]] = field(default_factory=list)

    # Синхронизация ожидания подтверждения MyTargetSelected для next-target.
    target_confirm_event: asyncio.Event = field(default_factory=asyncio.Event)
    target_confirm_expected_id: int | None = None

    # Диагностика: количество раз, что клиент видел каждый opcode (debug).
    opcode_counts: dict[int, int] = field(default_factory=dict)
    # Последние 20 пакетов (opcode, hex-body) для диагностики.
    recent_packets: list[tuple[int, str]] = field(default_factory=list)

    ws_clients: set["WebSocket"] = field(default_factory=set)

    def self_position(self) -> tuple[int, int, int] | None:
        if self.self_x is None or self.self_y is None or self.self_z is None:
            return None
        return (self.self_x, self.self_y, self.self_z)


__all__ = ["ApiState", "NpcRecord"]
