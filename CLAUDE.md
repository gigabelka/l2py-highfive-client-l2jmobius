# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project

**l2py** is an asyncio client for Lineage 2 High Five chronicle, targeting an **L2JMobius CT 2.6** server. It implements the full L2 wire protocol: RSA-scrambled login auth, Blowfish-wrapped login packets, XOR-based game packets, typed packet classes for both Login and Game servers, and orchestration flows that drive a session from TCP connect through world entry. Requires **Python 3.14+**.

**Status:** Alpha. Login flow is complete end-to-end through `EnterWorld`; in-world game actions (move, attack, skills) are not yet implemented.

The authoritative protocol reference is [SPECIFICATION.md](SPECIFICATION.md) — consult it before changing packet layouts, crypto, or framing. It documents wire format, opcodes, key derivation, and the exact packet sequences for both phases. Do not guess protocol behavior; cross-check against the spec.

## Commands

```bash
# Install (editable + dev extras)
pip install -e ".[dev]"

# Run the example end-to-end login (connects to a live server)
python main.py

# Tests
pytest                                       # full suite
pytest tests/test_crypto                     # one subtree
pytest tests/test_integration/test_login_flow.py::TestLoginFlow::test_name -v
pytest -k blowfish                           # by keyword

# Lint / format (ruff, py314 target, line-length 99)
ruff check .
ruff format .
```

`pytest-asyncio` is configured with `asyncio_mode = "auto"` — async test functions do **not** need the `@pytest.mark.asyncio` decorator. `pythonpath = ["src"]` is set in `pyproject.toml`, so tests import `l2py` directly without installing.

## Architecture

Three layers stacked on top of each other; understand this split before editing.

### 1. `crypto/` — stateless ciphers
- `blowfish.py` / `blowfish_engine.py` — Blowfish ECB used for the Login Server packet body.
- `login_crypt.py` — `LoginCrypt` wraps Blowfish with the NewCrypt checksum/scheme used on the login connection. Factory `create_login_crypt_for_l2jmobius()` produces the L2JMobius-compatible variant.
- `game_crypt.py` — `GameCrypt` implements the L2 XOR cipher with the rolling 8-byte key advanced by the per-packet length. **Encryption on the game channel is gated by `encryptionFlag` from the server's CryptInit packet**; L2JMobius CT 2.6 ships it as `0`, so real sessions stay plaintext — keep this code path working for both.
- `rsa.py` — `L2RSA` + `unscramble_modulus` for the scrambled 128-byte modulus the login server sends. Password is RSA-encrypted (no padding) before `RequestAuthLogin`.

### 2. `protocol/` — packet (de)serialization, no I/O
- `base.py` — `PacketReader` / `PacketWriter` primitives (little-endian, UTF-16LE null-terminated strings) and `ClientPacket` / `ServerPacket` base classes.
- `protocol/login/{client,server}_packets.py` — login-phase packets: `InitPacket`, `GGAuthPacket`, `LoginOkPacket`, `ServerListPacket`, `PlayOkPacket`, `LoginFailPacket` and their client counterparts.
- `protocol/game/{client,server}_packets.py` — game-phase packets including `CryptInit`, `UserInfo`, `CharSelectionInfo`, `EnterWorld`, etc.

Packet classes own their opcode and wire format — when adding one, add it here rather than inline in flow code.

### 3. `network/` — connections and flows
- `login_connection.py`, `game_connection.py` — low-level asyncio TCP transports. They own a `LoginCrypt` / `GameCrypt` instance and handle framing (`u16 LE` length prefix) + encrypt/decrypt transparently. Flow code sees decoded packet bytes.
- `login_flow.py` — `LoginFlow` orchestrates the 6-packet login exchange and returns a `LoginResult` holding the four session tokens, chosen `GameServer`, and Blowfish key.
- `game_flow.py` — `GameFlow` takes that `LoginResult`, connects to the Game Server, performs the CryptInit handshake, enables the XOR cipher only if the server's flag requests it, picks the character slot, sends `EnterWorld`, and returns a `GameSession` with a live connection + `CharacterInfo`.

### Top-level composition
- `client.py` — `L2Client.enter()` is the public facade: runs `LoginFlow` then `GameFlow` and returns the `GameSession`. All user-facing configuration is in `config.py` (`LoginConfig`, `Credentials`, `ConnectionConfig`).
- `events.py` — typed event emitter (`EventEmitter`, `EventMixin`) with event classes like `LoggedInEvent`, `ServerListEvent`, `PacketReceivedEvent` for observing flow progress.
- `models/` — plain dataclasses (`GameServer`, `CharacterInfo`) returned from flows.
- `debug/packet_inspector.py` — hex/annotated packet dump used when `debug_packets=True` is passed into a flow (also via `L2Client.enter(debug=True)`).

### Data flow at a glance
```
L2Client.enter
  └─> LoginFlow.execute         (login_connection + login_crypt + rsa)
        └─> LoginResult {tokens, GameServer, blowfish_key}
  └─> GameFlow.execute          (game_connection + game_crypt)
        └─> GameSession {connection, CharacterInfo}
```

## Conventions specific to this repo

- **Language:** many docstrings and log messages are in Russian — keep the existing language when editing a file rather than translating.
- **Python 3.14** features are fair game; `ruff` is pinned to `target-version = "py314"`.
- Packet classes carry their opcode as a class attribute. When adding a new packet, follow the existing `ClientPacket` / `ServerPacket` subclass pattern and register it where the matching flow dispatches opcodes.
- Integration tests under `tests/test_integration/` may connect to a live server (see defaults: `192.168.0.33:2106`, account `qwerty/qwerty`, `server_id=2`). They will fail in environments without that server — run `tests/test_crypto` and `tests/test_protocol` for offline verification.
- `good_sesion.txt` is a captured reference session used for protocol cross-checking — treat it as read-only test data.
