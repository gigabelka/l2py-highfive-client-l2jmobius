"""WebSocket-эндпоинт для стрима входящих игровых пакетов."""

from __future__ import annotations

import asyncio
import logging

from fastapi import APIRouter, WebSocket, WebSocketDisconnect

from l2py.api.state import ApiState, NpcRecord
from l2py.events import PacketReceivedEvent
from l2py.protocol.game.server_packets import (
    DeleteObjectPacket,
    InventoryUpdatePacket,
    ItemListPacket,
    MyTargetSelectedPacket,
    NpcInfoPacket,
    ShortCutInitPacket,
    ShortCutRegisterPacket,
    SkillListPacket,
    StatusUpdatePacket,
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


def _userinfo_snapshot(pkt: UserInfoPacket) -> dict:
    """Формирует dict-снимок всех распарсенных полей UserInfo."""
    return {
        "object_id": pkt.object_id,
        "name": pkt.name,
        "x": pkt.x,
        "y": pkt.y,
        "z": pkt.z,
        "heading": pkt.heading,
        "race": pkt.race,
        "sex": pkt.sex,
        "class_id": pkt.class_id,
        "level": pkt.level,
        "exp": pkt.exp,
        "str": pkt.str_,
        "dex": pkt.dex,
        "con": pkt.con,
        "int": pkt.int_,
        "wit": pkt.wit,
        "men": pkt.men,
        "max_hp": pkt.max_hp,
        "cur_hp": pkt.cur_hp,
        "max_mp": pkt.max_mp,
        "cur_mp": pkt.cur_mp,
        "sp": pkt.sp,
        "cur_load": pkt.cur_load,
        "max_load": pkt.max_load,
        "active_weapon_item": pkt.active_weapon_item,
    }


# Соответствие attr_id из StatusUpdate и полей last_user_info (docs: L2JMobius
# StatusUpdate.java). Используется для апдейта снимка при StatusUpdate на self.
_STATUS_UPDATE_TO_USER_INFO: dict[int, str] = {
    1: "level",
    2: "exp",
    3: "str",
    4: "dex",
    5: "con",
    6: "int",
    7: "wit",
    8: "men",
    9: "cur_hp",
    10: "max_hp",
    11: "cur_mp",
    12: "max_mp",
    13: "sp",
    14: "cur_load",
    15: "max_load",
}


def _track_self_and_target(state: ApiState, event: PacketReceivedEvent) -> None:
    """Обновляет кэш позиции и последней цели из входящих пакетов."""
    state.opcode_counts[event.opcode] = state.opcode_counts.get(event.opcode, 0) + 1
    state.recent_packets.append((event.opcode, event.data.hex()))
    if len(state.recent_packets) > 40:
        del state.recent_packets[:-40]
    try:
        if event.opcode == UserInfoPacket.opcode:
            pkt = UserInfoPacket(event.data)
            if pkt.character is not None:
                state.self_object_id = pkt.character.object_id
                state.self_x = pkt.character.x
                state.self_y = pkt.character.y
                state.self_z = pkt.character.z
            state.last_user_info = _userinfo_snapshot(pkt)
        elif event.opcode == StatusUpdatePacket.opcode:
            su_pkt = StatusUpdatePacket(event.data)
            if state.self_object_id is None or su_pkt.object_id == state.self_object_id:
                state.stats.update(su_pkt.updates)
                if state.last_user_info is not None:
                    for attr_id, value in su_pkt.updates.items():
                        key = _STATUS_UPDATE_TO_USER_INFO.get(attr_id)
                        if key is not None:
                            state.last_user_info[key] = value
        elif event.opcode == ItemListPacket.opcode:
            il_pkt = ItemListPacket(event.data)
            state.inventory = {it["object_id"]: it for it in il_pkt.items}
        elif event.opcode == InventoryUpdatePacket.opcode:
            iu_pkt = InventoryUpdatePacket(event.data)
            for change_type, record in iu_pkt.changes:
                oid = record["object_id"]
                if change_type == 3:  # REMOVED
                    state.inventory.pop(oid, None)
                else:  # ADDED / MODIFIED
                    state.inventory[oid] = record
        elif event.opcode == SkillListPacket.opcode:
            sl_pkt = SkillListPacket(event.data)
            state.skills = sl_pkt.skills
        elif event.opcode == MyTargetSelectedPacket.opcode:
            pkt = MyTargetSelectedPacket(event.data)
            state.last_target_object_id = pkt.object_id
            if state.target_confirm_expected_id is not None:
                state.target_confirm_event.set()
        elif event.opcode == NpcInfoPacket.opcode:
            npc_pkt = NpcInfoPacket(event.data)
            state.visible_npcs[npc_pkt.object_id] = NpcRecord(
                object_id=npc_pkt.object_id,
                template_id=npc_pkt.template_id,
                x=npc_pkt.x,
                y=npc_pkt.y,
                z=npc_pkt.z,
                attackable=npc_pkt.attackable,
            )
        elif event.opcode == DeleteObjectPacket.opcode:
            del_pkt = DeleteObjectPacket(event.data)
            state.visible_npcs.pop(del_pkt.object_id, None)
            if state.last_target_object_id == del_pkt.object_id:
                state.last_target_object_id = None
        elif event.opcode == ShortCutInitPacket.opcode:
            init_pkt = ShortCutInitPacket(event.data)
            state.shortcuts = {
                slot: (sc_type, sc_id, level)
                for (sc_type, slot, sc_id, level) in init_pkt.entries
            }
        elif event.opcode == ShortCutRegisterPacket.opcode:
            reg_pkt = ShortCutRegisterPacket(event.data)
            if reg_pkt.type == 0:
                state.shortcuts.pop(reg_pkt.slot, None)
            else:
                state.shortcuts[reg_pkt.slot] = (reg_pkt.type, reg_pkt.id, reg_pkt.level)
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
