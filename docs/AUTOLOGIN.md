# Automatic enter-game algorithm

This document describes the exact sequence of steps a client must perform to go from "cold start" to "character walking in the world", using only the configuration inputs `username`, `password`, `loginHost`, `loginPort`, `serverId`, `charSlot`, and `protocol = 273`. Packet layouts are described in [PROTOCOL.md](PROTOCOL.md); crypto primitives are in [CRYPTOGRAPHY.md](CRYPTOGRAPHY.md); constants in [CONSTANTS.md](CONSTANTS.md).

## Sequence diagram

```
Client                 Login Server                     Game Server
  |                         |                                 |
  |--- TCP connect -------->|                                 |
  |<-- Init (0x00) ---------|                                 |
  |--- RequestGGAuth(0x07)->|                                 |
  |<-- GGAuth (0x0B) -------|                                 |
  |--- RequestAuthLogin ----|                                 |
  |    (0x00, RSA creds)    |                                 |
  |<-- LoginOk (0x03) ------|                                 |
  |--- RequestServerList ---|                                 |
  |    (0x05)               |                                 |
  |<-- ServerList (0x04) ---|                                 |
  |--- RequestServerLogin --|                                 |
  |    (0x02)               |                                 |
  |<-- PlayOk (0x07) -------|                                 |
  |--- disconnect --------->|                                 |
  |                         |                                 |
  |--------------- TCP connect ---------------------->|       |
  |                                                   |       |
  |--- ProtocolVersion (0x0E, plaintext) ------------>|       |
  |<-- CryptInit (0x2E, plaintext) --------------------|       |
  |--- AuthRequest (0x2B, encrypted) ---------------->|       |
  |<-- CharSelectionInfo (0x09) -----------------------|       |
  |--- CharacterSelected (0x12, slot=charSlot) ------>|       |
  |<-- CharSelected (0x0B)  OR  UserInfo (0x32) ------|       |
  |--- RequestKeyMapping (0xD0 0x21) ---------------->|       |
  |--- EnterWorld (0x11, 104 zero bytes) ------------>|       |
  |<-- UserInfo (0x32) --------------------------------|       |
  |                                                   |       |
  |======= IN_GAME =========================================|
  |                                                   |       |
  |<-- NetPingRequest (0xD9) --------------------------|       |
  |--- NetPing (0xB1) --------------------------------->      |
  |                ...                                        |
```

## Detailed pseudocode

