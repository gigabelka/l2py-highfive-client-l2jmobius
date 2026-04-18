# Lineage 2 HighFive — Client ↔ Server Protocol Specification

**Chronicle:** HighFive
**Protocol version:** `273` (also valid: `267`, `268`, `271` — same wire format)
**Server flavor:** L2J Mobius (CT 2.6 HighFive)
**Scope:** this document describes the complete wire protocol used between a game client and the two servers it talks to (the Login Server and the Game Server), plus the exact sequence of packets needed to automatically log in and enter the world as a character. It is language-agnostic and is intended to let another developer (or another LLM) re-implement a working client in any language.

File paths are cited only for cross-checking; the spec itself does not depend on any language feature or library beyond "raw TCP socket", "RSA (no padding)", and "Blowfish ECB".

---

## 1. Overview

A Lineage 2 session has two independent TCP connections, executed strictly in sequence:

1. **Login phase** — client connects to the Login Server on `loginHost:loginPort` (typically port `2106`). The client authenticates with a login/password, receives a list of game servers, picks one, and is issued two pairs of 32-bit session tokens: `loginOkId1/2` and `playOkId1/2`. The client disconnects from the Login Server when this phase is over.

2. **Game phase** — client connects to the selected Game Server on the IP/port returned by the Login Server's ServerList. The client performs a handshake, identifies itself using the 4 session tokens obtained in phase 1, picks a character by slot number, and sends an EnterWorld packet. The server replies with a UserInfo packet which places the character in the world. From that point the connection is long-lived: the server streams world events, the client sends gameplay commands, and both sides periodically exchange keepalive pings.

Whether the game-phase connection is actually encrypted is decided **at runtime by the server**, through the `encryptionFlag` field of the CryptInit packet (see §3.7 and §5.3.2). L2J Mobius CT 2.6 HighFive leaves this flag at `0`, so a compliant client must be prepared for the entire game session to stay plaintext even though the XOR cipher infrastructure is in place.

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

## 2. Common primitives

### 2.1 Endianness

**Everything is little-endian** unless explicitly noted. This applies to:

- packet length prefix (`u16 LE`),
- all integer fields in every packet (client → server and server → client),
- the 32-bit words inside the NewCrypt checksum,
- the rolling DWORD at bytes 8..11 of the game XOR key.

The two exceptions are:

- **IPv4 address bytes** inside the ServerList record — stored as 4 individual bytes in network (big-endian, `a.b.c.d`) order, not as a single 32-bit integer.
- **RSA modulus** — a big-endian 128-byte integer by convention of the RSA standard. The modulus is additionally scrambled by the server (see §3.4).

### 2.2 Primitive types

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

- The encoding is pure **UTF-16LE** with **no byte-order mark** (BOM). Each code unit is 2 bytes little-endian. Characters outside the BMP are encoded as UTF-16 surrogate pairs (4 bytes total); L2J Mobius treats them as opaque code units, so a client only needs to preserve them byte-for-byte.
- The terminator is exactly **two `0x00` bytes** immediately after the last code unit. It is counted in the field's on-wire length but not in the string's character count.
- An **empty string** encodes as just `00 00` (two bytes total).
- A reader that encounters unterminated data must treat the packet as malformed.
- Fields that precede a `str` are at fixed offsets; fields that follow one can only be located by first scanning forward for the `00 00` terminator. No length prefix is ever used for `str`.

### 2.3 Packet framing

Every packet on both the Login Server connection and the Game Server connection has the same frame:

```
+---------+-----------------------+
| u16 len | body (len - 2 bytes)  |
+---------+-----------------------+
```

- `len` is little-endian and **includes the 2 bytes of the length field itself**. The minimum legal value is `2` (empty body). The maximum legal value is `0xFFFF = 65 535`, so the maximum body length is `65 533` bytes.
- `body` starts with a 1-byte opcode (or, for extended game packets, a `u8` + `u16 LE` sub-opcode — see §5.3.7).
- `body` may be encrypted (see §3). **Encryption is applied to the body only, never to the length prefix.**
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

## 3. Cryptography

Three independent cryptographic primitives are used: Blowfish (login phase), RSA-1024 with no padding (credential submission only), and an L2-specific 16-byte XOR stream cipher (game phase).

### 3.1 Blowfish (login phase)

Standard Blowfish in **ECB mode**, 16 Feistel rounds, 64-bit block, P-array of 18 DWORDs, 4 S-boxes of 256 DWORDs each. Any production Blowfish library will work; the L2 protocol uses no tweaks.

- **Block size:** 8 bytes. All login packets to be encrypted/decrypted are padded to a multiple of 8 bytes before encryption and are whole-number-of-8-blocks after decryption.
- **Byte order inside a block:** Blowfish internally consumes two 32-bit halves. The L2 implementation uses **little-endian** `bytesTo32Bits`, which is the standard OpenSSL / Bouncy Castle convention for packet-based Blowfish.
- **Key length:** 16 bytes (both the static login key and the session key returned in Init).

### 3.2 NewCrypt XOR checksum (login phase, post-Init)

Every login packet after Init is protected by a 32-bit XOR checksum written in the last 4 bytes of the (already-padded) body.

**Compute / verify algorithm** (little-endian, 4-byte DWORDs):

```
sum = 0
for i in 0, 4, 8, ..., size - 8:       # every DWORD except the last one
    sum ^= u32_le(raw[i..i+4])
# last 4 bytes of raw hold the checksum (or must be overwritten with `sum`)
```

The `size` MUST be a multiple of 4 and strictly greater than 4.

### 3.3 NewCrypt rolling XOR (Init packet only)

The Init packet uses a rolling XOR applied _in addition to_ the Blowfish decryption. The rolling XOR is a one-pass operation over the 4-byte DWORDs of the body, walked **from the end toward the beginning**, with a feedback loop:

```
size = len(body)
seed = u32_le(body[size - 8 .. size - 4])     # 4-byte seed (the 8 bytes at the tail
                                              # are reserved: seed then 4 unused bytes)
key  = seed
pos  = size - 12
while pos >= 4:
    w = u32_le(body[pos..pos+4])
    w ^= key
    key = (key - w) & 0xFFFFFFFF              # new key for the next (lower) DWORD
    body[pos..pos+4] = u32_le_bytes(w)
    pos -= 4
# After this loop the body up to (size - 8) is the real payload;
# discard the last 8 bytes.
```

### 3.4 RSA-1024 for credential submission

The server sends a scrambled 128-byte RSA public modulus inside the Init packet. The client unscrambles it, encrypts a 128-byte plaintext credential block with `RSA_NO_PADDING`, and sends the 128-byte ciphertext inside RequestAuthLogin.

**Key parameters:**

- Key size: 1024 bits (128 bytes modulus).
- Public exponent: `65537` (`0x10001`).
- Padding: **none** (`RSA_NO_PADDING`). The 128-byte plaintext block must be exactly 128 bytes.

