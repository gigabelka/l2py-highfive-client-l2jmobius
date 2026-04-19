"""HTTP-эндпоинты внешнего API клиента l2py."""

from __future__ import annotations

import asyncio
import logging

from fastapi import APIRouter, HTTPException, Path, Request

from l2py.api.schemas import (
    ItemView,
    SendResult,
    ShortcutView,
    SkillView,
    StatusResponse,
    TargetIdResponse,
)
from l2py.api.state import ApiState
from l2py.protocol.base import ClientPacket
from l2py.protocol.game.client_packets import (
    ActionPacket,
    AttackRequestPacket,
    RequestActionUsePacket,
    RequestMagicSkillUsePacket,
    UseItemPacket,
)

logger = logging.getLogger(__name__)

router = APIRouter(prefix="/api", tags=["actions"])


def _state(request: Request) -> ApiState:
    state: ApiState | None = getattr(request.app.state, "api_state", None)
    if state is None:
        raise HTTPException(status_code=503, detail="API state is not initialised")
    return state


def _require_session(state: ApiState):
    if state.session is None:
        raise HTTPException(status_code=503, detail="Game session is not active")
    return state.session


async def _send(state: ApiState, packet: ClientPacket) -> SendResult:
    session = _require_session(state)
    try:
        await session.connection.send_packet(packet)
    except ConnectionError as exc:
        raise HTTPException(status_code=502, detail=f"send failed: {exc}") from exc
    return SendResult(
        ok=True,
        opcode=f"0x{packet.opcode:02X}",
        description=type(packet).__name__,
    )


def _origin(state: ApiState) -> tuple[int, int, int]:
    pos = state.self_position()
    if pos is None:
        raise HTTPException(
            status_code=409,
            detail="Self position is not known yet (UserInfo not received).",
        )
    return pos


@router.get("/status", response_model=StatusResponse, summary="Текущее состояние клиента")
async def get_status(request: Request) -> StatusResponse:
    state = _state(request)
    session = state.session
    if session is None:
        return StatusResponse(connected=False)

    inventory = [
        ItemView(
            object_id=it["object_id"],
            item_id=it["item_id"],
            count=it["count"],
            location=it.get("location", 0),
            equipped=bool(it.get("equipped", 0)),
            body_part=it.get("body_part", 0),
            enchant=it.get("enchant", 0),
            type2=it.get("type2", 0),
            augmentation_id=it.get("augmentation_id", 0),
            mana=it.get("mana", -1),
            time=it.get("time", -9999),
            attack_element_type=it.get("attack_element_type", -2),
            attack_element_power=it.get("attack_element_power", 0),
            def_element=list(it.get("def_element") or []),
        )
        for it in state.inventory.values()
    ]
    skills = [
        SkillView(
            id=s["id"],
            level=s["level"],
            passive=s.get("passive", False),
            disabled=s.get("disabled", False),
        )
        for s in state.skills
    ]
    shortcuts = [
        ShortcutView(slot=slot, type=sc_type, id=sc_id, level=level)
        for slot, (sc_type, sc_id, level) in state.shortcuts.items()
    ]

    return StatusResponse(
        connected=True,
        char_name=session.character.name,
        object_id=state.self_object_id if state.self_object_id is not None
            else session.character.object_id,
        x=state.self_x if state.self_x is not None else session.character.x,
        y=state.self_y if state.self_y is not None else session.character.y,
        z=state.self_z if state.self_z is not None else session.character.z,
        last_target_id=state.last_target_object_id,
        user_info=state.last_user_info,
        stats=dict(state.stats),
        inventory=inventory,
        skills=skills,
        shortcuts=shortcuts,
    )


@router.get(
    "/action/sit-stand",
    response_model=SendResult,
    summary="Сидеть / Стоять",
)
async def sit_stand(request: Request) -> SendResult:
    state = _state(request)
    return await _send(state, RequestActionUsePacket(0))


@router.get(
    "/action/attack/{id}",
    response_model=SendResult,
    summary="Текущая цель: принимает только id цели",
)
async def attack(request: Request, id: int = Path(..., description="objectId цели")) -> SendResult:
    state = _state(request)
    x, y, z = _origin(state)
    return await _send(state, AttackRequestPacket(id, x, y, z, attack_id=0))


@router.get(
    "/action/pick-up/{id}",
    response_model=SendResult,
    summary="Поднять предмет: принимает только id предмета",
)
async def pick_up(request: Request, id: int = Path(..., description="objectId предмета на земле")) -> SendResult:
    state = _state(request)
    x, y, z = _origin(state)
    return await _send(state, ActionPacket(id, x, y, z, action_id=0))


@router.get(
    "/action/next-target",
    response_model=TargetIdResponse,
    summary="Выбрать ближайшего враждебного моба и вернуть его objectId",
)
async def next_target(request: Request) -> TargetIdResponse:
    state = _state(request)
    session = _require_session(state)
    sx, sy, sz = _origin(state)

    candidates = [
        npc for npc in state.visible_npcs.values()
        if npc.attackable and npc.object_id != state.self_object_id
    ]
    if not candidates:
        raise HTTPException(
            status_code=409,
            detail="no attackable NPCs in sight (NpcInfo кэш пуст)",
        )

    nearest = min(
        candidates,
        key=lambda n: (n.x - sx) ** 2 + (n.y - sy) ** 2 + (n.z - sz) ** 2,
    )

    state.target_confirm_expected_id = nearest.object_id
    state.target_confirm_event.clear()

    try:
        await session.connection.send_packet(
            ActionPacket(nearest.object_id, sx, sy, sz, action_id=0)
        )
    except ConnectionError as exc:
        state.target_confirm_expected_id = None
        raise HTTPException(status_code=502, detail=f"send failed: {exc}") from exc

    try:
        await asyncio.wait_for(state.target_confirm_event.wait(), timeout=1.5)
    except TimeoutError as exc:
        state.target_confirm_expected_id = None
        raise HTTPException(
            status_code=504,
            detail="server did not confirm MyTargetSelected in 1.5s",
        ) from exc

    state.target_confirm_expected_id = None
    return TargetIdResponse(id=state.last_target_object_id)


@router.get(
    "/key/f{slot}",
    response_model=SendResult,
    summary="F1–F12 функциональнык клавиши",
)
async def press_fkey(
    request: Request,
    slot: int = Path(..., ge=1, le=12),
) -> SendResult:
    state = _state(request)
    encoded_slot = slot - 1  # page 0
    entry = state.shortcuts.get(encoded_slot)
    if entry is None:
        raise HTTPException(
            status_code=404,
            detail=f"F{slot}: слот action-bar пуст или ShortCutInit ещё не получен",
        )
    sc_type, sc_id, level = entry
    if sc_type == 3:  # ACTION
        packet: ClientPacket = RequestActionUsePacket(sc_id)
    elif sc_type == 2:  # SKILL
        packet = RequestMagicSkillUsePacket(sc_id)
    elif sc_type == 1:  # ITEM
        packet = UseItemPacket(sc_id)
    else:
        raise HTTPException(
            status_code=409,
            detail=f"F{slot}: тип шортката {sc_type} не поддерживается (MACRO/RECIPE/BOOKMARK)",
        )
    logger.debug("F%d dispatch: type=%d id=%d level=%d", slot, sc_type, sc_id, level)
    return await _send(state, packet)


__all__ = ["router"]
