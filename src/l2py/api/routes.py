"""HTTP-эндпоинты внешнего API клиента l2py."""

from __future__ import annotations

import logging

from fastapi import APIRouter, HTTPException, Path, Request

from l2py.api.schemas import (
    SendResult,
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
    return StatusResponse(
        connected=True,
        char_name=session.character.name,
        object_id=state.self_object_id if state.self_object_id is not None
            else session.character.object_id,
        x=state.self_x if state.self_x is not None else session.character.x,
        y=state.self_y if state.self_y is not None else session.character.y,
        z=state.self_z if state.self_z is not None else session.character.z,
        last_target_id=state.last_target_object_id,
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
    summary="Текущая цель: возвращает id цели",
)
async def next_target(request: Request) -> TargetIdResponse:
    state = _state(request)
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