**Plaintext block layout (128 bytes):**

| Offset | Size | Content                                                                       |
| ------ | ---- | ----------------------------------------------------------------------------- |
| `0x00` | 94   | zeros                                                                         |
| `0x5E` | 14   | login, ASCII, null-padded (no null terminator required, the padding is zeros) |
| `0x6C` | 2    | zeros (separator)                                                             |
| `0x6E` | 16   | password, ASCII, null-padded                                                  |
| `0x7E` | 2    | zeros                                                                         |

**Unscrambling the modulus.** The Init packet's 128-byte `scrambledRsaKey` must be unscrambled with this sequence of in-place operations (in exactly this order):

```
# C^-1: XOR bytes 0x40..0x7F with bytes 0x00..0x3F
for i in 0..0x40:
    n[0x40 + i] ^= n[i]

# B^-1: XOR bytes 0x0D..0x10 with bytes 0x34..0x37
for i in 0..4:
    n[0x0D + i] ^= n[0x34 + i]

# A^-1: XOR bytes 0x00..0x3F with bytes 0x40..0x7F
for i in 0..0x40:
    n[i] ^= n[0x40 + i]

# D^-1: swap bytes 0x00..0x03 with 0x4D..0x50
for i in 0..4:
    swap(n[0x00 + i], n[0x4D + i])
```

After that, `n` is the big-endian RSA modulus ready to be used with a standard RSA library.

### 3.5 Login Blowfish keys

**Static key** (used _only_ to decrypt the Init packet):

```
6B 60 CB 5B 82 CE 90 B1 CC 2B 6C 55 6C 6C 6C 6C
```

**Session key** — 16 bytes received inside Init, at offset 153 of the body (after opcode+sessionId+protocolRev+scrambledRsaKey+16 reserved bytes). It is used for all login packets after Init, in both directions.

### 3.6 Login packet encryption pipelines

**Decrypt the Init packet (S→C, opcode `0x00`):**

```
body_enc = raw[2..]                         # strip u16 length
plain    = blowfish_ecb_decrypt(body_enc, STATIC_KEY)   # whole body (multiple of 8)
seed     = u32_le(plain[size - 8 .. size - 4])
rolling_xor_reverse(plain, seed)            # see §3.3
payload  = plain[0 .. size - 8]             # drop last 8 bytes
```

**Decrypt any subsequent S→C login packet:**

```
body_enc = raw[2..]
plain    = blowfish_ecb_decrypt(body_enc, SESSION_KEY)
assert newcrypt_checksum_ok(plain)          # last 4 bytes = XOR of all preceding DWORDs
# `plain` is the real body, starting with the opcode byte.
```

**Encrypt a C→S login packet (used for every outgoing login packet):**

```
body = opcode_byte + fields...              # raw, unencrypted
# 1. pad to multiple of 4 with zeros
# 2. append 8 zero bytes (4 reserved for checksum + 4 spare)
# 3. pad to next multiple of 8 with zeros (adds 0 or 4 zero bytes, since
#    after step 2 the buffer is already a multiple of 4)
# 4. write checksum into the last 4 bytes of the *3-step-padded* buffer
# 5. Blowfish-ECB encrypt with SESSION_KEY
# 6. prepend u16 LE length (encrypted_len + 2)
```

### 3.7 Game XOR stream cipher

After the game-side handshake (§5.3) the client receives 8 bytes of server-chosen XOR key. The full 16-byte key is formed by appending a fixed 8-byte tail:

```
staticTail = C8 27 93 01 A1 6C 31 97
key_cs = serverKey[0..8] + staticTail     # client→server key
key_sc = serverKey[0..8] + staticTail     # server→client key (same bytes, but evolves independently)
```

**Encryption (client → server)** — XOR each byte with the key and the previous _output_ byte:

```
prev = 0
for i in 0..len(body):
    out[i] = body[i] ^ key_cs[i & 15] ^ prev
    prev   = out[i]
```

**Decryption (server → client)** — XOR each byte with the key and the previous _input_ byte:

```
prev = 0
for i in 0..len(body):
    out[i] = body[i] ^ key_sc[i & 15] ^ prev
    prev   = body[i]                         # NOTE: the *encrypted* byte, not the decrypted one
```

**Per-packet key rotation** — after each direction processes a packet of size `N`, the DWORD at bytes 8..11 of the corresponding key is incremented by `N` (little-endian):

```
w  = u32_le(key[8..12])
w  = (w + N) & 0xFFFFFFFF
key[8..12] = u32_le_bytes(w)
```

Both `key_cs` and `key_sc` evolve independently. If the two sides drift out of sync, subsequent packets will be garbage — the stream cipher has no framing recovery.

**First packet rule (HighFive):** on HighFive the very first packet the server sends (CryptInit, §5.3.2) and the very first packet the client sends (ProtocolVersion, §5.3.1) are **plaintext** because the key has not yet been established. Whether packets after CryptInit are encrypted is controlled by CryptInit's `encryptionFlag`: if non-zero, all subsequent packets (starting with the client's AuthRequest) are XOR-encrypted; if zero, the entire session stays plaintext. L2J Mobius CT 2.6 HighFive sends `encryptionFlag = 0` — see §5.3.2.

### 3.8 Test vectors

The following vectors were captured from the reference implementation and can be used to self-verify a port. All input/output is expressed as hex bytes in wire order; no language features or library APIs are implied.

**3.8.1 Blowfish-ECB with the static login key.** Port-level sanity check that the Blowfish key schedule uses little-endian `bytesTo32Bits` (§3.1).

```
key        : 6B 60 CB 5B 82 CE 90 B1 CC 2B 6C 55 6C 6C 6C 6C
plaintext  : 00 11 22 33 44 55 66 77
ciphertext : 46 AA DA CC 2D 39 90 61
```

Round-trip: `Blowfish_decrypt(ciphertext, key) == plaintext`.

**3.8.2 NewCrypt checksum (§3.2).** Input is a 16-byte body whose last 4 bytes are the checksum slot (zero on input). After the algorithm those 4 bytes become the XOR of the three preceding DWORDs.

```
input  : AA BB CC DD  01 02 03 04  10 20 30 40  00 00 00 00
output : AA BB CC DD  01 02 03 04  10 20 30 40  BB 99 FF 99
```

Verification: XOR of `0xDDCCBBAA ^ 0x04030201 ^ 0x40302010` is `0x99FF99BB`, whose little-endian bytes are `BB 99 FF 99` — identical to the last 4 bytes of `output`.

**3.8.3 NewCrypt rolling XOR (§3.3).** The `decXORPass` operation walks a 24-byte buffer backwards. The last 8 bytes carry the seed (4 bytes) and an unused tail (4 bytes) and are never touched by the pass. The first 4 bytes are also untouched because the loop stops at offset 4. Only the middle three DWORDs mutate.

