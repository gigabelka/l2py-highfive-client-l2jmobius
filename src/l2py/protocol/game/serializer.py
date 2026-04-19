"""Packet → JSON-friendly dict serialization for the WebSocket stream.

The WS endpoint (`src/l2py/api/ws.py`) receives `PacketReceivedEvent(opcode,
data, source)` — raw bytes off the wire. Parsing and presentation rules live
here so that parser classes in `server_packets.py` stay focused on decoding.

The public entry point is :func:`packet_to_envelope` which produces the JSON
envelope described in the API docs:

    {
        "opcode": "0x32",
        "opcode_int": 50,
        "name": "UserInfo" | null,
        "source": "game",
        "len": 142,
        "hex": "...",
        "parsed": {...} | null,
        "parse_error": null | "..."
    }

Adding a parser for a new opcode: register a `ServerPacket` subclass in
`server_packets.py`, then (optionally) add a custom `_serialize_<name>` here.
The generic fallback is applied when no custom serializer exists.
"""

from __future__ import annotations

import dataclasses
from collections.abc import Callable
from typing import Any

from l2py.protocol.base import ServerPacket
from l2py.protocol.game.opcode_names import packet_name
from l2py.protocol.game.server_packets import (
    CharSelectedPacket,
    CharSelectionInfoPacket,
    DeleteObjectPacket,
    DropItemPacket,
    InventoryUpdatePacket,
    ItemListPacket,
    KeyPacket,
    MyTargetSelectedPacket,
    NetPingRequestPacket,
    NpcInfoPacket,
    ShortCutInitPacket,
    ShortCutRegisterPacket,
    SkillListPacket,
    SpawnItemPacket,
    StatusUpdatePacket,
    UserInfoPacket,
)