```
# ---- Phase 1: Login Server ----
loginSock = tcp_connect(loginHost, loginPort)

pkt = read_framed(loginSock)                      # see PROTOCOL.md "Packet framing"
init = blowfish_ecb_decrypt(pkt.body, STATIC_LOGIN_BLOWFISH_KEY)
seed = u32_le(init[len(init)-8 : len(init)-4])
rolling_xor_reverse(init, seed)                   # see CRYPTOGRAPHY.md "NewCrypt rolling XOR"
init = init[ : len(init) - 8]

assert init[0] == 0x00
sessionId          = i32_le(init[1:5])
protocolRev        = i32_le(init[5:9])            # expect 0xC621
scrambledRsaKey    = init[9:137]
# init[137:153] reserved
sessionBlowfishKey = init[153:169]                # 16 bytes

rsaModulus = unscramble_rsa_key(scrambledRsaKey)  # see CRYPTOGRAPHY.md "RSA-1024"
currentLoginKey = sessionBlowfishKey              # switch from static to session key

# --- RequestGGAuth (0x07) ---
# 32-byte body: opcode + sessionId + 19 zeros + GG client tag + 4 zeros.
# The server accepts an all-zero GG tag, so a minimal client may send
# bytes([0x07]) + i32_le(sessionId) + zeros(16) and stop after 21 bytes.
body = bytes([0x07]) + i32_le(sessionId) + zeros(19) + i32_le(0) + zeros(4)
send_login_encrypted(loginSock, body, currentLoginKey)

pkt = read_framed(loginSock)
gg = decrypt_login(pkt.body, currentLoginKey)     # Blowfish + verify checksum
assert gg[0] == 0x0B
ggAuthResponse = i32_le(gg[1:5])

# --- RequestAuthLogin (0x00) ---
# 184-byte body: opcode + 128-byte RSA + sessionId + 16 zeros + i32(8) +
# 3 zeros + 16-byte GG nonce + 4 zeros + i32 GG digest + 4 zeros.
# The server accepts an all-zero trailer, so a minimal client may send
# bytes([0x00]) + rsaCipher + i32_le(0) + i32_le(0) + zeros(8) (137 bytes).
plaintext = zeros(94) + ascii_right_padded(username, 14) + zeros(2)
          + ascii_right_padded(password, 16) + zeros(2)               # 128 bytes
rsaCipher = rsa_encrypt_no_padding(plaintext, rsaModulus, e=65537)    # 128 bytes
body = bytes([0x00]) + rsaCipher
     + i32_le(sessionId) + zeros(16) + i32_le(8) + zeros(3)
     + zeros(16) + zeros(4) + i32_le(0) + zeros(4)
send_login_encrypted(loginSock, body, currentLoginKey)

pkt = read_framed(loginSock)
ok = decrypt_login(pkt.body, currentLoginKey)
if ok[0] == 0x01: abort("LoginFail reason=" + str(ok[1]))
assert ok[0] == 0x03
loginOkId1 = i32_le(ok[1:5])
loginOkId2 = i32_le(ok[5:9])

# --- RequestServerList (0x05) ---
# 24-byte body. The single byte 0x05 at offset 9 is a flag/version marker;
# the trailing 14 bytes are GG-related and may be zero on Mobius.
body = bytes([0x05]) + i32_le(loginOkId1) + i32_le(loginOkId2)
     + bytes([0x05]) + zeros(6) + i32_le(0) + zeros(4)
send_login_encrypted(loginSock, body, currentLoginKey)

pkt = read_framed(loginSock)
sl = decrypt_login(pkt.body, currentLoginKey)
assert sl[0] == 0x04
count = sl[1]; pos = 3
servers = []
for i in 0..count:
    rec = parse_server_record(sl[pos : pos+21])   # see PROTOCOL.md "ServerList"
    pos += 21
    servers.append(rec)

chosen = first(s for s in servers if s.serverId == targetServerId)
if chosen is None: abort("ServerId not found")

# --- RequestServerLogin (0x02) ---
# 24-byte body: opcode + ids + serverId + 6 zeros + i32 GG checksum + 4 zeros.
body = bytes([0x02]) + i32_le(loginOkId1) + i32_le(loginOkId2)
     + bytes([chosen.serverId]) + zeros(6) + i32_le(0) + zeros(4)
send_login_encrypted(loginSock, body, currentLoginKey)

pkt = read_framed(loginSock)
po = decrypt_login(pkt.body, currentLoginKey)
if po[0] == 0x06: abort("PlayFail reason=" + str(po[1]))
assert po[0] == 0x07
playOkId1 = i32_le(po[1:5])
playOkId2 = i32_le(po[5:9])

tcp_close(loginSock)

# ---- Phase 2: Game Server ----
gameSock = tcp_connect(chosen.ip, chosen.port)

# Plaintext ProtocolVersion (0x0E)
send_framed(gameSock, bytes([0x0E]) + i32_le(273))

# Plaintext CryptInit (0x2E), exactly 23 bytes of body
pkt = read_framed(gameSock)
body = pkt.body
assert body[0] == 0x2E and body[1] == 0x01
xorKey        = body[2:10]
encryptionOn  = u32_le(body[10:14]) != 0
staticTail    = bytes([0xC8, 0x27, 0x93, 0x01, 0xA1, 0x6C, 0x31, 0x97])
key_cs = xorKey + staticTail        # 16 bytes
key_sc = xorKey + staticTail
# from now on, encrypt/decrypt with CRYPTOGRAPHY.md "Game XOR stream cipher"

# AuthRequest (0x2B) — first post-CryptInit packet. Encrypted iff encryptionOn;
# HighFive sends encryptionFlag = 0, so this stays plaintext.
nameUtf16 = utf16le(username) + bytes([0x00, 0x00])
body = bytes([0x2B]) + nameUtf16
     + i32_le(playOkId2) + i32_le(playOkId1)    # SWAPPED ORDER!
     + i32_le(loginOkId1) + i32_le(loginOkId2)
send_game_encrypted(gameSock, body, key_cs)

# CharSelectionInfo (0x09)
pkt = read_framed(gameSock); body = decrypt_game(pkt.body, key_sc)
assert body[0] == 0x09
# charCount = u32_le(body[1:5]); per-character records are not needed here.

# CharacterSelected (0x12, slot = charSlot) + 14 zero bytes
body = bytes([0x12]) + i32_le(charSlot) + zeros(14)
send_game_encrypted(gameSock, body, key_cs)

# Either CharSelected (0x0B) or UserInfo (0x32) directly
pkt = read_framed(gameSock); body = decrypt_game(pkt.body, key_sc)
if body[0] == 0x0B:
    # RequestKeyMapping (0xD0 0x21)
    send_game_encrypted(gameSock, bytes([0xD0]) + u16_le(0x0021), key_cs)
    # EnterWorld (0x11) + 104 zero bytes
    send_game_encrypted(gameSock, bytes([0x11]) + zeros(104), key_cs)
    pkt = read_framed(gameSock); body = decrypt_game(pkt.body, key_sc)

assert body[0] == 0x32    # UserInfo
state = IN_GAME

# ---- Phase 3: stay in-game ----
loop forever:
    pkt  = read_framed(gameSock)
    body = decrypt_game(pkt.body, key_sc)
    if body[0] == 0xD9:
        pingId = i32_le(body[1:5])
        # HighFive: opcode 0xB1 + pingId (5-byte body).
        pong   = bytes([0xB1]) + i32_le(pingId)
        send_game_encrypted(gameSock, pong, key_cs)
    else:
        handle_world_packet(body)
```

