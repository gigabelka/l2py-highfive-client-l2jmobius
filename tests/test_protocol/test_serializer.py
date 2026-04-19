"""Tests for the WS packet serializer (packet → JSON envelope)."""

from __future__ import annotations

from l2py.protocol.base import PacketWriter
from l2py.protocol.game.opcode_names import OPCODE_NAMES, packet_name
from l2py.protocol.game.serializer import (
    _REGISTRY,
    decode_raw,
    packet_to_envelope,
    serialize_user_info,
)
from l2py.protocol.game.server_packets import (
    DeleteObjectPacket,
    MyTargetSelectedPacket,
    NetPingRequestPacket,
    NpcInfoPacket,
    SkillListPacket,
    SpawnItemPacket,
    StatusUpdatePacket,
    UserInfoPacket,
)


def _write_user_info_fixture(name: str = "hero") -> bytes:
    """Builds a minimal UserInfoPacket body matching the parser layout."""
    w = PacketWriter()
    w.write_int32(1000)  # x
    w.write_int32(2000)  # y
    w.write_int32(-3000)  # z
    w.write_int32(42)  # heading
    w.write_int32(0x01020304)  # object_id
    w.write_string(name)
    w.write_int32(1)  # race
    w.write_int32(0)  # sex
    w.write_int32(88)  # class_id
    w.write_int32(76)  # level
    w.write_int64(123456789)  # exp
    for val in (40, 30, 43, 21, 20, 25):  # str..men
        w.write_int32(val)
    w.write_int32(3500)  # max_hp
    w.write_int32(3500)  # cur_hp
    w.write_int32(1200)  # max_mp
    w.write_int32(1100)  # cur_mp
    w.write_int32(50000)  # sp
    w.write_int32(15000)  # cur_load
    w.write_int32(80000)  # max_load
    w.write_int32(7575)  # active_weapon_item
    return w.to_bytes()


# --- basic envelope shape -------------------------------------------------


def test_unknown_opcode_returns_envelope_with_null_parsed():
    env = packet_to_envelope(0x7D, b"\x01\x02\x03", "game")
    assert env["opcode"] == "0x7D"
    assert env["opcode_int"] == 0x7D
    assert env["name"] == "Dummy"  # from OPCODE_NAMES
    assert env["source"] == "game"
    assert env["len"] == 3
    assert env["raw"]["hex"] == "010203"
    assert env["raw"]["bytes"] == [1, 2, 3]
    assert env["raw"]["ascii"] == "..."
    assert "u16_le" not in env["raw"]  # length 3 is not 2-aligned
    assert env["parsed"] is None
    assert env["parse_error"] is None


def test_totally_unknown_opcode_has_null_name():
    # 0x04 is ATTACK_DEAD_TARGET per enum, so pick an opcode not in enum.
    # All 0x00..0xFE are enumerated; use 0xFF.
    env = packet_to_envelope(0xFF, b"", "game")
    assert env["name"] is None
    assert env["parsed"] is None


def test_extended_opcode_name_lookup():
    # 0xFE + sub 0x2F == ExStorageMaxCount.
    sub = bytes([0x2F, 0x00])
    env = packet_to_envelope(0xFE, sub + b"\x64\x00\x00\x00", "game")
    assert env["name"] == "ExStorageMaxCount"


# --- parsed envelopes -----------------------------------------------------


def test_user_info_envelope():
    data = _write_user_info_fixture("hero")
    env = packet_to_envelope(UserInfoPacket.opcode, data, "game")

    assert env["name"] == "UserInfo"
    assert env["parse_error"] is None
    parsed = env["parsed"]
    assert parsed["object_id"] == 0x01020304
    assert parsed["name"] == "hero"
    assert parsed["x"] == 1000
    assert parsed["z"] == -3000
    assert parsed["class_id"] == 88
    assert parsed["level"] == 76
    assert parsed["exp"] == 123456789
    assert parsed["str"] == 40
    assert parsed["int"] == 21
    assert parsed["max_hp"] == 3500
    assert parsed["sp"] == 50000
    assert parsed["active_weapon_item"] == 7575
    # raw_tail is empty for a minimal fixture.
    assert parsed["raw_tail"] is None


def test_serialize_user_info_helper_shape_matches_legacy_snapshot():
    # Regression guard: ApiState.last_user_info schema stays stable.
    pkt = UserInfoPacket(_write_user_info_fixture())
    snap = serialize_user_info(pkt)
    assert set(snap.keys()) == {
        "object_id", "name", "x", "y", "z", "heading",
        "race", "sex", "class_id", "level", "exp",
        "str", "dex", "con", "int", "wit", "men",
        "max_hp", "cur_hp", "max_mp", "cur_mp",
        "sp", "cur_load", "max_load", "active_weapon_item",
    }


def test_status_update_envelope():
    w = PacketWriter()
    w.write_int32(123)  # object_id
    w.write_int32(3)  # count
    w.write_int32(9)
    w.write_int32(1500)  # CUR_HP
    w.write_int32(33)
    w.write_int32(800)  # CUR_CP
    w.write_int32(99)
    w.write_int32(42)  # unknown attr_id
    env = packet_to_envelope(StatusUpdatePacket.opcode, w.to_bytes(), "game")

    assert env["name"] == "StatusUpdate"
    parsed = env["parsed"]
    assert parsed["object_id"] == 123
    updates = {u["attr_id"]: u for u in parsed["updates"]}
    assert updates[9]["name"] == "cur_hp"
    assert updates[9]["value"] == 1500
    assert updates[33]["name"] == "cur_cp"
    assert updates[99]["name"] is None
    assert parsed["updates_by_id"]["9"] == 1500


