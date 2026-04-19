"""Pydantic-схемы запросов и ответов внешнего API."""

from __future__ import annotations

from pydantic import BaseModel


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


class TargetIdResponse(BaseModel):
    id: int | None = None


__all__ = [
    "StatusResponse",
    "SendResult",
    "TargetIdResponse",
]