```
seed     : 0x78563412 (read as u32 LE from bytes [size-8..size-4])
input    : DE AD BE EF  11 22 33 44  55 66 77 88  99 AA BB CC  12 34 56 78  00 00 00 00
output   : DE AD BE EF  A4 83 7B 3C  D2 F3 1F 4B  8B 9E ED B4  12 34 56 78  00 00 00 00
```

**3.8.4 RSA modulus unscramble (§3.4).** Deterministic input: `byte[i] = i` for `i ∈ [0, 0x80)`. The full 128-byte unscrambled modulus, in 16-byte rows:

```
input  (128 bytes): 00 01 02 ... 7F

output [0x00..0x0F]: 40 40 40 40  44 45 46 47  48 49 4A 4B  4C 79 7B 79
output [0x10..0x1F]: 67 51 52 53  54 55 56 57  58 59 5A 5B  5C 5D 5E 5F
output [0x20..0x2F]: 60 61 62 63  64 65 66 67  68 69 6A 6B  6C 6D 6E 6F
output [0x30..0x3F]: 70 71 72 73  74 75 76 77  78 79 7A 7B  7C 7D 7E 7F
output [0x40..0x4F]: 40 40 40 40  40 40 40 40  40 40 40 40  40 40 41 42
output [0x50..0x5F]: 43 40 40 40  40 40 40 40  40 40 40 40  40 40 40 40
output [0x60..0x6F]: 40 40 40 40  40 40 40 40  40 40 40 40  40 40 40 40
output [0x70..0x7F]: 40 40 40 40  40 40 40 40  40 40 40 40  40 40 40 40
```

**3.8.5 Game XOR stream cipher (§3.7).** Encrypt a 5-byte plaintext with a 16-byte key whose first 8 bytes are a trivial seed and whose last 8 are the static tail. After encryption, the DWORD at bytes `[8..12]` increases by `N = 5`.

```
key (before)     : 00 01 02 03  04 05 06 07  C8 27 93 01  A1 6C 31 97
plaintext        : 11 22 33 44 55
ciphertext (C→S) : 11 32 03 44 15
key (after N=5)  : 00 01 02 03  04 05 06 07  CD 27 93 01  A1 6C 31 97
```

Round-trip: running the S→C decrypt (§3.7) on `ciphertext` with `key (before)` reproduces `plaintext`.

---

## 4. Login Server protocol

