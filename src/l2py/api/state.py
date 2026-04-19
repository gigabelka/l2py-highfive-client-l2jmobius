"""Shared state for the external API server.

Хранит ссылку на текущий `GameSession`, кэш координат персонажа и последнего
выбранного objectId (нужны для AttackRequest / Action). Также держит множество
активных WebSocket-клиентов.
"""

from __future__ import annotations

from dataclasses import dataclass, field
from typing import TYPE_CHECKING

from l2py.events import EventEmitter

if TYPE_CHECKING:
    from fastapi import WebSocket

    from l2py.network.game_flow import GameSession


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

    ws_clients: set["WebSocket"] = field(default_factory=set)

    def self_position(self) -> tuple[int, int, int] | None:
        if self.self_x is None or self.self_y is None or self.self_z is None:
            return None
        return (self.self_x, self.self_y, self.self_z)


__all__ = ["ApiState"]