## Required configuration inputs

| Input       | Typical value | Notes                                                               |
| ----------- | ------------- | ------------------------------------------------------------------- |
| `username`  | string        | Login account                                                       |
| `password`  | string        | Password                                                            |
| `loginHost` | IPv4/DNS      | Login Server address                                                |
| `loginPort` | `2106`        |                                                                     |
| `protocol`  | `273`         | Must match a HighFive-compatible value (also `267`, `268`, `271`)   |
| `serverId`  | `1..255`      | The numeric id of the desired Game Server inside the ServerList     |
| `charSlot`  | `0..6`        | Which existing character to log in as (no auto-create is performed) |

A reimplementer can source these values from any suitable mechanism (configuration file, environment variables, CLI flags, etc.).

## Capture cross-reference

All packet sizes and trailing-block hex strings in the [Login Server protocol section of PROTOCOL.md](PROTOCOL.md#login-server-protocol) were verified
against live L2 official client ↔ HighFive server captures.
Observed packet sizes:

| Direction | Wire | Body | Section | Notes                                |
| --------- | ---- | ---- | ------- | ------------------------------------ |
| S→C       | 196  | 184  | [Init](PROTOCOL.md#init-s-c-opcode-0x00) | Init                                 |
| C→S       | 42   | 32   | [RequestGGAuth](PROTOCOL.md#requestggauth-c-s-opcode-0x07) | RequestGGAuth                        |
| S→C       | 42   | 32   | [GGAuth](PROTOCOL.md#ggauth-s-c-opcode-0x0b) | GGAuth (i32 echoes sessionId)        |
| C→S       | 194  | 184  | [RequestAuthLogin](PROTOCOL.md#requestauthlogin-c-s-opcode-0x00) | RequestAuthLogin                     |
| S→C       | 66   | 56   | [LoginOk](PROTOCOL.md#loginok-s-c-opcode-0x03) | LoginOk                              |
| C→S       | 34   | 24   | [RequestServerList](PROTOCOL.md#requestserverlist-c-s-opcode-0x05) | RequestServerList                    |
| S→C       | 50   | 40   | [ServerList](PROTOCOL.md#serverlist-s-c-opcode-0x04) | ServerList (1 record + 16-byte tail) |
| C→S       | 34   | 24   | [RequestServerLogin](PROTOCOL.md#requestserverlogin-c-s-opcode-0x02) | RequestServerLogin                   |
| S→C       | 26   | 16   | [PlayOk](PROTOCOL.md#playok-s-c-opcode-0x07) | PlayOk                               |
| C→S       | 267  | 265  | [ProtocolVersion](PROTOCOL.md#protocolversion-c-s-opcode-0x0e--plaintext) | ProtocolVersion + 260-byte client tail (server reads only the first 5 bytes) |
| S→C       | 25   | 23   | [CryptInit](PROTOCOL.md#cryptinit-s-c-opcode-0x2e--plaintext) | CryptInit (plaintext, `encryptionFlag = 0`) |
| C→S       | 49   | 47   | [AuthRequest](PROTOCOL.md#authrequest-c-s-opcode-0x2b--first-packet-after-cryptinit-encrypted-iff-cryptinitencryptionflag--0) | AuthRequest (`username="qwerty"`, includes 16-byte trailer) |
| C→S       | 21   | 19   | [CharacterSelected](PROTOCOL.md#characterselected-c-s-opcode-0x12) | CharacterSelected                    |

Body sizes are derived as `wire − 2` for plaintext frames and as
`wire − 2 − pad` for login-encrypted frames, where `pad` is the
4-/8-byte alignment from [Login packet encryption pipelines](CRYPTOGRAPHY.md#login-packet-encryption-pipelines).

## Error handling expected from a correct client

- **Wrong credentials** → LoginFail (`0x01`) with reason code (full table in [LoginFail](PROTOCOL.md#loginfail-s-c-opcode-0x01)); abort.
- **Server not in list** → no record matches `serverId`; abort before sending RequestServerLogin.
- **Server full / down** → PlayFail (`0x06`); abort.
- **Bad protocol version** → CryptInit's `result` byte is not `1`; abort.
- **Character slot empty or out of range** → the server closes the connection after CharacterSelected; the client should surface this as an error (there is no dedicated "char missing" packet).
- **Missing NetPing answer** → server disconnects after a timeout (~60 s). Always answer pings.