### 4.1 State machine

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
DONE  (disconnect from login server, move to §5)
```

### 4.2 Login Server opcode table

| Opcode | Direction | Name               | Section |
| ------ | --------- | ------------------ | ------- |
| `0x00` | S→C       | Init               | §4.3    |
| `0x01` | S→C       | LoginFail          | §4.4    |
| `0x03` | S→C       | LoginOk            | §4.5    |
| `0x04` | S→C       | ServerList         | §4.6    |
| `0x06` | S→C       | PlayFail           | §4.7    |
| `0x07` | S→C       | PlayOk             | §4.8    |
| `0x0B` | S→C       | GGAuth             | §4.9    |
| `0x00` | C→S       | RequestAuthLogin   | §4.10   |
| `0x02` | C→S       | RequestServerLogin | §4.11   |
| `0x05` | C→S       | RequestServerList  | §4.12   |
| `0x07` | C→S       | RequestGGAuth      | §4.13   |

Note that opcodes are not globally unique: `0x00` and `0x07` exist in both directions with different semantics. Always disambiguate by direction.

### 4.3 Init (S→C, opcode `0x00`)

Decrypted body (after Blowfish + reverse rolling XOR + dropping 8 trailing bytes
that hold the rolling-XOR seed and 4 unused bytes — see §3.3):

| Offset | Field              | Type         | Size | Notes                                                                      |
| ------ | ------------------ | ------------ | ---- | -------------------------------------------------------------------------- |
| 0      | opcode             | `u8`         | 1    | `0x00`                                                                     |
| 1      | `sessionId`        | `i32`        | 4    | echoed in RequestGGAuth                                                    |
| 5      | `protocolRevision` | `i32`        | 4    | expected `0x0000C621`                                                      |
| 9      | `scrambledRsaKey`  | `bytes[128]` | 128  | must be unscrambled (§3.4)                                                 |
| 137    | reserved           | `bytes[16]`  | 16   | four random `i32` (GG seed material), ignored by the client                |
| 153    | `blowfishKey`      | `bytes[16]`  | 16   | session key for every subsequent login packet, both directions             |
| 169    | null terminator    | `u8`         | 1    | `0x00` written by the server                                               |

Total server-written payload: **170 bytes** (`Init.java:62-77`). On the wire
the packet is longer because the login crypto pipeline appends a rolling-XOR
seed (4 bytes), 4 unused bytes, and zero-pads to a Blowfish 8-byte block —
bringing the post-decrypt buffer to **184 bytes**. After `decXORPass` and
dropping the last 8 bytes (§3.3) the client sees **176 bytes**, of which only
the first 170 are meaningful. Bytes 170..175 are zero pad and may be ignored.

### 4.4 LoginFail (S→C, opcode `0x01`)

| Offset | Field    | Type          |
| ------ | -------- | ------------- |
| 0      | opcode   | `u8` = `0x01` |
| 1      | `reason` | `u8`          |

Reason codes recognised by the reference client (all codes are hex):

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

### 4.5 LoginOk (S→C, opcode `0x03`)

| Offset | Field          | Type        | Notes                                                |
| ------ | -------------- | ----------- | ---------------------------------------------------- |
| 0      | opcode         | `u8` = `0x03` |                                                    |
| 1      | `loginOkId1`   | `i32`       | session token #1                                     |
| 5      | `loginOkId2`   | `i32`       | session token #2                                     |
| 9      | reserved       | `bytes[8]`  | two `writeInt(0)` calls                              |
| 17     | `accessLevel`  | `i32`       | `0x000003EA` for a normal account                    |
| 21     | reserved       | `i32`       | `writeInt(0)`                                        |
| 25     | reserved       | `bytes[16]` | `writeBytes(new byte[16])`                           |

Total server-written payload: **41 bytes** (`LoginOk.java:54-64`). The wire
body is longer because of login-packet padding (§3.6) — expect ~56 bytes on
the wire after Blowfish padding, NewCrypt checksum etc. A reimplementer
only needs to keep `loginOkId1` and `loginOkId2`; everything from offset 9
onward is opaque and may be skipped.

### 4.6 ServerList (S→C, opcode `0x04`)

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
per-server character count summary and various L2J Mobius account flags.
A reimplementer doing auto-login can ignore everything after the matched
server record — the client selects the record whose `serverId` matches
the configured `ServerId` and uses its `ip:port` for the Game Server
connection.

### 4.7 PlayFail (S→C, opcode `0x06`)

| Offset | Field    | Type          |
| ------ | -------- | ------------- |
| 0      | opcode   | `u8` = `0x06` |
| 1      | `reason` | `u8`          |

Reason codes recognised by the reference client:

| Code   | Meaning                 |
| ------ | ----------------------- |
| `0x03` | Password mismatch       |
| `0x04` | Access error, try later |
| `0x0F` | Too many players        |

Codes outside this set are logged as `Unknown reason (0x…)`. The legacy Interlude-era table (`0x01` = server full, `0x02` = server down, etc.) is **not** what L2J Mobius sends — a reimplementer must not hard-code it.

### 4.8 PlayOk (S→C, opcode `0x07`)

| Offset | Field          | Type        | Notes                                              |
| ------ | -------------- | ----------- | -------------------------------------------------- |
| 0      | opcode         | `u8` = `0x07` |                                                  |
| 1      | `playOkId1`    | `i32`       | session token #3                                   |
| 5      | `playOkId2`    | `i32`       | session token #4                                   |

Total server-written payload: **9 bytes** (`PlayOk.java:41-44`). The wire
body is longer because of login-packet padding (§3.6); the extra bytes are
crypto padding, not packet fields. Both tokens must be remembered — they
are sent later in the game AuthRequest.

### 4.9 GGAuth (S→C, opcode `0x0B`)

| Offset | Field            | Type        | Notes                                                |
| ------ | ---------------- | ----------- | ---------------------------------------------------- |
| 0      | opcode           | `u8` = `0x0B` |                                                    |
| 1      | `ggAuthResponse` | `i32`       | echoes the `sessionId` from Init                     |
| 5      | reserved         | `bytes[16]` | four `writeInt(0)` calls                             |

Total server-written payload: **21 bytes** (`GGAuth.java:41-47`). The wire
body is longer because of login-packet padding (§3.6); there is **no**
GameGuard nonce — the extra bytes on the wire are crypto padding.
`ggAuthResponse == sessionId` on every L2J Mobius CT 2.6 capture — the
reference Java server simply rewrites the first i32 of GGAuth to the
sessionId. A reimplementer can therefore treat `ggAuthResponse` as a
"keep-alive ack" and only needs the i32 itself.

### 4.10 RequestAuthLogin (C→S, opcode `0x00`)

Body size: **184 bytes** (before padding/encryption). After the §3.6
encryption pipeline this becomes a 192-byte ciphertext + 2-byte length
prefix = 194 bytes on the wire.

| Offset | Field             | Type         | Size | Notes                                              |
| ------ | ----------------- | ------------ | ---- | -------------------------------------------------- |
| 0      | opcode            | `u8`         | 1    | `0x00`                                             |
| 1      | RSA ciphertext    | `bytes[128]` | 128  | computed per §3.4                                  |
| 129    | `sessionId`       | `i32`        | 4    | echoed from Init                                   |
| 133    | reserved          | `bytes[16]`  | 16   | observed all-zero                                  |
| 149    | constant `0x08`   | `i32`        | 4    | observed `0x00000008` on every capture             |
| 153    | reserved          | `bytes[3]`   | 3    | observed all-zero (note unaligned)                 |
| 156    | GG random nonce   | `bytes[16]` | 16   | per-session 16-byte blob from the GameGuard layer  |
| 172    | reserved          | `bytes[4]`   | 4    | observed all-zero                                  |
| 176    | GG auth digest    | `i32`        | 4    | per-session i32 derived from the GameGuard challenge |
| 180    | reserved          | `bytes[4]`   | 4    | observed all-zero                                  |

The 128-byte RSA ciphertext is computed per §3.4 from the login, password,
and the unscrambled modulus from Init. The trailing 55 bytes after the
ciphertext are GameGuard-related — L2J Mobius CT 2.6 does not validate
them and accepts an all-zero blob, so a reimplementer that does not need
to defeat real GameGuard may transmit zeros for everything from offset 129
onward (the `l2py` reference client takes this shortcut).

**Alternative "new auth" mode (optional on the server).**
`RequestAuthLogin.java` supports a `newAuthMethod` branch that expects
**two** 128-byte RSA ciphertexts concatenated (256 bytes total) with this
plaintext layout across the decrypted 256-byte buffer:

| Offset    | Size | Content                         |
| --------- | ---- | ------------------------------- |
| `0x4E`    | 50   | login part 1, ASCII null-padded |
| `0xCE`    | 14   | login part 2, ASCII null-padded |
| `0xDC`    | 16   | password, ASCII null-padded     |

The effective login is `trim(part1) + trim(part2)`. This mode is enabled
via server configuration (L2J Mobius admin flag); the official CT 2.6
HighFive distribution leaves it **disabled**, so the single-block form
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

### 4.11 RequestServerLogin (C→S, opcode `0x02`)

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

The trailing 14 bytes (offsets 10..23) are GameGuard padding. L2J Mobius
accepts a 10-byte body (just opcode+ids+serverId) as well — this is what
the `l2py` reference client transmits.

### 4.12 RequestServerList (C→S, opcode `0x05`)

Body size: **24 bytes** (before padding/encryption). Wire = 34 bytes.

| Offset | Field          | Type         | Notes                                              |
| ------ | -------------- | ------------ | -------------------------------------------------- |
| 0      | opcode         | `u8` = `0x05` |                                                  |
| 1      | `loginOkId1`   | `i32`        | from LoginOk                                       |
| 5      | `loginOkId2`   | `i32`        | from LoginOk                                       |
| 9      | trailing block | `bytes[15]`  | observed `0x05`, 6 zeros, GG tag i32, 4 zeros     |

L2J Mobius only reads the two i32 session tokens (`RequestServerList.java`
calls `remaining() >= 8` and reads two ints), so everything from offset 9
onward is ignored by the server. The server accepts a **9-byte body**
(`opcode + loginOkId1 + loginOkId2`) — this is what the `l2py` reference
client transmits. The `0x05` byte at offset 9 observed on wire from the
official client is not a required flag/version marker.

### 4.13 RequestGGAuth (C→S, opcode `0x07`)

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
right one byte and the high byte XOR'd with `0x07`). L2J Mobius CT 2.6
does not validate this tag and accepts an all-zero blob, so a
reimplementer that does not need to defeat real GameGuard may transmit a
21-byte body with just `opcode + sessionId + 16 zero bytes` (this is what
the `l2py` reference client does).

The four magic constants `0x123 / 0x4567 / 0x89AB / 0xCDEF` documented for
older chronicles do **not** appear in HighFive captures.

### 4.14 Annotated hex dumps

The dumps below are synthetic but internally consistent: every offset add-up can be verified by hand. They all show the **decrypted** body (so the `u16 LE` length prefix is omitted — prepend `len = body + 2` when framing). Use them to cross-check your serializer's offsets against the authoritative specification.

**4.14.1 Init (S→C, `0x00`) — 184 bytes** (§4.3). The 128-byte scrambled RSA key and the 16-byte session Blowfish key are abbreviated as dotted runs for readability; both are opaque to the framer.

```
00                                               ; opcode = 0x00
44 33 22 11                                      ; sessionId        = 0x11223344
21 C6 00 00                                      ; protocolRevision = 0x0000C621
<128 bytes scrambledRsaKey>                      ; offsets 0x09..0x88
<16 bytes reserved, ignored>                     ; offsets 0x89..0x98
<16 bytes blowfishKey (session)>                 ; offsets 0x99..0xA8
00 00 00 00 00 5B A8 44 F7 00 00 00 00 00 00     ; trailing block, offsets 0xA9..0xB7
```

**4.14.2 LoginOk (S→C, `0x03`) — 56 bytes** (§4.5).

```
03                                               ; opcode = 0x03
DD CC BB AA                                      ; loginOkId1 = 0xAABBCCDD
44 33 22 11                                      ; loginOkId2 = 0x11223344
00 00 00 00 00 00 00 00                          ; reserved (offsets 0x09..0x10)
EA 03 00 00                                      ; accessLevel = 0x000003EA
<31 trailing bytes — opaque>                     ; offsets 0x15..0x37
```

**4.14.3 ServerList (S→C, `0x04`) with one record — 40 bytes** (§4.6). The 16-byte trailing block is reproduced verbatim from an observed 1-server response.

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

**4.14.4 GGAuth (S→C, `0x0B`) — 32 bytes** (§4.9).

```
0B                                               ; opcode = 0x0B
C0 00 A0 1A                                      ; ggAuthResponse echoes sessionId = 0x1AA000C0
00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00  ; 16 reserved zero bytes
55 69 30 14 6F 79 17 AC F1 76 ad                 ; 11-byte GG nonce
```

**4.14.5 LoginFail (S→C, `0x01`) — 2 bytes** (§4.4).

```
01                                               ; opcode = 0x01
03                                               ; reason = 0x03 "Wrong login or password"
```

**4.14.6 PlayOk (S→C, `0x07`) — 16 bytes** (§4.8).

```
07                                               ; opcode = 0x07
78 56 34 12                                      ; playOkId1 = 0x12345678
F0 DE BC 9A                                      ; playOkId2 = 0x9ABCDEF0
<7 trailing bytes — opaque GG/queue data>        ; offsets 0x09..0x0F
```

**4.14.7 PlayFail (S→C, `0x06`) — 2 bytes** (§4.7). L2J Mobius writes the reason as a single byte via `writeByte(reason.getCode())`.

```
06                                               ; opcode = 0x06
0F                                               ; reason = 0x0F "Too many players"
```

**4.14.8 RequestAuthLogin (C→S, `0x00`) — 184 bytes, pre-encryption** (§4.10). The RSA ciphertext is 128 opaque bytes; the trailing 55 bytes shown below are reproduced verbatim from an observed capture.

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

**4.14.9 RequestGGAuth (C→S, `0x07`) — 32 bytes, pre-encryption** (§4.13).

```
07                                               ; opcode = 0x07
C0 00 A0 1A                                      ; sessionId echo = 0x1AA000C0
00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00  ; 16 zero bytes (offsets 0x05..0x14)
00 00 00                                         ; 3 more zero bytes (offsets 0x15..0x17)
1D C0 00 A0                                      ; GG client tag (offset 0x18)
00 00 00 00                                      ; reserved (offsets 0x1C..0x1F)
```

**4.14.10 RequestServerList (C→S, `0x05`) — 24 bytes, pre-encryption** (§4.12).

```
05                                               ; opcode = 0x05
0B 2C 55 DF                                      ; loginOkId1 = 0xDF552C0B
02 6C 0B D2                                      ; loginOkId2 = 0xD20B6C02
05                                               ; constant 0x05 (offset 0x09)
00 00 00 00 00 00                                ; reserved (offsets 0x0A..0x0F)
08 0C 40 5E                                      ; GG checksum (offset 0x10)
00 00 00 00                                      ; reserved (offsets 0x14..0x17)
```

**4.14.11 RequestServerLogin (C→S, `0x02`) — 24 bytes, pre-encryption** (§4.11).

```
02                                               ; opcode = 0x02
0B 2C 55 DF                                      ; loginOkId1 = 0xDF552C0B
02 6C 0B D2                                      ; loginOkId2 = 0xD20B6C02
02                                               ; serverId = 2
00 00 00 00 00 00                                ; reserved (offsets 0x0A..0x0F)
0F 0B 40 5E                                      ; GG checksum (offset 0x10)
00 00 00 00                                      ; reserved (offsets 0x14..0x17)
```

All C→S login bodies above are then padded and encrypted per §3.6 before
being framed with a `u16 LE` length. The exact 4-byte GG blobs differ per
session — they are shown here only to anchor the field offsets.

---

## 5. Game Server protocol

### 5.1 State machine

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

### 5.2 Framing and encryption

- Packet framing is identical to the login server (§2.3): `u16 LE length` prefix that includes itself, followed by the body.
- The body is encrypted with the 16-byte XOR stream cipher (§3.7) **except for the very first packet in each direction**: client's ProtocolVersion and server's CryptInit are plaintext.
- There is **no** per-packet checksum on the game stream (in contrast to the login stream). Integrity is implicit: a wrong byte desynchronizes the stream cipher and corrupts all following packets.

### 5.3 Handshake packets

Every multi-byte field below is little-endian. Opcodes are the first byte of the _decrypted_ body.

#### 5.3.1 ProtocolVersion (C→S, opcode `0x0E`) — plaintext

| Offset | Field          | Type         | Value  |
| ------ | -------------- | ------------ | ------ |
| 0      | opcode         | `u8`         | `0x0E` |
| 1      | `protocol`     | `i32`        | `273`  |
| 5      | trailing block | `bytes[260]` | client build-info / hardware fingerprint, opaque |

L2J Mobius CT 2.6 only consumes the first 5 bytes. The official client
nonetheless sends a 265-byte body (267 bytes on the wire). A reimplementer may transmit only the 5-byte minimum form
— the `l2py` reference client does this and the server accepts it.

#### 5.3.2 CryptInit (S→C, opcode `0x2E`) — plaintext

23-byte packet (body, without the 2-byte length prefix):

| Offset | Field            | Type       | Notes                                                   |
| ------ | ---------------- | ---------- | ------------------------------------------------------- |
| 0      | opcode           | `u8`       | `0x2E`                                                  |
| 1      | `result`         | `u8`       | must be `1` for success; any other value is a rejection |
| 2      | `xorKey`         | `bytes[8]` | first 8 bytes of the stream cipher key                  |
| 10     | `encryptionFlag` | `u32`      | non-zero → encryption enabled for subsequent packets    |
| 14     | reserved         | `bytes[9]` | ignored                                                 |

After receiving CryptInit, the client builds `key_cs` and `key_sc` as `xorKey || staticTail` (§3.7) and enables encryption according to `encryptionFlag`.

**L2J Mobius CT 2.6 HighFive quirk:** the reference server sends `encryptionFlag = 0`, which disables the XOR stream cipher for the entire session — every subsequent packet (including AuthRequest) travels as plaintext. A correct client must honor this flag and only apply the XOR cipher when it is non-zero.

The reference client passes `encryptionFlag` directly into its crypt layer (`this.crypt.initKey(xorKeyData, useEncryption)`), and the crypt layer's `encrypt`/`decrypt` methods short-circuit to the identity function when `enabled = false`. In other words, a reimplementer is not required to special-case "encryption disabled" in the packet dispatcher — a no-op crypt object is the cleanest factoring.

#### 5.3.3 AuthRequest (C→S, opcode `0x2B`) — first packet after CryptInit (encrypted iff `CryptInit.encryptionFlag ≠ 0`)

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
it wrong silently breaks auth on L2J Mobius. The 16-byte trailing block
is sent by the official client (observed as a 49-byte body for
`username = "qwerty"`); L2J Mobius does not read past
`loginOkId2`, so a reimplementer may omit the trailer entirely (the
`l2py` reference client does).

#### 5.3.4 CharSelectionInfo (S→C, opcode `0x09`)

| Offset | Field             | Type          |
| ------ | ----------------- | ------------- |
| 0      | opcode            | `u8` = `0x09` |
| 1      | `charCount`       | `u32`         |
| 5      | character records | variable      |

The auto-login algorithm does not need to parse character records; it simply picks `CONFIG.CharSlotIndex` (default `0`) and sends CharacterSelected. A reimplementer that wants to display the character list must parse each record: per-character data includes the character name (UTF-16LE string), character id (`i32`), access level (`i32`), class id (`i32`), last used flag, and a variable-length block with appearance, stats, and equipment. The layout is stable across L2J Mobius builds but is irrelevant for auto-entering the world, so its full decoding is out of scope here.

#### 5.3.5 CharacterSelected (C→S, opcode `0x12`)

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
(`readShort + 3×readInt`, see `CharacterSelect.java:77-81`) and will cause a
`BufferUnderflowException` if absent. Total body size is **19 bytes**. All
four fields are carried over from the C4 client and are simply discarded by
L2J Mobius, so a client may transmit zeros.

#### 5.3.6 CharSelected (S→C, opcode `0x0B`)

Confirmation that the selected character was loaded. The body beyond the opcode is not required by the client; the presence of the opcode in state `WAIT_CHAR_SELECTED` triggers sending RequestKeyMapping and EnterWorld.

**Important quirk:** some server builds skip CharSelected and send UserInfo (`0x32`) directly. The client must therefore also accept UserInfo while still in `WAIT_CHAR_SELECTED` and promote the state machine straight to IN_GAME.

#### 5.3.7 RequestKeyMapping (C→S, extended opcode `0xD0 0x21`)

| Offset | Field       | Type  | Value    |
| ------ | ----------- | ----- | -------- |
| 0      | main opcode | `u8`  | `0xD0`   |
| 1      | sub-opcode  | `u16` | `0x0021` |

This is the canonical "extended packet" form used by L2 from Interlude onwards: a 1-byte primary opcode (`0xD0`) followed by a 2-byte LE sub-opcode.

#### 5.3.8 EnterWorld (C→S, opcode `0x11`)

Total body size: **105 bytes** (1 opcode + 104 zero pad).

| Offset | Field   | Type         | Value     |
| ------ | ------- | ------------ | --------- |
| 0      | opcode  | `u8`         | `0x11`    |
| 1      | padding | `bytes[104]` | all zeros |

**The 104 zero bytes are mandatory on L2J Mobius** — the server parses them as hardware info / traceroute blob and will throw `BufferUnderflowException` otherwise.

#### 5.3.9 UserInfo (S→C, opcode `0x32`)

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

### 5.4 Keepalive

The server periodically sends NetPingRequest; the client must answer promptly with NetPing or the server will close the connection.

#### 5.4.1 NetPingRequest (S→C, opcode `0xD9`)

| Offset | Field    | Type          |
| ------ | -------- | ------------- |
| 0      | opcode   | `u8` = `0xD9` |
| 1      | `pingId` | `i32`         |

Earlier protocol drafts (and most public L2 documentation) list this packet
at `0xD3`, but in L2J Mobius CT 2.6 HighFive `0xD3 = EARTHQUAKE` and the
ping request moved to `0xD9` (`ServerPackets.java:247`).

#### 5.4.2 NetPing (C→S, opcode `0xB1`)

**Observed on the wire: 5-byte body.** The reference client's live ping handler writes just the opcode and the echoed `pingId`:

| Offset | Field    | Type  | Value                    |
| ------ | -------- | ----- | ------------------------ |
| 0      | opcode   | `u8`  | `0xB1`                   |
| 1      | `pingId` | `i32` | echo from NetPingRequest |

On CT 2.6 HighFive the server opcode handler is `ClientPackets.NET_PING`
at `0xB1` (`ClientPackets.java:175`). Some earlier chronicle documentation
lists the C→S ping at `0xA8`; on CT 2.6 `0xA8 = REQUEST_PACKAGE_SEND`, so
sending a ping at `0xA8` will reach the wrong handler.

### 5.5 Representative gameplay packets

These packets are not required to enter the world, but are included so that a reimplementer knows the pattern used for common commands. All are subject to the XOR cipher when §5.3.2's `encryptionFlag` is non-zero.

All opcodes below are taken from `ClientPackets.java` in
`c:\MyProg\l2J-Mobius-CT-2.6-HighFive\java\org\l2jmobius\gameserver\network\`.
Earlier L2 chronicles (Interlude, Gracia, etc.) use different numbers — do
**not** port opcodes from Interlude-era documentation.

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
| `0xB1`        | NetPing                            | `i32 pingId` — see §5.4.2                                                                                            |
| `0xD0 …`      | extended packets                   | all extended C→S packets (see `ExClientPackets.java`), including RequestKeyMapping (`0x0021`)                        |

**Opcode `0x14` is NOT overloaded on CT 2.6 HighFive.** It is only
`RequestItemList` with no body. `UseItem` has its own opcode (`0x19`). The
"overload by body length" behaviour is an Interlude-era artefact and does
not apply here.

**Extended packet `0xD0 0x0001` = `RequestManorList`.** The often-cited
subopcode `0x0008` for "EnterGameServer / RequestManorList" is an
Interlude-era carryover and is absent from CT 2.6 HighFive. A reimplementer
does not need to send an `EnterGameServer` packet at all — the CT 2.6
server drives the transition from character selection to world through
`EnterWorld (0x11)`.

**RequestSocialAction** has opcode `0x34` on CT 2.6 HighFive but the server
handler is `null` in `ClientPackets.java`, i.e. not routed. Social actions
are therefore effectively unsupported by the CT 2.6 server build; the id
table below is retained only as protocol-level reference and is action-ids
sent via other means (e.g. `RequestActionUse 0x56`).

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

These suffice to implement movement, combat, inventory use, chat, skill casting, and basic social actions. Additional opcodes can be added incrementally — the L2J Mobius source is the authoritative reference for any packet not listed here.

### 5.6 Server-to-client packets beyond the handshake

Once the client reaches `IN_GAME`, the server begins streaming a large set of opcodes (inventory updates, spawn/despawn, chat, system messages, skill results, etc.) that this specification does not enumerate. A complete reimplementation is not required to decode them, but it **is** required to stay in sync with the encryption stream — which means every incoming packet must be:

1. **Framed** using the `u16 LE` length prefix (§2.3).
2. **Decrypted** with `key_sc` (§3.7), and `key_sc[8..12]` must be rotated by the packet's body size **regardless of whether the opcode is recognised**. Skipping the rotation for unknown packets will silently desynchronise subsequent packets.
3. **Dispatched** by opcode. Unknown opcodes should be logged at `WARN` level but **must not** trigger a disconnect — the L2J Mobius server regularly sends build-specific opcodes a HighFive-only client has never seen.

The two opcodes a minimal client **must** handle after `IN_GAME`:

- `0xD9` **NetPingRequest** — reply with NetPing (`0xB1`, §5.4) or the server will drop the connection after ~60 seconds.
- `0x32` **UserInfo** — sent periodically with updated player state; parse at least the leading fields described in §5.3.9 to keep the simulated world up to date.

Everything else can be treated as opaque until the client chooses to decode a specific feature. The reference dispatcher in the reference implementation is the canonical template for a HighFive dispatcher.

---

## 6. Automatic enter-game algorithm

This section describes the exact sequence of steps the reference client performs to go from "cold start" to "character walking in the world", using only the configuration inputs `username`, `password`, `loginHost`, `loginPort`, `serverId`, `charSlot`, and `protocol = 273`.

### 6.1 Sequence diagram

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

### 6.2 Detailed pseudocode

```
# ---- Phase 1: Login Server ----
loginSock = tcp_connect(loginHost, loginPort)

