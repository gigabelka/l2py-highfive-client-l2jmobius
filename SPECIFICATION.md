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
# 1. compute how many zero bytes must be added so that (len(body) + 4)
#    becomes a multiple of 8 — i.e. pad = (8 - (len(body) + 4) % 8) % 8
# 2. append `pad` zero bytes, then 4 zero bytes reserved for the checksum
#    (the buffer is now a multiple of 8)
# 3. compute the §3.2 XOR checksum over every DWORD except the last one,
#    and write it into the trailing 4 bytes
# 4. Blowfish-ECB encrypt with SESSION_KEY
# 5. prepend u16 LE length (encrypted_len + 2)
```

The single-step formula above is equivalent to the older "pad-to-4 / append-8 / pad-to-8" description and is the shape the reference client actually uses.

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

Decrypted body (after Blowfish + reverse rolling XOR + dropping 8 trailing bytes):

| Offset | Field              | Type         | Size | Notes                                    |
| ------ | ------------------ | ------------ | ---- | ---------------------------------------- |
| 0      | opcode             | `u8`         | 1    | `0x00`                                   |
| 1      | `sessionId`        | `i32`        | 4    | used by RequestGGAuth                    |
| 5      | `protocolRevision` | `i32`        | 4    | expected `0x0000C621`                    |
| 9      | `scrambledRsaKey`  | `bytes[128]` | 128  | must be unscrambled (§3.4)               |
| 137    | reserved           | `bytes[16]`  | 16   | four `i32`, ignored                      |
| 153    | `blowfishKey`      | `bytes[16]`  | 16   | session key for subsequent login packets |
| 169    | null terminator    | `u8`         | 1    | `0x00`                                   |

Total payload: **170 bytes**.

### 4.4 LoginFail (S→C, opcode `0x01`)

| Offset | Field    | Type          |
| ------ | -------- | ------------- |
| 0      | opcode   | `u8` = `0x01` |
| 1      | `reason` | `u8`          |

Reason codes recognised by the reference client (all codes are hex):

| Code   | Meaning                              |
| ------ | ------------------------------------ |
| `0x01` | Account does not exist               |
| `0x02` | Password is incorrect                |
| `0x03` | Password does not match this account |
| `0x04` | Account is banned                    |
| `0x05` | Account is already in use            |
| `0x06` | Server is under maintenance          |
| `0x07` | Account is already in use            |
| `0x08` | Server is full                       |
| `0x09` | Server is under maintenance          |
| `0x0A` | Login is currently prohibited        |
| `0x0B` | Server is full (queue)               |

Codes outside this set are logged as `Unknown reason (0x…)` and treated as fatal. Code `0x07` is specifically transient: the reference client waits a few seconds and retries. On any other LoginFail the client must close the connection.

### 4.5 LoginOk (S→C, opcode `0x03`)

| Offset | Field        | Type          |
| ------ | ------------ | ------------- |
| 0      | opcode       | `u8` = `0x03` |
| 1      | `loginOkId1` | `i32`         |
| 5      | `loginOkId2` | `i32`         |

Both tokens must be remembered — they are sent in RequestServerList, RequestServerLogin, and later in the game AuthRequest.

### 4.6 ServerList (S→C, opcode `0x04`)

| Offset   | Field             | Type                      |
| -------- | ----------------- | ------------------------- |
| 0        | opcode            | `u8` = `0x04`             |
| 1        | `serverCount`     | `u8`                      |
| 2        | `lastServer`      | `u8`                      |
| 3 + k·23 | server record `k` | see below (23 bytes each) |

**Server record (23 bytes):**

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
| 16     | trailing        | `bytes[7]` | opaque — size may differ across Mobius builds          |

The trailing 7 bytes carry `flags i32`, brackets flag, and other informational fields in some builds; a client only needs the first 16 bytes to connect. The reader should tolerate a varying trailing-block length.

The client selects the record whose `serverId` matches the configured `ServerId` and uses its `ip:port` for the Game Server connection.

### 4.7 PlayFail (S→C, opcode `0x06`)

| Offset | Field    | Type          |
| ------ | -------- | ------------- |
| 0      | opcode   | `u8` = `0x06` |
| 1      | `reason` | `i32`         |

Reason codes recognised by the reference client:

| Code   | Meaning                 |
| ------ | ----------------------- |
| `0x03` | Password mismatch       |
| `0x04` | Access error, try later |
| `0x0F` | Too many players        |

Codes outside this set are logged as `Unknown reason (0x…)`. The legacy Interlude-era table (`0x01` = server full, `0x02` = server down, etc.) is **not** what L2J Mobius sends — a reimplementer must not hard-code it.

### 4.8 PlayOk (S→C, opcode `0x07`)

| Offset | Field       | Type          |
| ------ | ----------- | ------------- |
| 0      | opcode      | `u8` = `0x07` |
| 1      | `playOkId1` | `i32`         |
| 5      | `playOkId2` | `i32`         |

Both tokens must be remembered — they are sent later in the game AuthRequest.

### 4.9 GGAuth (S→C, opcode `0x0B`)

| Offset | Field            | Type          |
| ------ | ---------------- | ------------- |
| 0      | opcode           | `u8` = `0x0B` |
| 1      | `ggAuthResponse` | `i32`         |

The client must remember `ggAuthResponse` and echo it inside RequestAuthLogin.

### 4.10 RequestAuthLogin (C→S, opcode `0x00`)

Body size: **145 bytes** (before padding/encryption).

| Offset | Field          | Type         | Size | Notes                                 |
| ------ | -------------- | ------------ | ---- | ------------------------------------- |
| 0      | opcode         | `u8`         | 1    | `0x00`                                |
| 1      | RSA ciphertext | `bytes[128]` | 128  | encrypted credentials (§3.4)          |
| 129    | `loginOkId1`   | `i32`        | 4    | `0` on first login (no LoginOk yet)   |
| 133    | `loginOkId2`   | `i32`        | 4    | `0` on first login                    |
| 137    | padding        | `bytes[8]`   | 8    | zeros                                 |

The 128-byte RSA ciphertext is computed per §3.4 from the login, password, and the unscrambled modulus from Init.

L2J Mobius does not validate the two `loginOkId` fields or the 8 trailing bytes on this packet — they were meaningful in earlier chronicles (and earlier documentation of this protocol referenced a 43-byte fixed GG block plus `ggAuthResponse`), but in CT 2.6 HighFive only the RSA ciphertext matters. Sending them as zeros is what the reference client does.

### 4.11 RequestServerLogin (C→S, opcode `0x02`)

| Offset | Field        | Type          |
| ------ | ------------ | ------------- |
| 0      | opcode       | `u8` = `0x02` |
| 1      | `loginOkId1` | `i32`         |
| 5      | `loginOkId2` | `i32`         |
| 9      | `serverId`   | `u8`          |

### 4.12 RequestServerList (C→S, opcode `0x05`)

Total body size: **10 bytes**.

| Offset | Field        | Type  | Value                |
| ------ | ------------ | ----- | -------------------- |
| 0      | opcode       | `u8`  | `0x05`               |
| 1      | `loginOkId1` | `i32` | from LoginOk         |
| 5      | `loginOkId2` | `i32` | from LoginOk         |
| 9      | `flags`      | `u8`  | constant `0x05`      |

### 4.13 RequestGGAuth (C→S, opcode `0x07`)

Body size: **21 bytes** (before padding/encryption).

| Offset | Field       | Type        | Value     |
| ------ | ----------- | ----------- | --------- |
| 0      | opcode      | `u8`        | `0x07`    |
| 1      | `sessionId` | `i32`       | from Init |
| 5      | padding     | `bytes[16]` | zeros     |

L2J Mobius does not verify the trailing 16 bytes — any content is accepted. Historical L2 documentation lists four `i32` GG constants (`0x00000123`, `0x00004567`, `0x000089AB`, `0x0000CDEF`) followed by 19 zero bytes; they are _not_ required by this server.

### 4.14 Annotated hex dumps

The dumps below are synthetic but internally consistent: every offset add-up can be verified by hand. They all show the **decrypted** body (so the `u16 LE` length prefix is omitted — prepend `len = body + 2` when framing). Use them to cross-check your serializer's offsets against the authoritative specification.

**4.14.1 Init (S→C, `0x00`) — 170 bytes** (§4.3). The 128-byte scrambled RSA key and the 16-byte session Blowfish key are abbreviated as dotted runs for readability; both are opaque to the framer.

```
00                                               ; opcode = 0x00
44 33 22 11                                      ; sessionId        = 0x11223344
21 C6 00 00                                      ; protocolRevision = 0x0000C621
<128 bytes scrambledRsaKey>                      ; offsets 0x09..0x88
<16 bytes reserved, ignored>                     ; offsets 0x89..0x98
<16 bytes blowfishKey (session)>                 ; offsets 0x99..0xA8
00                                               ; terminator (offset 0xA9)
```

**4.14.2 LoginOk (S→C, `0x03`) — 9 bytes** (§4.5).

```
03                                               ; opcode = 0x03
DD CC BB AA                                      ; loginOkId1 = 0xAABBCCDD
44 33 22 11                                      ; loginOkId2 = 0x11223344
```

**4.14.3 ServerList (S→C, `0x04`) with one record — 26 bytes** (§4.6).

```
04                                               ; opcode = 0x04
01                                               ; serverCount = 1
00                                               ; lastServer

