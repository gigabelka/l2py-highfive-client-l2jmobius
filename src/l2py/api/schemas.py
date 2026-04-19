"""Pydantic-схемы запросов и ответов внешнего API."""

from __future__ import annotations

from typing import Any

from pydantic import BaseModel, Field


class ItemView(BaseModel):
    object_id: int
    item_id: int
    count: int
    location: int = 0
    equipped: bool = False
    body_part: int = 0
    enchant: int = 0
    type2: int = 0
    augmentation_id: int = 0
    mana: int = -1
    time: int = -9999
    attack_element_type: int = -2
    attack_element_power: int = 0
    def_element: list[int] = Field(default_factory=list)


class SkillView(BaseModel):
    id: int
    level: int
    passive: bool = False
    disabled: bool = False


class ShortcutView(BaseModel):
    slot: int
    type: int
    id: int
    level: int


class StatusResponse(BaseModel):
    connected: bool
    char_name: str | None = None
    object_id: int | None = None
    x: int | None = None
    y: int | None = None
    z: int | None = None
    last_target_id: int | None = None

    user_info: dict[str, Any] | None = None
    stats: dict[int, int] = Field(default_factory=dict)
    inventory: list[ItemView] = Field(default_factory=list)
    skills: list[SkillView] = Field(default_factory=list)
    shortcuts: list[ShortcutView] = Field(default_factory=list)


class SendResult(BaseModel):
    ok: bool = True
    opcode: str
    description: str | None = None


class TargetIdResponse(BaseModel):
    id: int | None = None


__all__ = [
    "StatusResponse",
    "SendResult",
    "TargetIdResponse",
    "ItemView",
    "SkillView",
    "ShortcutView",
]
