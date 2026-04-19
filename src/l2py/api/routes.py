"""HTTP-эндпоинты внешнего API клиента l2py."""

from __future__ import annotations

import logging

from fastapi import APIRouter, HTTPException, Path, Request

from l2py.api.schemas import (
    AttackBody,
    ObjectIdBody,
    SendResult,
    ShortcutBody,
    SitStandRequest,
    StatusResponse,
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


@router.post(
    "/action/sit-stand",
    response_model=SendResult,
    summary="Sit / Stand (RequestActionUse action_id=0)",
)
async def sit_stand(body: SitStandRequest, request: Request) -> SendResult:
    state = _state(request)
    return await _send(state, RequestActionUsePacket(0, ctrl=body.ctrl, shift=body.shift))


@router.post(
    "/action/attack",
    response_model=SendResult,
    summary="Attack (AttackRequest 0x32)",
)
async def attack(body: AttackBody, request: Request) -> SendResult:
    state = _state(request)
    x, y, z = _origin(state)
    return await _send(
        state,
        AttackRequestPacket(body.object_id, x, y, z, attack_id=1 if body.shift else 0),
    )


@router.post(
    "/action/pick-up",
    response_model=SendResult,
    summary="Pick Up (Action 0x1F на objectId предмета)",
)
async def pick_up(body: ObjectIdBody, request: Request) -> SendResult:
    state = _state(request)
    x, y, z = _origin(state)
    return await _send(state, ActionPacket(body.object_id, x, y, z, action_id=0))


@router.post(
    "/action/next-target",
    response_model=SendResult,
    summary="Next Target — шлёт Action 0x1F на указанный objectId (цикл целей — на стороне вызывающего)",
)
async def next_target(body: ObjectIdBody, request: Request) -> SendResult:
    state = _state(request)
    x, y, z = _origin(state)
    return await _send(state, ActionPacket(body.object_id, x, y, z, action_id=0))


@router.post(
    "/key/f{slot}",
    response_model=SendResult,
    summary="F1–F12: диспатч по type (ACTION/SKILL/ITEM)",
)
async def press_fkey(
    body: ShortcutBody,
    request: Request,
    slot: int = Path(..., ge=1, le=12),
) -> SendResult:
    state = _state(request)
    if body.type == "ACTION":
        packet: ClientPacket = RequestActionUsePacket(body.id, ctrl=body.ctrl, shift=body.shift)
    elif body.type == "SKILL":
        packet = RequestMagicSkillUsePacket(body.id, ctrl=body.ctrl, shift=body.shift)
    elif body.type == "ITEM":
        packet = UseItemPacket(body.id, ctrl=body.ctrl)
    else:  # pragma: no cover - защищено Literal
        raise HTTPException(status_code=400, detail=f"Unsupported shortcut type: {body.type}")
    logger.debug("F%d dispatch: type=%s id=%d", slot, body.type, body.id)
    return await _send(state, packet)


__all__ = ["router"]