; --- server record 0 (23 bytes) ---
01                                               ; serverId = 1
7F 00 00 01                                      ; ip = 127.0.0.1 (bytes in display order)
61 1E 00 00                                      ; port = 7777 (i32 LE)
00                                               ; ageLimit
00                                               ; isPvp = false
32 00                                            ; onlinePlayers = 50 (u16 LE)
88 13                                            ; maxPlayers    = 5000 (u16 LE)
01                                               ; isOnline = true
00 00 00 00 00 00 00                             ; trailing opaque bytes (7)
```

**4.14.4 GGAuth (S→C, `0x0B`) — 5 bytes** (§4.9).

```
0B                                               ; opcode = 0x0B
EF BE AD DE                                      ; ggAuthResponse = 0xDEADBEEF
```

**4.14.5 LoginFail (S→C, `0x01`) — 2 bytes** (§4.4).

```
01                                               ; opcode = 0x01
03                                               ; reason = 0x03 "Password does not match this account"
```

**4.14.6 PlayOk (S→C, `0x07`) — 9 bytes** (§4.8).

```
07                                               ; opcode = 0x07
78 56 34 12                                      ; playOkId1 = 0x12345678
F0 DE BC 9A                                      ; playOkId2 = 0x9ABCDEF0
```

**4.14.7 PlayFail (S→C, `0x06`) — 5 bytes** (§4.7). Note the `i32` reason, not `u8`.

```
06                                               ; opcode = 0x06
0F 00 00 00                                      ; reason = 0x0F "Too many players"
```

**4.14.8 RequestAuthLogin (C→S, `0x00`) — 145 bytes, pre-encryption** (§4.10). The RSA ciphertext is 128 opaque bytes; the trailing 16 bytes are `loginOkId1/2` (zero on first login) plus 8 zero bytes of padding.

```
00                                               ; opcode = 0x00
<128 bytes RSA ciphertext>                       ; offsets 0x01..0x80
00 00 00 00                                      ; loginOkId1 = 0 (no LoginOk yet)
00 00 00 00                                      ; loginOkId2 = 0
00 00 00 00 00 00 00 00                          ; 8 zero bytes of padding
```

**4.14.9 RequestGGAuth (C→S, `0x07`) — 21 bytes, pre-encryption** (§4.13).

```
07                                               ; opcode = 0x07
44 33 22 11                                      ; sessionId echo = 0x11223344
00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00  ; 16 zero bytes of padding
```

**4.14.10 RequestServerList (C→S, `0x05`) — 10 bytes, pre-encryption** (§4.12).

```
05                                               ; opcode = 0x05
DD CC BB AA                                      ; loginOkId1 = 0xAABBCCDD
44 33 22 11                                      ; loginOkId2 = 0x11223344
05                                               ; flags = 0x05 (u8)
```

**4.14.11 RequestServerLogin (C→S, `0x02`) — 10 bytes, pre-encryption** (§4.11).

```
02                                               ; opcode = 0x02
DD CC BB AA                                      ; loginOkId1
44 33 22 11                                      ; loginOkId2
01                                               ; serverId = 1
```

All C→S login bodies above are then padded and encrypted per §3.6 before being framed with a `u16 LE` length.

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
  | answer NetPingRequest (0xD3) with NetPing (0xA8)
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

| Offset | Field      | Type  | Value  |
| ------ | ---------- | ----- | ------ |
| 0      | opcode     | `u8`  | `0x0E` |
| 1      | `protocol` | `i32` | `273`  |

#### 5.3.2 CryptInit (S→C, opcode `0x2E`) — plaintext

23-byte packet (body, without the 2-byte length prefix):

| Offset | Field             | Type       | Notes                                                   |
| ------ | ----------------- | ---------- | ------------------------------------------------------- |
| 0      | opcode            | `u8`       | `0x2E`                                                  |
| 1      | `result`          | `u8`       | must be `1` for success; any other value is a rejection |
| 2      | `xorKey`          | `bytes[8]` | first 8 bytes of the stream cipher key                  |
| 10     | `encryptionFlag`  | `u32`      | non-zero → encryption enabled for subsequent packets    |
| 14     | `serverId`        | `i32`      | optional — present in L2J Mobius CT 2.6                 |
| 18     | `obfuscationFlag` | `u8`       | optional                                                |
| 19     | `obfuscationKey`  | `i32`      | optional                                                |

The 9 bytes starting at offset 14 are what older documentation calls "reserved"; L2J Mobius CT 2.6 populates them as shown above. A client must tolerate packets shorter than 23 bytes (parsing extra fields only when bytes remain).

After receiving CryptInit, the client builds `key_cs` and `key_sc` as `xorKey || staticTail` (§3.7) and enables encryption according to `encryptionFlag`.

**L2J Mobius CT 2.6 HighFive quirk:** the reference server sends `encryptionFlag = 0`, which disables the XOR stream cipher for the entire session — every subsequent packet (including AuthRequest) travels as plaintext. A correct client must honor this flag and only apply the XOR cipher when it is non-zero.

The reference client passes `encryptionFlag` directly into its crypt layer (`this.crypt.initKey(xorKeyData, useEncryption)`), and the crypt layer's `encrypt`/`decrypt` methods short-circuit to the identity function when `enabled = false`. In other words, a reimplementer is not required to special-case "encryption disabled" in the packet dispatcher — a no-op crypt object is the cleanest factoring.

#### 5.3.3 AuthRequest (C→S, opcode `0x2B`) — first packet after CryptInit (encrypted iff `CryptInit.encryptionFlag ≠ 0`)

| Offset | Field        | Type  | Notes                            |
| ------ | ------------ | ----- | -------------------------------- |
| 0      | opcode       | `u8`  | `0x2B`                           |
| 1      | `username`   | `str` | UTF-16LE, 2-byte null terminator |
| var    | `playOkId2`  | `i32` | **note the swapped order**       |
| var+4  | `playOkId1`  | `i32` |                                  |
| var+8  | `loginOkId1` | `i32` |                                  |
| var+12 | `loginOkId2` | `i32` |                                  |

**The field order `play2, play1, login1, login2` is mandatory** — getting it wrong silently breaks auth on L2J Mobius.

#### 5.3.4 CharSelectionInfo (S→C, opcode `0x09`)

**Header:**

| Offset | Field             | Type          | Notes                 |
| ------ | ----------------- | ------------- | --------------------- |
| 0      | opcode            | `u8` = `0x09` |                       |
| 1      | `charCount`       | `i32`         | number of records     |
| 5      | `maxChars`        | `i32`         | account character cap |
| 9      | reserved          | `u8`          | ignored               |
| 10     | character records | variable      | see below             |

**Per-character record (variable length due to two embedded `str` fields):**

| #   | Field                        | Type        | Notes                                               |
| --- | ---------------------------- | ----------- | --------------------------------------------------- |
| 1   | `name`                       | `str`       | UTF-16LE + `u16 0x0000`                             |
| 2   | `objectId`                   | `i32`       | unique character id                                 |
| 3   | `loginName`                  | `str`       | account login                                       |
| 4   | `sessionId`                  | `i32`       | echoes the login session token                      |
| 5   | `clanId`                     | `i32`       | `0` if no clan                                      |
| 6   | `builderLevel`               | `i32`       |                                                     |
| 7   | `sex`                        | `i32`       | `0`=male, `1`=female                                |
| 8   | `race`                       | `i32`       |                                                     |
| 9   | `baseClassId`                | `i32`       |                                                     |
| 10  | `gameServerName`             | `i32`       | server id                                           |
| 11  | `x`, `y`, `z`                | `i32` × 3   | last known coords                                   |
| 12  | `hp`, `mp`                   | `f64` × 2   | current                                             |
| 13  | `sp`                         | `i32`       |                                                     |
| 14  | `exp`                        | `i64`       |                                                     |
| 15  | `expPct`                     | `f64`       | HighFive: progress toward next level                |
| 16  | `level`                      | `i32`       |                                                     |
| 17  | `karma`, `pkKills`, `pvpKills` | `i32` × 3 |                                                     |
| 18  | reserved                     | `i32` × 7   | zeros                                               |
| 19  | `paperdoll[0..17]`           | `i32` × 17  | item ids per paperdoll slot                         |
| 20  | `hairStyle`, `hairColor`, `face` | `i32` × 3 |                                                 |
| 21  | `maxHp`, `maxMp`             | `f64` × 2   |                                                     |
| 22  | `deleteTimer`                | `i32`       | seconds remaining, or `0`                           |
| 23  | `classId`                    | `i32`       | current (subclass) class id                         |
| 24  | `active`                     | `i32`       | `!=0` → last-played character                       |
| 25  | `enchantEffect`              | `u8`        |                                                     |
| 26  | `augmentation`               | `i32`       |                                                     |
| 27  | `transform`                  | `i32`       |                                                     |
| 28  | pet info                     | `i32` × 5 + `f64` × 2 | id/name-id/level/max-hp/max-mp/etc.       |
| 29  | `vitality`                   | `i32`       |                                                     |

The auto-login algorithm does not need any of these fields beyond the count — it picks `CONFIG.CharSlotIndex` (default `0`) and sends CharacterSelected. A reimplementer that wants to display or filter the list must parse each record in order; the layout above matches what L2J Mobius CT 2.6 HighFive emits.

#### 5.3.5 CharacterSelected (C→S, opcode `0x12`)

Total body size: **19 bytes**.

| Offset | Field       | Type  | Value   |
| ------ | ----------- | ----- | ------- |
| 0      | opcode      | `u8`  | `0x12`  |
| 1      | `slotIndex` | `i32` | 0-based |
| 5      | `unk1`      | `i16` | `0`     |
| 7      | `unk2`      | `i32` | `0`     |
| 11     | `unk3`      | `i32` | `0`     |
| 15     | `unk4`      | `i32` | `0`     |

**All four trailing fields are mandatory on L2J Mobius** — the server reads them (`cd` followed by `hddd` in dispatch terms) and will disconnect on underflow. On the wire they are 14 zero bytes; the field breakdown matches the server's `readH()/readD()` sequence.

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

#### 5.4.1 NetPingRequest (S→C, opcode `0xD3`)

| Offset | Field    | Type          |
| ------ | -------- | ------------- |
| 0      | opcode   | `u8` = `0xD3` |
| 1      | `pingId` | `i32`         |

#### 5.4.2 NetPing (C→S, opcode `0xA8`)

**Observed on the wire: 5-byte body.** The reference client's live ping handler writes just the opcode and the echoed `pingId`:

| Offset | Field    | Type  | Value                    |
| ------ | -------- | ----- | ------------------------ |
| 0      | opcode   | `u8`  | `0xA8`                   |
| 1      | `pingId` | `i32` | echo from NetPingRequest |

A 13-byte variant also exists in the codebase, adding two trailing `i32` constants:

| Offset | Field    | Type  | Value        |
| ------ | -------- | ----- | ------------ |
| 5      | reserved | `i32` | `0x00000000` |
| 9      | unknown  | `i32` | `0x00080000` |

The 13-byte class is not currently invoked at runtime; it is retained because packet captures from several official L2 clients show those trailing constants. A reimplementer should emit the **5-byte form** to match L2J Mobius, and may emit the 13-byte form when targeting more lenient servers. L2J Mobius accepts both, as long as the body begins with the opcode and a valid `pingId`.

### 5.5 Representative gameplay packets

These packets are not required to enter the world, but are included so that a reimplementer knows the pattern used for common commands. All are subject to the XOR cipher when §5.3.2's `encryptionFlag` is non-zero.

| Opcode        | Name                                 | Body (beyond opcode)                                                                                                 |
| ------------- | ------------------------------------ | -------------------------------------------------------------------------------------------------------------------- |
| `0x01`        | MoveToLocation                       | `i32 targetX, i32 targetY, i32 targetZ, i32 originX, i32 originY, i32 originZ, i32 movementMode` (`1` = mouse click) |
| `0x04`        | Action                               | `i32 objectId, i32 originX, i32 originY, i32 originZ, u8 shiftClick`                                                 |
| `0x0A`        | AttackRequest                        | `i32 objectId, i32 originX, i32 originY, i32 originZ, u8 shiftClick`                                                 |
| `0x14`        | **UseItem** _or_ **RequestItemList** | overloaded — see note below                                                                                          |
| `0x17`        | DropItem                             | `i32 objectId, i32 count, i32 x, i32 y, i32 z`                                                                       |
| `0x1B`        | RequestSocialAction                  | `i32 actionId` — see action id table below                                                                           |
| `0x1D`        | ChangeWaitType2                      | `i32 typeStand` (`0`=sit, `1`=stand)                                                                                 |
| `0x29`        | RequestJoinParty                     | `str playerName`                                                                                                     |
| `0x38`        | Say2                                 | `str text, i32 chatType, [str target]` — the `target` field is present only when `chatType` = `24` (whisper)         |
| `0x39`        | UseSkill                             | `i32 skillId, u8 ctrlPressed, u8 shiftPressed`                                                                       |
| `0x63`        | RequestQuestList                     | _(no body)_                                                                                                          |
| `0xD0 0x0008` | EnterGameServer / RequestManorList   | _(no body; extended packet, see §5.3.7)_                                                                             |

**Opcode `0x14` is overloaded C→S on HighFive.** Both `UseItem` (5-byte body: opcode + `i32 itemObjectId`) and `RequestItemList` / `RequestInventoryOpen` (1-byte body: opcode only) use the same opcode. The server disambiguates by the post-opcode body length — a 4-byte payload is a use-item request, an empty payload is an item-list request. On CT_0_Interlude the item-list opcode is `0x15` instead; for HighFive always use `0x14` with the appropriate body length.

**Extended opcode `0xD0 0x0008` is overloaded C→S.** Both `EnterGameServer` and `RequestManorList` emit the same 3-byte body; the server interprets the packet according to the current session phase (handshake vs. in-game). A reimplementer does not usually need to send `EnterGameServer` at all — it exists in the reference implementation for CT_0-style flows.

**RequestSocialAction action ids** (body is `i32`).

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

- `0xD3` **NetPingRequest** — reply with NetPing (§5.4) or the server will drop the connection after ~60 seconds.
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
  |<-- NetPingRequest (0xD3) --------------------------|       |
  |--- NetPing (0xA8) --------------------------------->      |
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
body = bytes([0x07]) + i32_le(sessionId) + zeros(16)    # body = 21 bytes
send_login_encrypted(loginSock, body, currentLoginKey)

pkt = read_framed(loginSock)
gg = decrypt_login(pkt.body, currentLoginKey)     # Blowfish + verify checksum
assert gg[0] == 0x0B
# ggAuthResponse is not echoed back by L2J Mobius; any value is ignored.

# --- RequestAuthLogin (0x00) ---
plaintext = zeros(94) + ascii_right_padded(username, 14) + zeros(2)
          + ascii_right_padded(password, 16) + zeros(2)               # 128 bytes
rsaCipher = rsa_encrypt_no_padding(plaintext, rsaModulus, e=65537)    # 128 bytes
body = bytes([0x00]) + rsaCipher + i32_le(0) + i32_le(0) + zeros(8)   # body = 145 bytes
send_login_encrypted(loginSock, body, currentLoginKey)

pkt = read_framed(loginSock)
ok = decrypt_login(pkt.body, currentLoginKey)
if ok[0] == 0x01: abort("LoginFail reason=" + str(ok[1]))
assert ok[0] == 0x03
loginOkId1 = i32_le(ok[1:5])
loginOkId2 = i32_le(ok[5:9])

# --- RequestServerList (0x05) ---
body = bytes([0x05]) + i32_le(loginOkId1) + i32_le(loginOkId2) + bytes([0x05])
send_login_encrypted(loginSock, body, currentLoginKey)

pkt = read_framed(loginSock)
sl = decrypt_login(pkt.body, currentLoginKey)
assert sl[0] == 0x04
count = sl[1]; pos = 3
servers = []
for i in 0..count:
    rec = parse_server_record(sl[pos : pos+23])   # §4.6
    pos += 23
    servers.append(rec)

chosen = first(s for s in servers if s.serverId == targetServerId)
if chosen is None: abort("ServerId not found")

# --- RequestServerLogin (0x02) ---
body = bytes([0x02]) + i32_le(loginOkId1) + i32_le(loginOkId2) + bytes([chosen.serverId])
send_login_encrypted(loginSock, body, currentLoginKey)

pkt = read_framed(loginSock)
po = decrypt_login(pkt.body, currentLoginKey)
if po[0] == 0x06: abort("PlayFail reason=" + str(i32_le(po[1:5])))
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
    if body[0] == 0xD3:
        pingId = i32_le(body[1:5])
        # L2J Mobius HighFive observed form: opcode + pingId only (5-byte body).
        pong   = bytes([0xA8]) + i32_le(pingId)
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

### 6.4 Error handling expected from a correct client

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
- [ ] Login state machine with all 7 packets (§4.3 — §4.13).
- [ ] ServerList parsing with 21-byte records (§4.6).
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
- [ ] NetPing (0xA8) answer to every NetPingRequest (0xD3) with a **5-byte body** = `u8 0xA8 + i32 pingId`. The legacy 13-byte form (`+ 0x00000000 + 0x00080000`) is optional.
- [ ] Handle the overloaded `0x14` opcode correctly on C→S: 5-byte body = UseItem, 1-byte body = RequestItemList.
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
| RequestServerList flags           | `u8 = 0x05`                                                    | §4.12                    |
| RequestGGAuth trailing            | 16 zero bytes after `sessionId` (no GG constants)              | §4.13                    |
| RequestAuthLogin trailing         | `loginOkId1 (i32) + loginOkId2 (i32) + 8 zero bytes` (all zeros on first login) | §4.10   |
| RSA plaintext layout              | 94 zero / 14 login / 2 zero / 16 password / 2 zero = 128 bytes | §3.4                     |
| RSA public exponent               | `65537` (`0x10001`)                                            | §3.4                     |
| CharacterSelected padding         | 14 zero bytes after `slotIndex` (`i16 + i32 + i32 + i32`)      | §5.3.5                   |
| EnterWorld padding                | 104 zero bytes after opcode                                    | §5.3.8                   |
| NetPing observed wire form        | opcode + `i32 pingId` (5-byte body)                            | §5.4.2                   |
| NetPing legacy trailing constants | `0x00000000`, `0x00080000` (optional)                          | §5.4.2                   |
| Maximum packet length             | `0xFFFF` (= 65 533-byte body)                                  | §2.3                     |

**LoginFail reason codes** (§4.4):

| Code   | Meaning                              |
| ------ | ------------------------------------ |
| `0x01` | Account does not exist               |
| `0x02` | Password is incorrect                |
| `0x03` | Password does not match this account |
| `0x04` | Account is banned                    |
| `0x05` | Account is already in use            |
| `0x06` | Server is under maintenance          |
| `0x07` | Account is already in use            |
| `0x08` | Server is full                       |
| `0x09` | Server is under maintenance          |
| `0x0A` | Login is currently prohibited        |
| `0x0B` | Server is full (queue)               |

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

**Overloaded C→S opcodes** (§5.5):

| Opcode        | First interpretation  | Second interpretation         | Disambiguation |
| ------------- | --------------------- | ----------------------------- | -------------- |
| `0x14`        | UseItem (4-byte body) | RequestItemList (0-byte body) | Body length    |
| `0xD0 0x0008` | EnterGameServer       | RequestManorList              | Session phase  |

---