pkt = read_framed(loginSock)                      # §2.3
init = blowfish_ecb_decrypt(pkt.body, STATIC_LOGIN_BLOWFISH_KEY)
seed = u32_le(init[len(init)-8 : len(init)-4])
rolling_xor_reverse(init, seed)                   # §3.3
init = init[ : len(init) - 8]

assert init[0] == 0x00
sessionId          = i32_le(init[1:5])
protocolRev        = i32_le(init[5:9])            # expect 0xC621
scrambledRsaKey    = init[9:137]
# init[137:153] reserved
sessionBlowfishKey = init[153:169]                # 16 bytes

rsaModulus = unscramble_rsa_key(scrambledRsaKey)  # §3.4
currentLoginKey = sessionBlowfishKey              # switch from static to session key

# --- RequestGGAuth (0x07) ---
# 32-byte body: opcode + sessionId + 19 zeros + GG client tag + 4 zeros.
# L2J Mobius accepts an all-zero GG tag, so a minimal client may send
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
# L2J Mobius accepts an all-zero trailer, so a minimal client may send
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
    rec = parse_server_record(sl[pos : pos+21])   # §4.6
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
# from now on, encrypt/decrypt with §3.7

# AuthRequest (0x2B) — first post-CryptInit packet. Encrypted iff encryptionOn;
# L2J Mobius HighFive sends encryptionFlag = 0, so this stays plaintext.
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
        # L2J Mobius HighFive: opcode 0xB1 + pingId (5-byte body).
        pong   = bytes([0xB1]) + i32_le(pingId)
        send_game_encrypted(gameSock, pong, key_cs)
    else:
        handle_world_packet(body)
