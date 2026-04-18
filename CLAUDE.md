# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project

`l2py` — an asyncio client for Lineage 2 High Five chronicle, compatible with the [L2JMobius](https://github.com/L2JMobius/L2J_Mobius) server (CT 2.6). Implements the wire protocol end-to-end (login + game) for programmatic control of an L2 client. Requires Python **3.14+**.

## Commands

Install in dev mode (creates an editable install with test/lint deps):

```bash
python -m venv .venv
.venv\Scripts\activate          # Windows
pip install -e ".[dev]"
```

Run the example autologin entry point:

```bash
python main.py
```

Testing (pytest, `asyncio_mode = "auto"`, `pythonpath = ["src"]`):

```bash
pytest                                      # full suite
pytest tests/test_crypto                    # a directory
pytest tests/test_protocol/test_login_packets.py::TestName::test_case   # single test
pytest -k "blowfish"                        # filter by name
```

Lint / format:

```bash
ruff check .
ruff format .
```

## Architecture

The codebase is split along protocol boundaries. Understanding the login → game handoff is essential before editing any network or crypto code.

### Two-phase session lifecycle

[src/l2py/client.py](src/l2py/client.py) exposes `L2Client.enter()` — the only public entry point. It orchestrates two sequential flows:

1. **`LoginFlow`** ([src/l2py/network/login_flow.py](src/l2py/network/login_flow.py)) — talks to the **Login Server** (default port 2106). Performs Init/GGAuth/AuthLogin/ServerList/PlayOk handshake and returns session keys (`loginOkId1/2`, `playOkId1/2`) plus the chosen `GameServer` address.
2. **`GameFlow`** ([src/l2py/network/game_flow.py](src/l2py/network/game_flow.py)) — opens a fresh TCP connection to the chosen Game Server, does ProtocolVersion/CryptInit handshake, AuthRequest (reusing the session keys from phase 1 in the specific order **playOkId2, playOkId1, loginOkId1, loginOkId2**), then CharacterSelected → EnterWorld, yielding a `GameSession` with a live connection you can keep alive via `session.run_keepalive()`.

These phases use **different ciphers and different key material** — do not share crypto state between them.

### Crypto ([src/l2py/crypto/](src/l2py/crypto/))

- **`blowfish.py` / `blowfish_engine.py`** — Blowfish ECB, used only during the login phase. Static login key is `6B 60 CB 5B 82 CE 90 B1 CC 2B 6C 55 6C 6C 6C 6C`.
- **`login_crypt.py`** — padding (4-byte align + 8 zeros + 8-byte align), NewCrypt XOR checksum in the last 4 bytes, then Blowfish. The first Init packet additionally uses a rolling XOR reverse and drops 8 trailing bytes.
- **`rsa.py`** — RSA-1024 with `RSA_NO_PADDING`, exponent 65537. Server-supplied modulus must be *unscrambled* before use (order: C⁻¹, B⁻¹, A⁻¹, D⁻¹). Plaintext layout: 94 / 14 login / 2 / 16 password / 2.
- **`game_crypt.py`** — XOR stream cipher used on the game channel *after* `CryptInit`. Static key tail `C8 27 93 01 A1 6C 31 97`. Chaining: `out[i] = src[i] ^ key[i&15] ^ prev` (prev = ciphertext byte in both directions). **After every packet, rotate `key[8..12] += packetSize` as a LE DWORD** — this MUST be done even for unrecognized opcodes or the stream desyncs.

### Protocol ([src/l2py/protocol/](src/l2py/protocol/))

All values are little-endian. Framing: `u16 LE length` prefix that INCLUDES the 2 length bytes themselves.

- **`base.py`** — `PacketReader` / `PacketWriter` primitives (`read_byte`, `read_int`, `read_string` UTF-16LE null-terminated, etc.), plus `ClientPacket` / `ServerPacket` abstract bases.
- **`login/client_packets.py`**, **`login/server_packets.py`** — login-phase packets (7 total; see [docs/PROTOCOL.md](docs/PROTOCOL.md)).
- **`game/client_packets.py`**, **`game/server_packets.py`** — game-phase packets. Note CT 2.6–specific opcodes: `NetPingRequest = 0xD9` answered with `NetPing = 0xB1` (5-byte body, not 0xA8/0xD3); `UseItem = 0x19` (not 0x14). Extended opcodes are `0xFE 0xXXXX`.

### Events ([src/l2py/events.py](src/l2py/events.py))

Typed event bus used by the flows to publish handshake milestones and incoming packets. Subscribe at the `GameSession` level.

## Protocol reference

When touching packet encoding, crypto, or adding new opcodes, the authoritative specs live in [docs/](docs/):

- [docs/PROTOCOL.md](docs/PROTOCOL.md) — every login + game packet with annotated hex dumps and exact body sizes on L2JMobius HighFive.
- [docs/CRYPTOGRAPHY.md](docs/CRYPTOGRAPHY.md) — test vectors and pipelines for Blowfish, NewCrypt XOR, RSA unscramble, and the game XOR cipher.
- [docs/AUTOLOGIN.md](docs/AUTOLOGIN.md) — full pseudocode for the three-phase login → game → in-game sequence.
- [docs/CONSTANTS.md](docs/CONSTANTS.md) — LoginFail/PlayFail reason codes, social-action ids, duplicate opcodes across packet directions.
- [docs/CHECKLIST.md](docs/CHECKLIST.md) — porting checklist, also useful as a correctness smoke-test list.
- [docs/SKILLS.md](docs/SKILLS.md) — class skill trees (1st/2nd/3rd) for every playable class: skill id, name, max level, learn-level, SP total. Generated from the L2JMobius server XML by [scripts/gen_skills_doc.py](scripts/gen_skills_doc.py); rerun that script to refresh.
- [docs/INVENTORY.md](docs/INVENTORY.md) — character inventory spec (personal items only — weapons, armor, accessories, adena): 25 paperdoll slots, body-part bitmasks, WeaponType/ArmorType/CrystalType taxonomies, per-class equip rules, on-wire item record, and the narrow packet set (`ItemList 0x11`, `InventoryUpdate 0x21`, `ExStorageMaxCount 0xFE 0x2F`, `UseItem 0x19`, `RequestUnEquipItem 0x16`, `RequestDropItem 0x17`, `RequestDestroyItem 0x60`). Warehouse / pet / trade / quest items are out of scope.
- [docs/ITEMS.md](docs/ITEMS.md) — catalogue of every item a character can put into their inventory (weapons, armor, off-hand shields/sigils, jewelry, belt, hair, adena). Grouped by weapon type / body slot / armor type / crystal grade; includes id, name, weight, and core stats. Generated from the L2JMobius server XML by [scripts/gen_items_doc.py](scripts/gen_items_doc.py); rerun to refresh.

## Gotchas

- Login and game packets have the **same framing** but different crypto — never reuse cipher objects across the phase boundary.
- Login keys (`loginOkId1/2`, `playOkId1/2`) must be forwarded into `AuthRequest` in the non-obvious order listed above.
- `ServerList` records are 21 bytes each; the trailer block (per-server character counts) is not needed for autologin and should be skipped.
- On the game channel, never disconnect on an unknown opcode — log and drop, but still advance the XOR key rotation.
- `UserInfo (0x32)` arriving in `WAIT_CHAR_SELECTED` state is an implicit confirmation of character selection.
