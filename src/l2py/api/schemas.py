"""Pydantic-схемы запросов и ответов внешнего API."""

from __future__ import annotations

from typing import Literal

from pydantic import BaseModel, Field


class SitStandRequest(BaseModel):
    ctrl: bool = False
    shift: bool = False


class AttackBody(BaseModel):
    object_id: int = Field(..., description="objectId цели")
    shift: bool = Field(False, description="Shift-click: forced attack")


class ObjectIdBody(BaseModel):
    object_id: int = Field(..., description="objectId цели/предмета на земле")


class ShortcutBody(BaseModel):
    type: Literal["ACTION", "SKILL", "ITEM"] = Field(
        ..., description="Тип ячейки быстрого доступа"
    )
    id: int = Field(..., description="action_id / skill_id / objectId предмета")
    ctrl: bool = False
    shift: bool = False


class StatusResponse(BaseModel):
    connected: bool
    char_name: str | None = None
    object_id: int | None = None
    x: int | None = None
    y: int | None = None
    z: int | None = None
    last_target_id: int | None = None


class SendResult(BaseModel):
    ok: bool = True
    opcode: str
    description: str | None = None


__all__ = [
    "SitStandRequest",
    "AttackBody",
    "ObjectIdBody",
    "ShortcutBody",
    "StatusResponse",
    "SendResult",
]