```

### 6.3 Required configuration inputs

| Input       | Typical value | Notes                                                               |
| ----------- | ------------- | ------------------------------------------------------------------- |
| `username`  | string        | Login account (the reference client defaults to `qwerty`)           |
| `password`  | string        | Password (defaults to `qwerty`)                                     |
| `loginHost` | IPv4/DNS      | Login Server address                                                |
| `loginPort` | `2106`        |                                                                     |
| `protocol`  | `273`         | Must match a HighFive-compatible value (also `267`, `268`, `271`)   |
| `serverId`  | `1..255`      | The numeric id of the desired Game Server inside the ServerList     |
| `charSlot`  | `0..6`        | Which existing character to log in as (no auto-create is performed) |

The reference implementation reads these from environment variables (`L2_USERNAME`, `L2_PASSWORD`, `L2_LOGIN_IP`, `L2_LOGIN_PORT`, `L2_PROTOCOL`, `L2_SERVER_ID`, `L2_CHAR_SLOT`). A reimplementer can use any equivalent source.

### 6.4 Capture cross-reference

All packet sizes and trailing-block hex strings in §4 were verified
against live L2 official client ↔ L2J Mobius CT 2.6 HighFive captures.
Observed packet sizes:

| Direction | Wire | Body | Section | Notes                                |
| --------- | ---- | ---- | ------- | ------------------------------------ |
| S→C       | 196  | 184  | §4.3    | Init                                 |
| C→S       | 42   | 32   | §4.13   | RequestGGAuth                        |
| S→C       | 42   | 32   | §4.9    | GGAuth (i32 echoes sessionId)        |
| C→S       | 194  | 184  | §4.10   | RequestAuthLogin                     |
| S→C       | 66   | 56   | §4.5    | LoginOk                              |
| C→S       | 34   | 24   | §4.12   | RequestServerList                    |
| S→C       | 50   | 40   | §4.6    | ServerList (1 record + 16-byte tail) |
| C→S       | 34   | 24   | §4.11   | RequestServerLogin                   |
| S→C       | 26   | 16   | §4.8    | PlayOk                               |
| C→S       | 267  | 265  | §5.3.1  | ProtocolVersion + 260-byte client tail (server reads only the first 5 bytes) |
| S→C       | 25   | 23   | §5.3.2  | CryptInit (plaintext, `encryptionFlag = 0`) |
| C→S       | 49   | 47   | §5.3.3  | AuthRequest (`username="qwerty"`, includes 16-byte trailer) |
| C→S       | 21   | 19   | §5.3.5  | CharacterSelected                    |

Body sizes are derived as `wire − 2` for plaintext frames and as
`wire − 2 − pad` for login-encrypted frames, where `pad` is the
4-/8-byte alignment from §3.6.

### 6.5 Error handling expected from a correct client

- **Wrong credentials** → LoginFail (`0x01`) with reason code (full table in §4.4); abort.
- **Server not in list** → no record matches `serverId`; abort before sending RequestServerLogin.
- **Server full / down** → PlayFail (`0x06`); abort.
- **Bad protocol version** → CryptInit's `result` byte is not `1`; abort.
- **Character slot empty or out of range** → the server closes the connection after CharacterSelected; the client should surface this as an error (there is no dedicated "char missing" packet).
- **Missing NetPing answer** → server disconnects after a timeout (~60 s). Always answer pings.

---

## 7. Implementation checklist

Use this list when porting to a new language. Tick every box to have a working auto-login client.

- [ ] TCP connection with `u16 LE` length-prefixed frame reassembly.
- [ ] Blowfish ECB 16-round cipher, little-endian byte-to-DWORD conversion.
- [ ] Static login Blowfish key `6B 60 CB 5B 82 CE 90 B1 CC 2B 6C 55 6C 6C 6C 6C`.
- [ ] Init packet decryption = Blowfish(static) + rolling XOR reverse + drop trailing 8 bytes.
- [ ] Per-packet NewCrypt XOR checksum (compute on send, verify on recv) over 4-byte DWORDs with last 4 bytes holding the result.
- [ ] Login-packet padding: 4-byte align → +8 zeros → 8-byte align → write checksum → Blowfish encrypt.
- [ ] RSA modulus unscrambler (C^-1, B^-1, A^-1, D^-1 in that order).
- [ ] RSA-1024 encryption with `RSA_NO_PADDING`, exponent 65537, 128-byte plaintext layout (94 / 14 login / 2 / 16 password / 2).
- [ ] Login state machine with all 7 packets (§4.3 — §4.13). On HighFive
      L2J Mobius, body sizes are: Init 184, GGAuth 32 (only first i32
      matters), LoginOk 56 (only first 9 bytes matter), ServerList
      3+N·21+trailer, PlayOk 16 (only first 9 bytes matter), RequestGGAuth
      32 (or 21 minimal), RequestAuthLogin 184 (or 137 minimal),
      RequestServerList 24 (or 10 minimal), RequestServerLogin 24 (or 10
      minimal).
- [ ] ServerList parsing with 21-byte records (§4.6); skip the trailing
      block — it is per-server character counts that auto-login does not need.
- [ ] Transition to Game Server using `gameServerIp:gameServerPort` from the matched ServerList record.
- [ ] Game packet framing same as login; XOR cipher only after CryptInit.
- [ ] Static game XOR tail `C8 27 93 01 A1 6C 31 97`.
- [ ] Stream-cipher chaining: `out[i] = src[i] ^ key[i&15] ^ prev`; on send `prev = out[i]`, on recv `prev = encrypted[i]`.
- [ ] Key rotation after every packet: `key[8..12] += packetSize` (LE DWORD).
- [ ] ProtocolVersion (0x0E) with `i32 273`, plaintext.
- [ ] AuthRequest (0x2B): username UTF-16LE + null, then **playOkId2, playOkId1, loginOkId1, loginOkId2** in that order.
- [ ] CharacterSelected (0x12): `i32 slotIndex` + 14 zero bytes.
- [ ] Accept UserInfo (0x32) directly in `WAIT_CHAR_SELECTED` state as an implicit confirmation.
- [ ] RequestKeyMapping extended packet `0xD0 0x21` followed by EnterWorld (0x11) + 104 zero bytes.
- [ ] Reach IN_GAME upon receiving UserInfo (0x32); parse at least the initial fields (x, y, z, objectId, name, level, HP/MP).
- [ ] NetPing (`0xB1`) answer to every NetPingRequest (`0xD9`) with a **5-byte body** = `u8 0xB1 + i32 pingId`. Do not use `0xA8` / `0xD3` — those are different packets on CT 2.6 HighFive.
- [ ] Do **not** treat `0x14` as overloaded on CT 2.6 — it is only `RequestItemList`. `UseItem` is `0x19`.
- [ ] Rotate `key_sc[8..12]` by the body size for **every** decrypted packet — even the ones whose opcode is unrecognised — or the XOR stream desynchronises (§5.6).
- [ ] Never disconnect on an unknown opcode; log and drop the packet instead (§5.6).

---

## 8. Constants appendix

| Name                              | Value                                                          | Used in                  |
| --------------------------------- | -------------------------------------------------------------- | ------------------------ |
| Protocol version (HighFive)       | `273` (also `267`, `268`, `271`)                               | ProtocolVersion (§5.3.1) |
| Expected Init protocol revision   | `0x0000C621`                                                   | Init (§4.3)              |
| Static login Blowfish key         | `6B 60 CB 5B 82 CE 90 B1 CC 2B 6C 55 6C 6C 6C 6C`              | Init decryption (§3.5)   |
| Static game XOR tail              | `C8 27 93 01 A1 6C 31 97`                                      | XOR key (§3.7)           |
| RequestServerList minimal body    | 9 bytes (opcode + 2×i32); the server ignores any trailer       | §4.12                    |
| RequestGGAuth body shape          | 32 bytes; server reads 21 (opcode + sessionId + 16 zeros)      | §4.13                    |
| RequestAuthLogin body shape       | 184 bytes; opcode + 128-byte RSA + 55-byte GG trailer          | §4.10                    |
| RSA plaintext layout              | 94 zero / 14 login / 2 zero / 16 password / 2 zero = 128 bytes | §3.4                     |
| RSA public exponent               | `65537` (`0x10001`)                                            | §3.4                     |
| CharacterSelected trailing fields | `i16 + 3×i32` (= 14 bytes of typed zeros) after `slotIndex`    | §5.3.5                   |
| EnterWorld padding                | 104 zero bytes after opcode                                    | §5.3.8                   |
| NetPingRequest opcode (S→C)       | `0xD9`                                                         | §5.4.1                   |
| NetPing opcode (C→S)              | `0xB1`, 5-byte body (`u8 + i32 pingId`)                        | §5.4.2                   |
| Maximum packet length             | `0xFFFF` (= 65 533-byte body)                                  | §2.3                     |

**LoginFail reason codes** (§4.4):

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

**PlayFail reason codes** (§4.7):

| Code   | Meaning                 |
| ------ | ----------------------- |
| `0x03` | Password mismatch       |
| `0x04` | Access error, try later |
| `0x0F` | Too many players        |

**RequestSocialAction action ids** (§5.5):

| Id  | Action    | Id   | Action  |
| --- | --------- | ---- | ------- |
| `1` | Stand/Sit | `8`  | Unaware |
| `2` | Greeting  | `9`  | Waiting |
| `3` | Victory   | `10` | Laugh   |
| `4` | Advance   | `11` | Think   |
| `5` | No        | `12` | Applaud |
| `6` | Yes       | `13` | Dance   |
| `7` | Bow       |      |         |

**Duplicated C→S opcodes on CT 2.6 HighFive** (§5.5):

| Opcode | Handler class   | Notes                                                       |
| ------ | --------------- | ----------------------------------------------------------- |
| `0x01` | `AttackRequest` | basic attack; same class also registered at `0x32`          |
| `0x32` | `AttackRequest` | alternate attack opcode; identical behaviour to `0x01`      |

There is no body-length or phase-based opcode overloading on CT 2.6 — the
Interlude-era claims about `0x14` (UseItem/RequestItemList) and
`0xD0 0x0008` (EnterGameServer/RequestManorList) do not apply to this
chronicle.

---
