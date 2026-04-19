"""Regression guard for WS packet tracking: envelope must be broadcast and
ApiState.last_user_info must stay populated (routes.py depends on it)."""

from __future__ import annotations

import asyncio
from typing import Any

import pytest

from l2py.api.state import ApiState
from l2py.api.ws import _broadcast, _track_self_and_target, register_subscribers
from l2py.events import PacketReceivedEvent
from l2py.protocol.base import PacketWriter
from l2py.protocol.game.server_packets import UserInfoPacket


def _user_info_bytes() -> bytes:
    w = PacketWriter()
    w.write_int32(100)  # x
    w.write_int32(200)  # y
    w.write_int32(-50)  # z
    w.write_int32(0)  # heading
    w.write_int32(42)  # object_id
    w.write_string("tester")
    w.write_int32(0)  # race
    w.write_int32(1)  # sex
    w.write_int32(10)  # class_id
    w.write_int32(20)  # level
    w.write_int64(9999)  # exp
    for val in (1, 2, 3, 4, 5, 6):
        w.write_int32(val)
    for val in (500, 400, 300, 200):  # max_hp, cur_hp, max_mp, cur_mp
        w.write_int32(val)
    w.write_int32(77)  # sp
    w.write_int32(111)  # cur_load
    w.write_int32(999)  # max_load
    w.write_int32(0)  # active_weapon_item
    return w.to_bytes()


class FakeWebSocket:
    """Minimal async duck-typed WebSocket that captures JSON sends."""

    def __init__(self) -> None:
        self.sent: list[dict[str, Any]] = []

    async def send_json(self, payload: dict[str, Any]) -> None:
        self.sent.append(payload)


@pytest.mark.asyncio
async def test_broadcast_emits_parsed_envelope():
    state = ApiState()
    ws = FakeWebSocket()
    state.ws_clients.add(ws)  # type: ignore[arg-type]

    event = PacketReceivedEvent(
        opcode=UserInfoPacket.opcode, data=_user_info_bytes(), source="game"
    )
    await _broadcast(state, event)

    assert len(ws.sent) == 1
    payload = ws.sent[0]
    assert payload["opcode"] == "0x32"
    assert payload["name"] == "UserInfo"
    assert payload["source"] == "game"
    assert payload["parsed"]["object_id"] == 42
    assert payload["parsed"]["name"] == "tester"


def test_track_self_and_target_populates_last_user_info():
    state = ApiState()
    event = PacketReceivedEvent(
        opcode=UserInfoPacket.opcode, data=_user_info_bytes(), source="game"
    )
    _track_self_and_target(state, event)

    assert state.self_object_id == 42
    assert state.self_x == 100
    assert state.last_user_info is not None
    assert state.last_user_info["name"] == "tester"
    assert state.last_user_info["max_hp"] == 500
    assert state.last_user_info["sp"] == 77


@pytest.mark.asyncio
async def test_subscriber_pipeline_tracks_and_broadcasts():
    state = ApiState()
    ws = FakeWebSocket()
    state.ws_clients.add(ws)  # type: ignore[arg-type]
    register_subscribers(state)

    await state.emitter.emit(
        PacketReceivedEvent(
            opcode=UserInfoPacket.opcode, data=_user_info_bytes(), source="game"
        )
    )

    # allow any pending callbacks to complete
    await asyncio.sleep(0)

    assert state.self_object_id == 42
    assert state.last_user_info is not None
    assert ws.sent and ws.sent[0]["name"] == "UserInfo"