def test_net_ping_envelope():
    w = PacketWriter()
    w.write_int32(0xDEADBEEF - (1 << 32))  # signed wrap
    env = packet_to_envelope(NetPingRequestPacket.opcode, w.to_bytes(), "game")
    assert env["name"] == "NetPing"
    assert env["parsed"]["ping_id"] == 0xDEADBEEF - (1 << 32)


def test_my_target_selected_envelope():
    w = PacketWriter()
    w.write_int32(555)
    w.write_int32(-1)
    env = packet_to_envelope(MyTargetSelectedPacket.opcode, w.to_bytes(), "game")
    assert env["name"] == "MyTargetSelected"
    assert env["parsed"] == {"object_id": 555, "color_distance": -1}


def test_npc_info_envelope():
    w = PacketWriter()
    w.write_int32(9001)  # object_id
    w.write_int32(1020304)  # template_id + 1_000_000
    w.write_int32(1)  # attackable
    w.write_int32(10)
    w.write_int32(20)
    w.write_int32(30)
    w.write_int32(0)  # heading
    env = packet_to_envelope(NpcInfoPacket.opcode, w.to_bytes(), "game")
    assert env["name"] == "NpcInfo"
    parsed = env["parsed"]
    assert parsed["object_id"] == 9001
    assert parsed["template_id"] == 20304
    assert parsed["attackable"] is True


def test_spawn_item_envelope():
    w = PacketWriter()
    w.write_int32(1)  # object_id
    w.write_int32(57)  # item_id (adena)
    w.write_int32(100)  # x
    w.write_int32(200)  # y
    w.write_int32(300)  # z
    w.write_int32(1)  # stackable
    w.write_int64(50000)  # count
    env = packet_to_envelope(SpawnItemPacket.opcode, w.to_bytes(), "game")
    assert env["name"] == "SpawnItem"
    parsed = env["parsed"]
    assert parsed["item_id"] == 57
    assert parsed["count"] == 50000
    assert parsed["stackable"] is True


def test_delete_object_envelope():
    w = PacketWriter()
    w.write_int32(777)
    env = packet_to_envelope(DeleteObjectPacket.opcode, w.to_bytes(), "game")
    assert env["name"] == "DeleteObject"
    assert env["parsed"] == {"object_id": 777}


def test_skill_list_envelope():
    w = PacketWriter()
    w.write_int32(2)  # count
    # Skill 1
    w.write_int32(0)  # passive
    w.write_int32(3)  # level
    w.write_int32(1068)  # id
    w.write_byte(0)  # disabled
    # Skill 2
    w.write_int32(1)  # passive
    w.write_int32(1)  # level
    w.write_int32(234)  # id
    w.write_byte(1)  # disabled
    env = packet_to_envelope(SkillListPacket.opcode, w.to_bytes(), "game")
    assert env["name"] == "SkillList"
    parsed = env["parsed"]
    assert len(parsed["skills"]) == 2
    assert parsed["skills"][0] == {"id": 1068, "level": 3, "passive": False, "disabled": False}
    assert parsed["skills"][1] == {"id": 234, "level": 1, "passive": True, "disabled": True}


def test_truncated_payload_sets_hex_but_parse_survives():
    # UserInfo parser swallows its own exceptions; should not surface parse_error.
    env = packet_to_envelope(UserInfoPacket.opcode, b"\x01\x02", "game")
    assert env["name"] == "UserInfo"
    # parser is tolerant, so parsed is set with defaults
    assert env["parsed"] is not None
    assert env["raw"]["hex"] == "0102"


# --- coverage invariants --------------------------------------------------


def test_decode_raw_int_views():
    # 8 bytes: two identical i32 values = 1, 2 → all aligned views must appear.
    data = bytes.fromhex("0100000002000000")
    dec = decode_raw(data)
    assert dec["hex"] == "0100000002000000"
    assert dec["len"] == 8
    assert dec["bytes"] == [1, 0, 0, 0, 2, 0, 0, 0]
    assert dec["u16_le"] == [1, 0, 2, 0]
    assert dec["i32_le"] == [1, 2]
    assert dec["u32_le"] == [1, 2]
    assert dec["i64_le"] == [(2 << 32) | 1]
    assert dec["ascii"] == "........"
    assert "utf16le_strings" not in dec  # no printable UTF-16LE string


def test_decode_raw_extracts_utf16le_strings():
    data = "hero".encode("utf-16le") + b"\x00\x00" + b"\x11\x22"
    dec = decode_raw(data)
    assert dec["utf16le_strings"] == [{"offset": 0, "value": "hero", "byte_len": 10}]


def test_decode_raw_empty():
    dec = decode_raw(b"")
    assert dec == {"hex": "", "len": 0, "bytes": [], "ascii": ""}


def test_decode_raw_ascii_preview_shows_printable():
    dec = decode_raw(b"\x00AB\xff")
    assert dec["ascii"] == ".AB."


def test_user_info_raw_tail_is_decoded_when_present():
    payload = _write_user_info_fixture("hero") + b"\xaa\xbb\xcc\xdd"
    env = packet_to_envelope(UserInfoPacket.opcode, payload, "game")
    tail = env["parsed"]["raw_tail"]
    assert tail is not None
    assert tail["hex"] == "aabbccdd"
    assert tail["bytes"] == [0xAA, 0xBB, 0xCC, 0xDD]
    assert tail["u32_le"] == [0xDDCCBBAA]


def test_every_registered_opcode_has_name():
    missing = [op for op in _REGISTRY if op not in OPCODE_NAMES]
    assert missing == [], f"Registered parsers missing from OPCODE_NAMES: {missing}"


def test_packet_name_helper_matches_table():
    for op, name in OPCODE_NAMES.items():
        if op == 0xFE:
            continue  # requires sub-opcode
        assert packet_name(op) == name
