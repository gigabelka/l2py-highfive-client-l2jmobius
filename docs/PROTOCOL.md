# Lineage 2 HighFive — Client ↔ Server Protocol Specification

**Chronicle:** HighFive
**Protocol version:** `273` (also valid: `267`, `268`, `271` — same wire format)
**Scope:** this document describes the complete wire protocol used between a game client and the two servers it talks to (the Login Server and the Game Server). The automatic login sequence is described separately in [AUTOLOGIN.md](AUTOLOGIN.md); cryptographic primitives are described in [CRYPTOGRAPHY.md](CRYPTOGRAPHY.md); constants and opcode tables in [CONSTANTS.md](CONSTANTS.md).

The spec depends on no language feature or library beyond "raw TCP socket", "RSA (no padding)", and "Blowfish ECB".

---

## Overview

A Lineage 2 session has two independent TCP connections, executed strictly in sequence:

1. **Login phase** — client connects to the Login Server on `loginHost:loginPort` (typically port `2106`). The client authenticates with a login/password, receives a list of game servers, picks one, and is issued two pairs of 32-bit session tokens: `loginOkId1/2` and `playOkId1/2`. The client disconnects from the Login Server when this phase is over.

2. **Game phase** — client connects to the selected Game Server on the IP/port returned by the Login Server's ServerList. The client performs a handshake, identifies itself using the 4 session tokens obtained in phase 1, picks a character by slot number, and sends an EnterWorld packet. The server replies with a UserInfo packet which places the character in the world. From that point the connection is long-lived: the server streams world events, the client sends gameplay commands, and both sides periodically exchange keepalive pings.