# StatusUpdate attr_id → UserInfo field name (subset that overlaps UserInfo).
# Source: L2JMobius `StatusUpdate.java`.
STATUS_UPDATE_TO_USER_INFO: dict[int, str] = {
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

# Full attr_id → symbolic name (L2JMobius `StatusUpdate.java`).
STATUS_UPDATE_ATTR_NAMES: dict[int, str] = {
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
    17: "p_atk",
    18: "atk_spd",
    19: "p_def",
    20: "evasion",
    21: "accuracy",
    22: "critical",
    23: "m_atk",
    24: "cast_spd",
    25: "m_def",
    26: "pvp_flag",
    27: "karma",
    33: "cur_cp",
    34: "max_cp",
}


def _bytes_field(b: bytes) -> dict[str, Any] | None:
    if not b:
        return None
    return {"hex": b.hex(), "len": len(b)}


def _serialize_key(p: KeyPacket) -> dict[str, Any]:
    return {
        "result": p.result,
        "enabled": p.enabled,
        "xor_key": _bytes_field(p.xor_key),
        "server_id": p.server_id,
        "obfuscation_key": p.obfuscation_key,
    }


def _serialize_char_selection_info(p: CharSelectionInfoPacket) -> dict[str, Any]:
    return {"characters": [dataclasses.asdict(c) for c in p.characters]}


def _serialize_char_selected(p: CharSelectedPacket) -> dict[str, Any]:
    return {
        "name": p.name,
        "session_id": p.session_id,
        "clan_id": p.clan_id,
        "sex": p.sex,
        "race": p.race,
        "class_id": p.class_id,
        "x": p.x,
        "y": p.y,
        "z": p.z,
    }


def serialize_user_info(p: UserInfoPacket) -> dict[str, Any]:
    """Build a dict of all parsed UserInfo fields.

    Exposed as a module-level helper because `ApiState.last_user_info` must
    use the exact same shape (so that StatusUpdate merges stay coherent).
    """
    return {
        "object_id": p.object_id,
        "name": p.name,
        "x": p.x,
        "y": p.y,
        "z": p.z,
        "heading": p.heading,
        "race": p.race,
        "sex": p.sex,
        "class_id": p.class_id,
        "level": p.level,
        "exp": p.exp,
        "str": p.str_,
        "dex": p.dex,
        "con": p.con,
        "int": p.int_,
        "wit": p.wit,
        "men": p.men,
        "max_hp": p.max_hp,
        "cur_hp": p.cur_hp,
        "max_mp": p.max_mp,
        "cur_mp": p.cur_mp,
        "sp": p.sp,
        "cur_load": p.cur_load,
        "max_load": p.max_load,
        "active_weapon_item": p.active_weapon_item,
    }


def _serialize_user_info_full(p: UserInfoPacket) -> dict[str, Any]:
    out = serialize_user_info(p)
    out["raw_tail"] = _bytes_field(p.raw_tail)
    return out


def _serialize_net_ping_request(p: NetPingRequestPacket) -> dict[str, Any]:
    return {"ping_id": p.ping_id}


def _serialize_my_target_selected(p: MyTargetSelectedPacket) -> dict[str, Any]:
    return {"object_id": p.object_id, "color_distance": p.color_distance}


_SHORTCUT_TYPE_NAMES: dict[int, str] = {
    0: "none",
    1: "item",
    2: "skill",
    3: "action",
    4: "macro",
    5: "recipe",
    6: "bookmark",
}


def _shortcut_to_dict(entry: tuple[int, int, int, int]) -> dict[str, Any]:
    sc_type, slot, sc_id, level = entry
    return {
        "type": sc_type,
        "type_name": _SHORTCUT_TYPE_NAMES.get(sc_type),
        "slot": slot,
        "id": sc_id,
        "level": level,
    }


def _serialize_shortcut_init(p: ShortCutInitPacket) -> dict[str, Any]:
    return {"entries": [_shortcut_to_dict(e) for e in p.entries]}


def _serialize_shortcut_register(p: ShortCutRegisterPacket) -> dict[str, Any]:
    return {
        "type": p.type,
        "type_name": _SHORTCUT_TYPE_NAMES.get(p.type),
        "slot": p.slot,
        "id": p.id,
        "level": p.level,
    }


def _serialize_status_update(p: StatusUpdatePacket) -> dict[str, Any]:
    updates = [
        {
            "attr_id": attr_id,
            "name": STATUS_UPDATE_ATTR_NAMES.get(attr_id),
            "value": value,
        }
        for attr_id, value in p.updates.items()
    ]
    return {
        "object_id": p.object_id,
        "updates": updates,
        "updates_by_id": {str(k): v for k, v in p.updates.items()},
    }


def _serialize_item_list(p: ItemListPacket) -> dict[str, Any]:
    return {"show_window": bool(p.show_window), "items": list(p.items)}


_INVENTORY_CHANGE_NAMES = {1: "added", 2: "modified", 3: "removed"}


def _serialize_inventory_update(p: InventoryUpdatePacket) -> dict[str, Any]:
    return {
        "changes": [
            {
                "change": _INVENTORY_CHANGE_NAMES.get(change_type, "unknown"),
                "change_type": change_type,
                "item": record,
            }
            for change_type, record in p.changes
        ]
    }


def _serialize_skill_list(p: SkillListPacket) -> dict[str, Any]:
    return {"skills": list(p.skills)}


def _serialize_npc_info(p: NpcInfoPacket) -> dict[str, Any]:
    return {
        "object_id": p.object_id,
        "template_id": p.template_id,
        "attackable": p.attackable,
        "x": p.x,
        "y": p.y,
        "z": p.z,
        "heading": p.heading,
    }


def _serialize_spawn_item(p: SpawnItemPacket) -> dict[str, Any]:
    return {
        "object_id": p.object_id,
        "item_id": p.item_id,
        "x": p.x,
        "y": p.y,
        "z": p.z,
        "stackable": p.stackable,
        "count": p.count,
    }


def _serialize_drop_item(p: DropItemPacket) -> dict[str, Any]:
    return {
        "dropper_object_id": p.dropper_object_id,
        "object_id": p.object_id,
        "item_id": p.item_id,
        "x": p.x,
        "y": p.y,
        "z": p.z,
        "stackable": p.stackable,
        "count": p.count,
    }


def _serialize_delete_object(p: DeleteObjectPacket) -> dict[str, Any]:
    return {"object_id": p.object_id}


# opcode → (parser class, serializer function).
_REGISTRY: dict[int, tuple[type[ServerPacket], Callable[[Any], dict[str, Any]]]] = {
    KeyPacket.opcode: (KeyPacket, _serialize_key),
    CharSelectionInfoPacket.opcode: (CharSelectionInfoPacket, _serialize_char_selection_info),
    CharSelectedPacket.opcode: (CharSelectedPacket, _serialize_char_selected),
    UserInfoPacket.opcode: (UserInfoPacket, _serialize_user_info_full),
    NetPingRequestPacket.opcode: (NetPingRequestPacket, _serialize_net_ping_request),
    MyTargetSelectedPacket.opcode: (MyTargetSelectedPacket, _serialize_my_target_selected),
    ShortCutInitPacket.opcode: (ShortCutInitPacket, _serialize_shortcut_init),
    ShortCutRegisterPacket.opcode: (ShortCutRegisterPacket, _serialize_shortcut_register),
    StatusUpdatePacket.opcode: (StatusUpdatePacket, _serialize_status_update),
    ItemListPacket.opcode: (ItemListPacket, _serialize_item_list),
    InventoryUpdatePacket.opcode: (InventoryUpdatePacket, _serialize_inventory_update),
    SkillListPacket.opcode: (SkillListPacket, _serialize_skill_list),
    NpcInfoPacket.opcode: (NpcInfoPacket, _serialize_npc_info),
    SpawnItemPacket.opcode: (SpawnItemPacket, _serialize_spawn_item),
    DropItemPacket.opcode: (DropItemPacket, _serialize_drop_item),
    DeleteObjectPacket.opcode: (DeleteObjectPacket, _serialize_delete_object),
}


def packet_to_envelope(opcode: int, data: bytes, source: str) -> dict[str, Any]:
    """Build the WS JSON envelope for a received packet.

    Always emits opcode/hex/len/source. If a parser is registered for ``opcode``,
    attempts to parse+serialize and attaches ``parsed``. On parse failure, sets
    ``parse_error`` with a short description.
    """
    envelope: dict[str, Any] = {
        "opcode": f"0x{opcode:02X}",
        "opcode_int": opcode,
        "name": packet_name(opcode, data),
        "source": source,
        "len": len(data),
        "hex": data.hex(),
        "parsed": None,
        "parse_error": None,
    }

    entry = _REGISTRY.get(opcode)
    if entry is None:
        return envelope

    parser_cls, serializer = entry
    try:
        pkt = parser_cls(data)
        envelope["parsed"] = serializer(pkt)
    except Exception as exc:  # noqa: BLE001 — we want to surface any parse error
        envelope["parse_error"] = f"{type(exc).__name__}: {exc}"
    return envelope


__all__ = [
    "packet_to_envelope",
    "serialize_user_info",
    "STATUS_UPDATE_TO_USER_INFO",
    "STATUS_UPDATE_ATTR_NAMES",
]
