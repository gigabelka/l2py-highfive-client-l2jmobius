"""WebSocket-эндпоинт для стрима входящих игровых пакетов."""

from __future__ import annotations

import asyncio
import logging

from fastapi import APIRouter, WebSocket, WebSocketDisconnect

from l2py.api.state import ApiState
from l2py.events import PacketReceivedEvent
from l2py.protocol.game.server_packets import (
    MyTargetSelectedPacket,
    UserInfoPacket,
)

logger = logging.getLogger(__name__)

router = APIRouter()


async def _broadcast(state: ApiState, event: PacketReceivedEvent) -> None:
    """Рассылает событие всем подключённым WS-клиентам, дропает медленных."""
    if not state.ws_clients:
        return
    payload = {
        "opcode": f"0x{event.opcode:02X}",
        "hex": event.data.hex(),
        "len": len(event.data),
        "source": event.source,
    }
    dead: list[WebSocket] = []
    for ws in list(state.ws_clients):
        try:
            await asyncio.wait_for(ws.send_json(payload), timeout=1.0)
        except (asyncio.TimeoutError, WebSocketDisconnect, RuntimeError, Exception) as exc:
            logger.debug("Dropping slow/broken WS client: %r", exc)
            dead.append(ws)
    for ws in dead:
        state.ws_clients.discard(ws)


def _track_self_and_target(state: ApiState, event: PacketReceivedEvent) -> None:
    """Обновляет кэш позиции и последней цели из входящих пакетов."""
    try:
        if event.opcode == UserInfoPacket.opcode:
            pkt = UserInfoPacket(event.data)
            if pkt.character is not None:
                state.self_object_id = pkt.character.object_id
                state.self_x = pkt.character.x
                state.self_y = pkt.character.y
                state.self_z = pkt.character.z
        elif event.opcode == MyTargetSelectedPacket.opcode:
            pkt = MyTargetSelectedPacket(event.data)
            state.last_target_object_id = pkt.object_id
    except Exception:
        logger.debug("Failed to parse tracking packet 0x%02X", event.opcode, exc_info=True)


def register_subscribers(state: ApiState) -> None:
    """Подписывает API-слой на PacketReceivedEvent эмиттера сессии."""

    async def _on_packet(event: PacketReceivedEvent) -> None:
        _track_self_and_target(state, event)
        await _broadcast(state, event)

    state.emitter.on(PacketReceivedEvent, _on_packet)


@router.websocket("/ws/packets")
async def packets_stream(websocket: WebSocket) -> None:
    state: ApiState = websocket.app.state.api_state
    await websocket.accept()
    state.ws_clients.add(websocket)
    logger.info("WS client connected (total=%d)", len(state.ws_clients))
    try:
        while True:
            # Держим соединение открытым; входящие сообщения от клиента игнорируем.
            await websocket.receive_text()
    except WebSocketDisconnect:
        pass
    finally:
        state.ws_clients.discard(websocket)
        logger.info("WS client disconnected (total=%d)", len(state.ws_clients))


__all__ = ["router", "register_subscribers"]