Whether the game-phase connection is actually encrypted is decided **at runtime by the server**, through the `encryptionFlag` field of the CryptInit packet (see [Game XOR stream cipher](CRYPTOGRAPHY.md#game-xor-stream-cipher) and [CryptInit](#crypt-init-s-c-opcode-0x2e--plaintext)). On HighFive the server leaves this flag at `0`, so a compliant client must be prepared for the entire game session to stay plaintext even though the XOR cipher infrastructure is in place.

```
  +--------+        +--------------+        +-------------+
  | Client |--TCP-->| Login Server |  disc. | Game Server |
  |        |<--6 pkt exchange-->  |------>  |             |
  |        |                                |             |
  |        |--------new TCP connect-------->|             |
  |        |<-------handshake + auth------->|             |
  |        |<======long-lived game session=>|             |
  +--------+                                 +-------------+
```

---

## Common primitives

### Endianness

**Everything is little-endian** unless explicitly noted. This applies to:

- packet length prefix (`u16 LE`),
- all integer fields in every packet (client → server and server → client),
- the 32-bit words inside the NewCrypt checksum,
- the rolling DWORD at bytes 8..11 of the game XOR key.

The two exceptions are:

- **IPv4 address bytes** inside the ServerList record — stored as 4 individual bytes in network (big-endian, `a.b.c.d`) order, not as a single 32-bit integer.
- **RSA modulus** — a big-endian 128-byte integer by convention of the RSA standard. The modulus is additionally scrambled by the server (see [RSA-1024 for credential submission](CRYPTOGRAPHY.md#rsa-1024-for-credential-submission)).

### Primitive types

| Name       | Size       | Notes                                                    |
| ---------- | ---------- | -------------------------------------------------------- |
| `u8`       | 1 byte     | unsigned                                                 |
| `i8`       | 1 byte     | signed                                                   |
| `u16`      | 2 bytes LE | unsigned                                                 |
| `i16`      | 2 bytes LE | signed                                                   |
| `i32`      | 4 bytes LE | signed                                                   |
| `u32`      | 4 bytes LE | unsigned                                                 |
| `i64`      | 8 bytes LE | signed                                                   |
| `f32`      | 4 bytes LE | IEEE-754 single                                          |
| `f64`      | 8 bytes LE | IEEE-754 double                                          |
| `bytes[N]` | N bytes    | raw, no length prefix                                    |
| `str`      | UTF-16LE   | variable, terminated by a `u16 0x0000` — see notes below |

Notes on `str`:

- The encoding is pure **UTF-16LE** with **no byte-order mark** (BOM). Each code unit is 2 bytes little-endian. Characters outside the BMP are encoded as UTF-16 surrogate pairs (4 bytes total); the server treats them as opaque code units, so a client only needs to preserve them byte-for-byte.
- The terminator is exactly **two `0x00` bytes** immediately after the last code unit. It is counted in the field's on-wire length but not in the string's character count.
- An **empty string** encodes as just `00 00` (two bytes total).
- A reader that encounters unterminated data must treat the packet as malformed.
- Fields that precede a `str` are at fixed offsets; fields that follow one can only be located by first scanning forward for the `00 00` terminator. No length prefix is ever used for `str`.

### Packet framing

Every packet on both the Login Server connection and the Game Server connection has the same frame:

```
+---------+-----------------------+
| u16 len | body (len - 2 bytes)  |
+---------+-----------------------+
```

- `len` is little-endian and **includes the 2 bytes of the length field itself**. The minimum legal value is `2` (empty body). The maximum legal value is `0xFFFF = 65 535`, so the maximum body length is `65 533` bytes.
- `body` starts with a 1-byte opcode (or, for extended game packets, a `u8` + `u16 LE` sub-opcode — see [RequestKeyMapping](#requestkeymapping-c-s-extended-opcode-0xd0-0x21)).
- `body` may be encrypted (see [CRYPTOGRAPHY.md](CRYPTOGRAPHY.md)). **Encryption is applied to the body only, never to the length prefix.**
- If the reader ever sees `len < 2`, or if the TCP connection closes mid-body, the connection must be considered desynchronised and closed. There is no in-stream resync marker.

Reassembly algorithm (pseudocode):

```
buf = empty
while socket is open:
    buf += read(socket)
    while len(buf) >= 2:
        n = u16_le(buf[0..2])
        if len(buf) < n: break
        pkt = buf[0..n]
        buf = buf[n..]
        process(pkt)
```

---

## Login Server protocol

### State machine

```
IDLE
  | connect()
  v
CONNECTING
  | TCP established
  v
WAIT_INIT
  | recv Init (0x00) ............ store sessionId, rsaPublicKey, set session Blowfish key
  |   send RequestGGAuth (0x07)
  v
WAIT_GG_AUTH
  | recv GGAuth (0x0B) .......... store ggAuthResponse
  |   send RequestAuthLogin (0x00)
  v
WAIT_LOGIN_OK
  |-- recv LoginFail (0x01) ---> ERROR (abort)
  |-- recv LoginOk  (0x03) ..... store loginOkId1/2
  |       send RequestServerList (0x05)
  v
WAIT_SERVER_LIST
  | recv ServerList (0x04) ..... pick gameServerIp/port by ServerId
  |   send RequestServerLogin (0x02)
  v
WAIT_PLAY_OK
  |-- recv PlayFail (0x06) ---> ERROR (abort)
  |-- recv PlayOk   (0x07) ..... store playOkId1/2
  v
DONE  (disconnect from login server, move to Game Server protocol)
```

### Login Server opcode table

| Opcode | Direction | Name               | Section |
| ------ | --------- | ------------------ | ------- |
| `0x00` | S→C       | Init               | [Init](#init-s-c-opcode-0x00) |
| `0x01` | S→C       | LoginFail          | [LoginFail](#loginfail-s-c-opcode-0x01) |
| `0x03` | S→C       | LoginOk            | [LoginOk](#loginok-s-c-opcode-0x03) |
| `0x04` | S→C       | ServerList         | [ServerList](#serverlist-s-c-opcode-0x04) |
| `0x06` | S→C       | PlayFail           | [PlayFail](#playfail-s-c-opcode-0x06) |
| `0x07` | S→C       | PlayOk             | [PlayOk](#playok-s-c-opcode-0x07) |
| `0x0B` | S→C       | GGAuth             | [GGAuth](#ggauth-s-c-opcode-0x0b) |
| `0x00` | C→S       | RequestAuthLogin   | [RequestAuthLogin](#requestauthlogin-c-s-opcode-0x00) |
| `0x02` | C→S       | RequestServerLogin | [RequestServerLogin](#requestserverlogin-c-s-opcode-0x02) |
| `0x05` | C→S       | RequestServerList  | [RequestServerList](#requestserverlist-c-s-opcode-0x05) |
| `0x07` | C→S       | RequestGGAuth      | [RequestGGAuth](#requestggauth-c-s-opcode-0x07) |

Note that opcodes are not globally unique: `0x00` and `0x07` exist in both directions with different semantics. Always disambiguate by direction.

### Init (S→C, opcode `0x00`)

Decrypted body (after Blowfish + reverse rolling XOR + dropping 8 trailing bytes
that hold the rolling-XOR seed and 4 unused bytes — see [NewCrypt rolling XOR (Init packet only)](CRYPTOGRAPHY.md#newcrypt-rolling-xor-init-packet-only)):

| Offset | Field              | Type         | Size | Notes                                                                      |
| ------ | ------------------ | ------------ | ---- | -------------------------------------------------------------------------- |
| 0      | opcode             | `u8`         | 1    | `0x00`                                                                     |
| 1      | `sessionId`        | `i32`        | 4    | echoed in RequestGGAuth                                                    |
| 5      | `protocolRevision` | `i32`        | 4    | expected `0x0000C621`                                                      |
| 9      | `scrambledRsaKey`  | `bytes[128]` | 128  | must be unscrambled (see [RSA-1024 for credential submission](CRYPTOGRAPHY.md#rsa-1024-for-credential-submission)) |
| 137    | reserved           | `bytes[16]`  | 16   | four random `i32` (GG seed material), ignored by the client                |
| 153    | `blowfishKey`      | `bytes[16]`  | 16   | session key for every subsequent login packet, both directions             |
| 169    | null terminator    | `u8`         | 1    | `0x00` written by the server                                               |

Total server-written payload: **170 bytes**. On the wire
the packet is longer because the login crypto pipeline appends a rolling-XOR
seed (4 bytes), 4 unused bytes, and zero-pads to a Blowfish 8-byte block —
bringing the post-decrypt buffer to **184 bytes**. After `decXORPass` and
dropping the last 8 bytes (see [NewCrypt rolling XOR (Init packet only)](CRYPTOGRAPHY.md#newcrypt-rolling-xor-init-packet-only)) the client sees **176 bytes**, of which only
the first 170 are meaningful. Bytes 170..175 are zero pad and may be ignored.

### LoginFail (S→C, opcode `0x01`)

| Offset | Field    | Type          |
| ------ | -------- | ------------- |
| 0      | opcode   | `u8` = `0x01` |
| 1      | `reason` | `u8`          |

Reason codes (all codes are hex):

| Code   | Meaning                   |
| ------ | ------------------------- |
| `0x01` | System error              |
| `0x02` | Wrong password            |
| `0x03` | Wrong login or password   |
| `0x04` | Access denied             |
| `0x05` | Invalid account info      |
| `0x06` | Access denied (try later) |
| `0x07` | Account already in use    |
| `0x08` | Age restriction           |
| `0x09` | Server full               |
| `0x10` | Maintenance               |
| `0x11` | Temporary ban             |
| `0x23` | Dual box restriction      |

Codes outside this set are logged as `Unknown reason (0x…)` and treated as fatal. On any LoginFail the client must close the connection.

### LoginOk (S→C, opcode `0x03`)

| Offset | Field          | Type        | Notes                                                |
| ------ | -------------- | ----------- | ---------------------------------------------------- |
| 0      | opcode         | `u8` = `0x03` |                                                    |
| 1      | `loginOkId1`   | `i32`       | session token #1                                     |
| 5      | `loginOkId2`   | `i32`       | session token #2                                     |
| 9      | reserved       | `bytes[8]`  | two `writeInt(0)` calls                              |
| 17     | `accessLevel`  | `i32`       | `0x000003EA` for a normal account                    |
| 21     | reserved       | `i32`       | `writeInt(0)`                                        |
| 25     | reserved       | `bytes[16]` | `writeBytes(new byte[16])`                           |

Total server-written payload: **41 bytes**. The wire
body is longer because of login-packet padding (see [Login packet encryption pipelines](CRYPTOGRAPHY.md#login-packet-encryption-pipelines)) — expect ~56 bytes on
the wire after Blowfish padding, NewCrypt checksum etc. A reimplementer
only needs to keep `loginOkId1` and `loginOkId2`; everything from offset 9
onward is opaque and may be skipped.

### ServerList (S→C, opcode `0x04`)

| Offset       | Field             | Type                      | Notes                                          |
| ------------ | ----------------- | ------------------------- | ---------------------------------------------- |
| 0            | opcode            | `u8` = `0x04`             |                                                |
| 1            | `serverCount`     | `u8`                      |                                                |
| 2            | `lastServerId`   | `u8`                      | id of the server the account last logged onto |
| 3 + k·21     | server record `k` | see below (21 bytes each) |                                                |
| 3 + N·21     | trailing block   | variable                  | per-server character counts and account flags |

**Server record (21 bytes):**

| Offset | Field           | Type       | Notes                                                  |
| ------ | --------------- | ---------- | ------------------------------------------------------ |
| 0      | `serverId`      | `u8`       |                                                        |
| 1      | `ip[0..4]`      | `bytes[4]` | IPv4 as `a.b.c.d` (bytes are already in display order) |
| 5      | `port`          | `i32`      |                                                        |
| 9      | `ageLimit`      | `u8`       |                                                        |
| 10     | `isPvp`         | `u8`       | `0`/`1`                                                |
| 11     | `onlinePlayers` | `u16`      |                                                        |
| 13     | `maxPlayers`    | `u16`      |                                                        |
| 15     | `isOnline`      | `u8`       | `0`/`1`                                                |
| 16     | `flags`         | `i32`      | informational                                          |
| 20     | reserved        | `u8`       |                                                        |

A typical 1-server response (40-byte body) shows a 16-byte trailing block
after the single record:
`00 00 01 02 01 00 3e 2d 03 e0 67 16 7f 24 1c 0d`. This block holds the
per-server character count summary and various account flags.
A reimplementer doing auto-login can ignore everything after the matched
server record — the client selects the record whose `serverId` matches
the configured `ServerId` and uses its `ip:port` for the Game Server
connection.

### PlayFail (S→C, opcode `0x06`)

| Offset | Field    | Type          |
| ------ | -------- | ------------- |
| 0      | opcode   | `u8` = `0x06` |
| 1      | `reason` | `u8`          |

Reason codes:

| Code   | Meaning                 |
| ------ | ----------------------- |
| `0x03` | Password mismatch       |
| `0x04` | Access error, try later |
| `0x0F` | Too many players        |

Codes outside this set are logged as `Unknown reason (0x…)`. The legacy Interlude-era table (`0x01` = server full, `0x02` = server down, etc.) is **not** what HighFive sends — a reimplementer must not hard-code it.

### PlayOk (S→C, opcode `0x07`)

| Offset | Field          | Type        | Notes                                              |
| ------ | -------------- | ----------- | -------------------------------------------------- |
| 0      | opcode         | `u8` = `0x07` |                                                  |
| 1      | `playOkId1`    | `i32`       | session token #3                                   |
| 5      | `playOkId2`    | `i32`       | session token #4                                   |

Total server-written payload: **9 bytes**. The wire
body is longer because of login-packet padding (see [Login packet encryption pipelines](CRYPTOGRAPHY.md#login-packet-encryption-pipelines)); the extra bytes are
crypto padding, not packet fields. Both tokens must be remembered — they
are sent later in the game AuthRequest.

### GGAuth (S→C, opcode `0x0B`)

| Offset | Field            | Type        | Notes                                                |
| ------ | ---------------- | ----------- | ---------------------------------------------------- |
| 0      | opcode           | `u8` = `0x0B` |                                                    |
| 1      | `ggAuthResponse` | `i32`       | echoes the `sessionId` from Init                     |
| 5      | reserved         | `bytes[16]` | four `writeInt(0)` calls                             |

Total server-written payload: **21 bytes**. The wire
body is longer because of login-packet padding (see [Login packet encryption pipelines](CRYPTOGRAPHY.md#login-packet-encryption-pipelines)); there is **no**
GameGuard nonce — the extra bytes on the wire are crypto padding.
`ggAuthResponse == sessionId` on every HighFive capture — the
server simply rewrites the first i32 of GGAuth to the
sessionId. A reimplementer can therefore treat `ggAuthResponse` as a
"keep-alive ack" and only needs the i32 itself.

### RequestAuthLogin (C→S, opcode `0x00`)

Body size: **184 bytes** (before padding/encryption). After the [login encryption pipeline](CRYPTOGRAPHY.md#login-packet-encryption-pipelines) this becomes a 192-byte ciphertext + 2-byte length
prefix = 194 bytes on the wire.

| Offset | Field             | Type         | Size | Notes                                              |
| ------ | ----------------- | ------------ | ---- | -------------------------------------------------- |
| 0      | opcode            | `u8`         | 1    | `0x00`                                             |
| 1      | RSA ciphertext    | `bytes[128]` | 128  | computed per [RSA-1024 for credential submission](CRYPTOGRAPHY.md#rsa-1024-for-credential-submission) |
| 129    | `sessionId`       | `i32`        | 4    | echoed from Init                                   |
| 133    | reserved          | `bytes[16]`  | 16   | observed all-zero                                  |
| 149    | constant `0x08`   | `i32`        | 4    | observed `0x00000008` on every capture             |
| 153    | reserved          | `bytes[3]`   | 3    | observed all-zero (note unaligned)                 |
| 156    | GG random nonce   | `bytes[16]` | 16   | per-session 16-byte blob from the GameGuard layer  |
| 172    | reserved          | `bytes[4]`   | 4    | observed all-zero                                  |
| 176    | GG auth digest    | `i32`        | 4    | per-session i32 derived from the GameGuard challenge |
| 180    | reserved          | `bytes[4]`   | 4    | observed all-zero                                  |

The 128-byte RSA ciphertext is computed per [RSA-1024 for credential submission](CRYPTOGRAPHY.md#rsa-1024-for-credential-submission) from the login, password,
and the unscrambled modulus from Init. The trailing 55 bytes after the
ciphertext are GameGuard-related — HighFive does not validate
them and accepts an all-zero blob, so a reimplementer that does not need
to defeat real GameGuard may transmit zeros for everything from offset 129
onward.

**Alternative "new auth" mode (optional on the server).**
The server supports a `newAuthMethod` branch that expects
**two** 128-byte RSA ciphertexts concatenated (256 bytes total) with this
plaintext layout across the decrypted 256-byte buffer:

| Offset    | Size | Content                         |
| --------- | ---- | ------------------------------- |
| `0x4E`    | 50   | login part 1, ASCII null-padded |
| `0xCE`    | 14   | login part 2, ASCII null-padded |
| `0xDC`    | 16   | password, ASCII null-padded     |

The effective login is `trim(part1) + trim(part2)`. This mode is enabled
via a server admin flag; HighFive leaves it **disabled** by default, so the single-block form
described above is what real servers accept. A reimplementer only needs
the dual-block form if they integrate with a server that explicitly opts
into new-auth.

Trailing 55 bytes (offsets 129..183), captured from a real official client:

```
c0 00 a0 1a 00 00 00 00 00 00 00 00 00 00 00 00
00 00 00 00 00 08 00 00 00 00 00 00 c1 d4 52 30
ed 19 5f 2b d2 ed 9f e7 2b 31 04 39 00 00 00 00
38 ee 4a 6a 00 00 00 00
```

### RequestServerLogin (C→S, opcode `0x02`)

Body size: **24 bytes** (before padding/encryption). Wire = 34 bytes.

| Offset | Field          | Type         | Notes                                              |
| ------ | -------------- | ------------ | -------------------------------------------------- |
| 0      | opcode         | `u8` = `0x02` |                                                  |
| 1      | `loginOkId1`   | `i32`        | from LoginOk                                       |
| 5      | `loginOkId2`   | `i32`        | from LoginOk                                       |
| 9      | `serverId`     | `u8`         | id of the chosen Game Server                       |
| 10     | reserved       | `bytes[6]`   | observed all-zero                                  |
| 16     | GG checksum    | `i32`        | per-session GameGuard tag (observed `0x5E400B0F`) |
| 20     | reserved       | `bytes[4]`   | observed all-zero                                  |

The trailing 14 bytes (offsets 10..23) are GameGuard padding. The server
accepts a 10-byte body (just opcode+ids+serverId) as well, which is the
recommended minimal form for a reimplementer.

### RequestServerList (C→S, opcode `0x05`)

Body size: **24 bytes** (before padding/encryption). Wire = 34 bytes.

| Offset | Field          | Type         | Notes                                              |
| ------ | -------------- | ------------ | -------------------------------------------------- |
| 0      | opcode         | `u8` = `0x05` |                                                  |
| 1      | `loginOkId1`   | `i32`        | from LoginOk                                       |
| 5      | `loginOkId2`   | `i32`        | from LoginOk                                       |
| 9      | trailing block | `bytes[15]`  | observed `0x05`, 6 zeros, GG tag i32, 4 zeros     |

The server only reads the two i32 session tokens (it checks `remaining() >= 8`
and reads two ints), so everything from offset 9
onward is ignored by the server. The server accepts a **9-byte body**
(`opcode + loginOkId1 + loginOkId2`), which is the recommended minimal
form. The `0x05` byte at offset 9 observed on wire from the official
client is not a required flag/version marker.

### RequestGGAuth (C→S, opcode `0x07`)

Body size: **32 bytes** (before padding/encryption). Wire = 42 bytes.

| Offset | Field            | Type         | Notes                                         |
| ------ | ---------------- | ------------ | --------------------------------------------- |
| 0      | opcode           | `u8`         | `0x07`                                        |
| 1      | `sessionId`      | `i32`        | echoed from Init                              |
| 5      | reserved         | `bytes[19]`  | observed all-zero                             |
| 24     | GG client tag    | `i32`        | per-session GameGuard derivative              |
| 28     | reserved         | `bytes[4]`   | observed all-zero                             |

The 4-byte "GG client tag" at offset 24 is computed by the official
client's GameGuard module from the `sessionId`. A sample observed value
was `0xA000C01D` for `sessionId = 0x1AA000C0` (sessionId rotated
right one byte and the high byte XOR'd with `0x07`). HighFive
does not validate this tag and accepts an all-zero blob, so a
reimplementer that does not need to defeat real GameGuard may transmit a
21-byte body with just `opcode + sessionId + 16 zero bytes`.

The four magic constants `0x123 / 0x4567 / 0x89AB / 0xCDEF` documented for
older chronicles do **not** appear in HighFive captures.

### Annotated hex dumps

The dumps below are synthetic but internally consistent: every offset add-up can be verified by hand. They all show the **decrypted** body (so the `u16 LE` length prefix is omitted — prepend `len = body + 2` when framing). Use them to cross-check your serializer's offsets against the authoritative specification.

**Init (S→C, `0x00`) — 184 bytes** (see [Init](#init-s-c-opcode-0x00)). The 128-byte scrambled RSA key and the 16-byte session Blowfish key are abbreviated as dotted runs for readability; both are opaque to the framer.

```
00                                               ; opcode = 0x00
44 33 22 11                                      ; sessionId        = 0x11223344
21 C6 00 00                                      ; protocolRevision = 0x0000C621
<128 bytes scrambledRsaKey>                      ; offsets 0x09..0x88
<16 bytes reserved, ignored>                     ; offsets 0x89..0x98
<16 bytes blowfishKey (session)>                 ; offsets 0x99..0xA8
00 00 00 00 00 5B A8 44 F7 00 00 00 00 00 00     ; trailing block, offsets 0xA9..0xB7
```

**LoginOk (S→C, `0x03`) — 56 bytes** (see [LoginOk](#loginok-s-c-opcode-0x03)).

```
03                                               ; opcode = 0x03
DD CC BB AA                                      ; loginOkId1 = 0xAABBCCDD
44 33 22 11                                      ; loginOkId2 = 0x11223344
00 00 00 00 00 00 00 00                          ; reserved (offsets 0x09..0x10)
EA 03 00 00                                      ; accessLevel = 0x000003EA
<31 trailing bytes — opaque>                     ; offsets 0x15..0x37
```

**ServerList (S→C, `0x04`) with one record — 40 bytes** (see [ServerList](#serverlist-s-c-opcode-0x04)). The 16-byte trailing block is reproduced verbatim from an observed 1-server response.

```
04                                               ; opcode = 0x04
01                                               ; serverCount = 1
02                                               ; lastServerId = 2

; --- server record 0 (21 bytes) ---
02                                               ; serverId = 2
C0 A8 00 21                                      ; ip = 192.168.0.33 (bytes in display order)
61 1E 00 00                                      ; port = 7777 (i32 LE)
00                                               ; ageLimit
01                                               ; isPvp = true
00 00                                            ; onlinePlayers = 0 (u16 LE)
D0 07                                            ; maxPlayers    = 2000 (u16 LE)
01                                               ; isOnline = true
40 00 00 00                                      ; flags = 0x40 (i32 LE)
00                                               ; reserved

; --- trailing block (16 bytes, opaque) ---
00 00 01 02 01 00 3E 2D 03 E0 67 16 7F 24 1C 0D
```

**GGAuth (S→C, `0x0B`) — 32 bytes** (see [GGAuth](#ggauth-s-c-opcode-0x0b)).

```
0B                                               ; opcode = 0x0B
C0 00 A0 1A                                      ; ggAuthResponse echoes sessionId = 0x1AA000C0
00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00  ; 16 reserved zero bytes
55 69 30 14 6F 79 17 AC F1 76 ad                 ; 11-byte GG nonce
```

**LoginFail (S→C, `0x01`) — 2 bytes** (see [LoginFail](#loginfail-s-c-opcode-0x01)).

```
01                                               ; opcode = 0x01
03                                               ; reason = 0x03 "Wrong login or password"
```

**PlayOk (S→C, `0x07`) — 16 bytes** (see [PlayOk](#playok-s-c-opcode-0x07)).

```
07                                               ; opcode = 0x07
78 56 34 12                                      ; playOkId1 = 0x12345678
F0 DE BC 9A                                      ; playOkId2 = 0x9ABCDEF0
<7 trailing bytes — opaque GG/queue data>        ; offsets 0x09..0x0F
```

**PlayFail (S→C, `0x06`) — 2 bytes** (see [PlayFail](#playfail-s-c-opcode-0x06)). The server writes the reason as a single byte.

```
06                                               ; opcode = 0x06
0F                                               ; reason = 0x0F "Too many players"
```

**RequestAuthLogin (C→S, `0x00`) — 184 bytes, pre-encryption** (see [RequestAuthLogin](#requestauthlogin-c-s-opcode-0x00)). The RSA ciphertext is 128 opaque bytes; the trailing 55 bytes shown below are reproduced verbatim from an observed capture.

```
00                                               ; opcode = 0x00
<128 bytes RSA ciphertext>                       ; offsets 0x01..0x80
C0 00 A0 1A                                      ; sessionId echo (offset 0x81)
00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00  ; reserved (offsets 0x85..0x94)
08 00 00 00                                      ; constant 0x08 (offset 0x95)
00 00 00                                         ; reserved 3 bytes (offsets 0x99..0x9B)
C1 D4 52 30 ED 19 5F 2B D2 ED 9F E7 2B 31 04 39  ; GG random nonce (0x9C..0xAB)
00 00 00 00                                      ; reserved (0xAC..0xAF)
38 EE 4A 6A                                      ; GG auth digest (0xB0..0xB3)
00 00 00 00                                      ; reserved (0xB4..0xB7)
```

**RequestGGAuth (C→S, `0x07`) — 32 bytes, pre-encryption** (see [RequestGGAuth](#requestggauth-c-s-opcode-0x07)).

```
07                                               ; opcode = 0x07
C0 00 A0 1A                                      ; sessionId echo = 0x1AA000C0
00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00  ; 16 zero bytes (offsets 0x05..0x14)
00 00 00                                         ; 3 more zero bytes (offsets 0x15..0x17)
1D C0 00 A0                                      ; GG client tag (offset 0x18)
00 00 00 00                                      ; reserved (offsets 0x1C..0x1F)
```

**RequestServerList (C→S, `0x05`) — 24 bytes, pre-encryption** (see [RequestServerList](#requestserverlist-c-s-opcode-0x05)).

```
05                                               ; opcode = 0x05
0B 2C 55 DF                                      ; loginOkId1 = 0xDF552C0B
02 6C 0B D2                                      ; loginOkId2 = 0xD20B6C02
05                                               ; constant 0x05 (offset 0x09)
00 00 00 00 00 00                                ; reserved (offsets 0x0A..0x0F)
08 0C 40 5E                                      ; GG checksum (offset 0x10)
00 00 00 00                                      ; reserved (offsets 0x14..0x17)
```

**RequestServerLogin (C→S, `0x02`) — 24 bytes, pre-encryption** (see [RequestServerLogin](#requestserverlogin-c-s-opcode-0x02)).

```
02                                               ; opcode = 0x02
0B 2C 55 DF                                      ; loginOkId1 = 0xDF552C0B
02 6C 0B D2                                      ; loginOkId2 = 0xD20B6C02
02                                               ; serverId = 2
00 00 00 00 00 00                                ; reserved (offsets 0x0A..0x0F)
0F 0B 40 5E                                      ; GG checksum (offset 0x10)
00 00 00 00                                      ; reserved (offsets 0x14..0x17)
```

All C→S login bodies above are then padded and encrypted per [Login packet encryption pipelines](CRYPTOGRAPHY.md#login-packet-encryption-pipelines) before
being framed with a `u16 LE` length. The exact 4-byte GG blobs differ per
session — they are shown here only to anchor the field offsets.

---

## Game Server protocol

### State machine

```
IDLE
  | connect()
  v
CONNECTING
  | TCP established
  |   send ProtocolVersion (0x0E)   -- plaintext
  v
WAIT_CRYPT_INIT
  | recv CryptInit (0x2E)            -- plaintext
  |   init XOR cipher
  |   send AuthRequest (0x2B)        -- first encrypted packet
  v
WAIT_CHAR_LIST
  | recv CharSelectionInfo (0x09)
  |   send CharacterSelected (0x12, slot = configured char slot)
  v
WAIT_CHAR_SELECTED
  |-- recv CharSelected (0x0B) ----.
  |-- recv UserInfo (0x32) direct -+--> fall through to IN_GAME steps
  |                                |
  |   send RequestKeyMapping (0xD0 0x21)
  |   send EnterWorld (0x11)
  v
WAIT_USER_INFO
  | recv UserInfo (0x32)
  v
IN_GAME
  | handle world packets, send gameplay packets,
  | answer NetPingRequest (0xD9) with NetPing (0xB1)
  v
(disconnect) -> ERROR / DISCONNECTED
```

### Framing and encryption

- Packet framing is identical to the login server (see [Packet framing](#packet-framing)): `u16 LE length` prefix that includes itself, followed by the body.
- The body is encrypted with the 16-byte XOR stream cipher (see [Game XOR stream cipher](CRYPTOGRAPHY.md#game-xor-stream-cipher)) **except for the very first packet in each direction**: client's ProtocolVersion and server's CryptInit are plaintext.
- There is **no** per-packet checksum on the game stream (in contrast to the login stream). Integrity is implicit: a wrong byte desynchronizes the stream cipher and corrupts all following packets.

### Handshake packets

Every multi-byte field below is little-endian. Opcodes are the first byte of the _decrypted_ body.

#### ProtocolVersion (C→S, opcode `0x0E`) — plaintext

| Offset | Field          | Type         | Value  |
| ------ | -------------- | ------------ | ------ |
| 0      | opcode         | `u8`         | `0x0E` |
| 1      | `protocol`     | `i32`        | `273`  |
| 5      | trailing block | `bytes[260]` | client build-info / hardware fingerprint, opaque |

HighFive only consumes the first 5 bytes. The official client
nonetheless sends a 265-byte body (267 bytes on the wire). A reimplementer may transmit only the 5-byte minimum form
and the server will accept it.

#### CryptInit (S→C, opcode `0x2E`) — plaintext

23-byte packet (body, without the 2-byte length prefix):

| Offset | Field            | Type       | Notes                                                   |
| ------ | ---------------- | ---------- | ------------------------------------------------------- |
| 0      | opcode           | `u8`       | `0x2E`                                                  |
| 1      | `result`         | `u8`       | must be `1` for success; any other value is a rejection |
| 2      | `xorKey`         | `bytes[8]` | first 8 bytes of the stream cipher key                  |
| 10     | `encryptionFlag` | `u32`      | non-zero → encryption enabled for subsequent packets    |
| 14     | reserved         | `bytes[9]` | ignored                                                 |

After receiving CryptInit, the client builds `key_cs` and `key_sc` as `xorKey || staticTail` (see [Game XOR stream cipher](CRYPTOGRAPHY.md#game-xor-stream-cipher)) and enables encryption according to `encryptionFlag`.

**HighFive quirk:** the server sends `encryptionFlag = 0`, which disables the XOR stream cipher for the entire session — every subsequent packet (including AuthRequest) travels as plaintext. A correct client must honor this flag and only apply the XOR cipher when it is non-zero.

A clean way to structure the crypt layer is to pass `encryptionFlag` into an `initKey(xorKeyData, useEncryption)` method and have `encrypt`/`decrypt` short-circuit to the identity function when `useEncryption = false`. In other words, a reimplementer is not required to special-case "encryption disabled" in the packet dispatcher — a no-op crypt object is the cleanest factoring.

#### AuthRequest (C→S, opcode `0x2B`) — first packet after CryptInit (encrypted iff `CryptInit.encryptionFlag ≠ 0`)

| Offset | Field          | Type        | Notes                                           |
| ------ | -------------- | ----------- | ----------------------------------------------- |
| 0      | opcode         | `u8`        | `0x2B`                                          |
| 1      | `username`     | `str`       | UTF-16LE, 2-byte null terminator                |
| var    | `playOkId2`    | `i32`       | **note the swapped order**                      |
| var+4  | `playOkId1`    | `i32`       |                                                 |
| var+8  | `loginOkId1`   | `i32`       |                                                 |
| var+12 | `loginOkId2`   | `i32`       |                                                 |
| var+16 | trailing block | `bytes[16]` | observed `01 00 00 00 15 02 00 00 00 …` (opaque) |

**The field order `play2, play1, login1, login2` is mandatory** — getting
it wrong silently breaks auth. The 16-byte trailing block
is sent by the official client (observed as a 49-byte body for
`username = "qwerty"`); the server does not read past
`loginOkId2`, so a reimplementer may omit the trailer entirely.

#### CharSelectionInfo (S→C, opcode `0x09`)

| Offset | Field             | Type          |
| ------ | ----------------- | ------------- |
| 0      | opcode            | `u8` = `0x09` |
| 1      | `charCount`       | `u32`         |
| 5      | character records | variable      |

The auto-login algorithm does not need to parse character records; it simply picks `CONFIG.CharSlotIndex` (default `0`) and sends CharacterSelected. A reimplementer that wants to display the character list must parse each record: per-character data includes the character name (UTF-16LE string), character id (`i32`), access level (`i32`), class id (`i32`), last used flag, and a variable-length block with appearance, stats, and equipment. The layout is stable across HighFive builds but is irrelevant for auto-entering the world, so its full decoding is out of scope here.

#### CharacterSelected (C→S, opcode `0x12`)

Total body size: **19 bytes** (1 opcode + 4 `slotIndex` + 14 zero pad).

| Offset | Field       | Type        | Value     |
| ------ | ----------- | ----------- | --------- |
| 0      | opcode      | `u8`        | `0x12`    |
| 1      | `slotIndex` | `i32`       | 0-based   |
| 5      | `_unk1`     | `i16`       | zero      |
| 7      | `_unk2`     | `i32`       | zero      |
| 11     | `_unk3`     | `i32`       | zero      |
| 15     | `_unk4`     | `i32`       | zero      |

The trailing 14 bytes are read by the server as four typed fields
(one `i16` + three `i32`) and will cause a
`BufferUnderflowException` if absent. Total body size is **19 bytes**. All
four fields are carried over from the C4 client and are simply discarded by
the server, so a client may transmit zeros.

#### CharSelected (S→C, opcode `0x0B`)

Confirmation that the selected character was loaded. The body beyond the opcode is not required by the client; the presence of the opcode in state `WAIT_CHAR_SELECTED` triggers sending RequestKeyMapping and EnterWorld.

**Important quirk:** some server builds skip CharSelected and send UserInfo (`0x32`) directly. The client must therefore also accept UserInfo while still in `WAIT_CHAR_SELECTED` and promote the state machine straight to IN_GAME.

#### RequestKeyMapping (C→S, extended opcode `0xD0 0x21`)

| Offset | Field       | Type  | Value    |
| ------ | ----------- | ----- | -------- |
| 0      | main opcode | `u8`  | `0xD0`   |
| 1      | sub-opcode  | `u16` | `0x0021` |

This is the canonical "extended packet" form used by L2 from Interlude onwards: a 1-byte primary opcode (`0xD0`) followed by a 2-byte LE sub-opcode.

#### EnterWorld (C→S, opcode `0x11`)

Total body size: **105 bytes** (1 opcode + 104 zero pad).

| Offset | Field   | Type         | Value     |
| ------ | ------- | ------------ | --------- |
| 0      | opcode  | `u8`         | `0x11`    |
| 1      | padding | `bytes[104]` | all zeros |

**The 104 zero bytes are mandatory** — the server parses them as a hardware info / traceroute blob and will throw `BufferUnderflowException` otherwise.

#### UserInfo (S→C, opcode `0x32`)

Large packet containing the player's current state. The fields relevant for reaching IN_GAME are the first ones; the rest are used by the world simulation and can be decoded incrementally.

Initial fields (byte offsets within the decrypted body):

| Offset | Field                   | Type          | Notes                                            |
| ------ | ----------------------- | ------------- | ------------------------------------------------ |
| 0      | opcode                  | `u8` = `0x32` |                                                  |
| 1      | `x`                     | `i32`         | spawn X                                          |
| 5      | `y`                     | `i32`         | spawn Y                                          |
| 9      | `z`                     | `i32`         | spawn Z                                          |
| 13     | `vehicleId`             | `i32`         | `0` if unmounted                                 |
| 17     | `objectId`              | `i32`         | unique id of the player's character in the world |
| 21     | `name`                  | `str`         | UTF-16LE + null terminator                       |
| var    | `race`                  | `i32`         |                                                  |
| var+4  | `sex`                   | `i32`         | `0`=male, `1`=female                             |
| var+8  | `classId`               | `i32`         |                                                  |
| var+12 | `level`                 | `i32`         |                                                  |
| var+16 | `exp`                   | `i64`         |                                                  |
| ...    | STR/DEX/CON/INT/WIT/MEN | `i32` × 6     |                                                  |
| ...    | `maxHp`, `curHp`        | `i32` × 2     |                                                  |
| ...    | `maxMp`, `curMp`        | `i32` × 2     |                                                  |
| ...    | `maxCp`, `curCp`        | `i32` × 2     |                                                  |
| ...    | `sp`                    | `i32`         |                                                  |
| ...    | `curLoad`, `maxLoad`    | `i32` × 2     |                                                  |

The fields after `maxLoad` contain inventory paperdoll slots, abnormal effects, PvP info, etc. They are not needed for the auto-login to report "in game". A reimplementer can treat everything after the first `~24` fields as opaque until it chooses to parse specific features.

### Keepalive

The server periodically sends NetPingRequest; the client must answer promptly with NetPing or the server will close the connection.

#### NetPingRequest (S→C, opcode `0xD9`)

| Offset | Field    | Type          |
| ------ | -------- | ------------- |
| 0      | opcode   | `u8` = `0xD9` |
| 1      | `pingId` | `i32`         |

Earlier protocol drafts (and most public L2 documentation) list this packet
at `0xD3`, but on HighFive `0xD3 = EARTHQUAKE` and the
ping request moved to `0xD9`.

#### NetPing (C→S, opcode `0xB1`)

**Observed on the wire: 5-byte body.** A minimal ping reply writes just the opcode and the echoed `pingId`:

| Offset | Field    | Type  | Value                    |
| ------ | -------- | ----- | ------------------------ |
| 0      | opcode   | `u8`  | `0xB1`                   |
| 1      | `pingId` | `i32` | echo from NetPingRequest |

On HighFive the server opcode handler for the C→S ping is at `0xB1`.
Some earlier chronicle documentation lists the C→S ping at `0xA8`;
on HighFive `0xA8 = REQUEST_PACKAGE_SEND`, so sending a ping at `0xA8`
will reach the wrong handler.

### Representative gameplay packets

These packets are not required to enter the world, but are included so that a reimplementer knows the pattern used for common commands. All are subject to the XOR cipher when [CryptInit](#cryptinit-s-c-opcode-0x2e--plaintext)'s `encryptionFlag` is non-zero.

C→S opcodes for HighFive. Earlier L2 chronicles (Interlude, Gracia, etc.) use
different numbers — do **not** port opcodes from Interlude-era documentation.

| Opcode        | Name                               | Body (beyond opcode)                                                                                                 |
| ------------- | ---------------------------------- | -------------------------------------------------------------------------------------------------------------------- |
| `0x01`        | AttackRequest (basic)              | `i32 objectId, i32 originX, i32 originY, i32 originZ, u8 shiftClick` (see also `0x32`, aliased class)                |
| `0x0F`        | MoveToLocation                     | `i32 targetX, i32 targetY, i32 targetZ, i32 originX, i32 originY, i32 originZ, i32 movementMode` (`1` = mouse click) |
| `0x14`        | RequestItemList                    | _(no body — just the opcode)_                                                                                        |
| `0x17`        | RequestDropItem                    | `i32 objectId, i64 count, i32 x, i32 y, i32 z`                                                                       |
| `0x19`        | UseItem                            | `i32 itemObjectId, i32 ctrlPressed`                                                                                  |
| `0x1F`        | Action                             | `i32 objectId, i32 originX, i32 originY, i32 originZ, u8 shiftClick`                                                 |
| `0x32`        | AttackRequest                      | same body as `0x01`; both opcodes dispatch to `AttackRequest` class                                                  |
| `0x39`        | RequestMagicSkillUse               | `i32 skillId, i32 ctrlPressed, u8 shiftPressed`                                                                      |
| `0x42`        | RequestJoinParty                   | `str playerName, i32 itemDistribution`                                                                               |
| `0x49`        | Say2                               | `str text, i32 chatType, str target` — `target` is only read when `chatType` = `2` (whisper)                         |
| `0x57`        | RequestRestart                     | _(no body)_                                                                                                          |
| `0x62`        | RequestQuestList                   | _(no body)_                                                                                                          |
| `0x63`        | RequestQuestAbort                  | `i32 questId`                                                                                                        |
| `0xB1`        | NetPing                            | `i32 pingId` — see [NetPing](#netping-c-s-opcode-0xb1)                                                               |
| `0xD0 …`      | extended packets                   | all extended C→S packets, including RequestKeyMapping (`0x0021`)                                                     |

**Opcode `0x14` is NOT overloaded on HighFive.** It is only
`RequestItemList` with no body. `UseItem` has its own opcode (`0x19`). The
"overload by body length" behaviour is an Interlude-era artefact and does
not apply here.

**Extended packet `0xD0 0x0001` = `RequestManorList`.** The often-cited
subopcode `0x0008` for "EnterGameServer / RequestManorList" is an
Interlude-era carryover and is absent from HighFive. A reimplementer
does not need to send an `EnterGameServer` packet at all — the HighFive
server drives the transition from character selection to world through
`EnterWorld (0x11)`.

**RequestSocialAction** has opcode `0x34` on HighFive but the server
handler is not routed. Social actions are therefore effectively
unsupported by the HighFive server build; the id table below is retained
only as protocol-level reference, and action ids are sent via other means
(e.g. `RequestActionUse 0x56`).

**Social action ids** (body is `i32`).

| Id   | Action           |
| ---- | ---------------- |
| `1`  | Stand/Sit toggle |
| `2`  | Greeting         |
| `3`  | Victory          |
| `4`  | Advance          |
| `5`  | No               |
| `6`  | Yes              |
| `7`  | Bow              |
| `8`  | Unaware          |
| `9`  | Waiting          |
| `10` | Laugh            |
| `11` | Think            |
| `12` | Applaud          |
| `13` | Dance            |

These suffice to implement movement, combat, inventory use, chat, skill casting, and basic social actions. Additional opcodes can be added incrementally.

### Server-to-client packets beyond the handshake

Once the client reaches `IN_GAME`, the server begins streaming a large set of opcodes (inventory updates, spawn/despawn, chat, system messages, skill results, etc.) that this specification does not enumerate. A complete reimplementation is not required to decode them, but it **is** required to stay in sync with the encryption stream — which means every incoming packet must be:

1. **Framed** using the `u16 LE` length prefix (see [Packet framing](#packet-framing)).
2. **Decrypted** with `key_sc` (see [Game XOR stream cipher](CRYPTOGRAPHY.md#game-xor-stream-cipher)), and `key_sc[8..12]` must be rotated by the packet's body size **regardless of whether the opcode is recognised**. Skipping the rotation for unknown packets will silently desynchronise subsequent packets.
3. **Dispatched** by opcode. Unknown opcodes should be logged at `WARN` level but **must not** trigger a disconnect — the server regularly sends build-specific opcodes a HighFive-only client has never seen.

The two opcodes a minimal client **must** handle after `IN_GAME`:

- `0xD9` **NetPingRequest** — reply with NetPing (`0xB1`, see [Keepalive](#keepalive)) or the server will drop the connection after ~60 seconds.
- `0x32` **UserInfo** — sent periodically with updated player state; parse at least the leading fields described in [UserInfo](#userinfo-s-c-opcode-0x32) to keep the simulated world up to date.

Everything else can be treated as opaque until the client chooses to decode a specific feature.
