# Cryptography

This document describes the cryptographic primitives used by the Lineage 2 HighFive protocol: Blowfish for the login phase, RSA-1024 (no padding) for credential submission, and an L2-specific XOR stream cipher for the game phase. Constants index: [CONSTANTS.md](CONSTANTS.md); packets that use these primitives: [PROTOCOL.md](PROTOCOL.md).

Three independent cryptographic primitives are used: Blowfish (login phase), RSA-1024 with no padding (credential submission only), and an L2-specific 16-byte XOR stream cipher (game phase).

## Blowfish (login phase)

Standard Blowfish in **ECB mode**, 16 Feistel rounds, 64-bit block, P-array of 18 DWORDs, 4 S-boxes of 256 DWORDs each. Any production Blowfish library will work; the L2 protocol uses no tweaks.

- **Block size:** 8 bytes. All login packets to be encrypted/decrypted are padded to a multiple of 8 bytes before encryption and are whole-number-of-8-blocks after decryption.
- **Byte order inside a block:** Blowfish internally consumes two 32-bit halves. The L2 implementation uses **little-endian** `bytesTo32Bits`, which is the standard OpenSSL / Bouncy Castle convention for packet-based Blowfish.
- **Key length:** 16 bytes (both the static login key and the session key returned in Init).

## NewCrypt XOR checksum (login phase, post-Init)

Every login packet after Init is protected by a 32-bit XOR checksum written in the last 4 bytes of the (already-padded) body.

**Compute / verify algorithm** (little-endian, 4-byte DWORDs):

```
sum = 0
for i in 0, 4, 8, ..., size - 8:       # every DWORD except the last one
    sum ^= u32_le(raw[i..i+4])
# last 4 bytes of raw hold the checksum (or must be overwritten with `sum`)
```

The `size` MUST be a multiple of 4 and strictly greater than 4.

## NewCrypt rolling XOR (Init packet only)

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

## RSA-1024 for credential submission

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
| `0x6C` | 16   | password, ASCII, null-padded (immediately follows login, no separator)        |
| `0x7C` | 4    | zeros                                                                         |

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

## Login Blowfish keys

**Static key** (used _only_ to decrypt the Init packet):

```
6B 60 CB 5B 82 CE 90 B1 CC 2B 6C 55 6C 6C 6C 6C
```

**Session key** — 16 bytes received inside Init, at offset 153 of the body (after opcode+sessionId+protocolRev+scrambledRsaKey+16 reserved bytes). It is used for all login packets after Init, in both directions.

## Login packet encryption pipelines

**Decrypt the Init packet (S→C, opcode `0x00`):**

```
body_enc = raw[2..]                         # strip u16 length
plain    = blowfish_ecb_decrypt(body_enc, STATIC_KEY)   # whole body (multiple of 8)
seed     = u32_le(plain[size - 8 .. size - 4])
rolling_xor_reverse(plain, seed)            # see NewCrypt rolling XOR (Init packet only)
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

## Game XOR stream cipher

After the game-side handshake (see [Game Server handshake](PROTOCOL.md#handshake-packets)) the client receives 8 bytes of server-chosen XOR key. The full 16-byte key is formed by appending a fixed 8-byte tail:

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

**First packet rule (HighFive):** on HighFive the very first packet the server sends (CryptInit, see [Game Server handshake](PROTOCOL.md#handshake-packets)) and the very first packet the client sends (ProtocolVersion, same section) are **plaintext** because the key has not yet been established. Whether packets after CryptInit are encrypted is controlled by CryptInit's `encryptionFlag`: if non-zero, all subsequent packets (starting with the client's AuthRequest) are XOR-encrypted; if zero, the entire session stays plaintext. On HighFive the server sends `encryptionFlag = 0` — see [Game Server handshake](PROTOCOL.md#handshake-packets).

## Test vectors

The following vectors can be used to self-verify a port. All input/output is expressed as hex bytes in wire order; no language features or library APIs are implied.

### Blowfish-ECB with the static login key

Port-level sanity check that the Blowfish key schedule uses little-endian `bytesTo32Bits` (see [Blowfish](#blowfish-login-phase)).

```
key        : 6B 60 CB 5B 82 CE 90 B1 CC 2B 6C 55 6C 6C 6C 6C
plaintext  : 00 11 22 33 44 55 66 77
ciphertext : 46 AA DA CC 2D 39 90 61
```

Round-trip: `Blowfish_decrypt(ciphertext, key) == plaintext`.

### NewCrypt checksum

Input is a 16-byte body whose last 4 bytes are the checksum slot (zero on input). After the algorithm those 4 bytes become the XOR of the three preceding DWORDs. (See [NewCrypt XOR checksum](#newcrypt-xor-checksum-login-phase-post-init).)

```
input  : AA BB CC DD  01 02 03 04  10 20 30 40  00 00 00 00
output : AA BB CC DD  01 02 03 04  10 20 30 40  BB 99 FF 99
```

Verification: XOR of `0xDDCCBBAA ^ 0x04030201 ^ 0x40302010` is `0x99FF99BB`, whose little-endian bytes are `BB 99 FF 99` — identical to the last 4 bytes of `output`.

### NewCrypt rolling XOR

The `decXORPass` operation walks a 24-byte buffer backwards. The last 8 bytes carry the seed (4 bytes) and an unused tail (4 bytes) and are never touched by the pass. The first 4 bytes are also untouched because the loop stops at offset 4. Only the middle three DWORDs mutate. (See [NewCrypt rolling XOR (Init packet only)](#newcrypt-rolling-xor-init-packet-only).)

```
seed     : 0x78563412 (read as u32 LE from bytes [size-8..size-4])
input    : DE AD BE EF  11 22 33 44  55 66 77 88  99 AA BB CC  12 34 56 78  00 00 00 00
output   : DE AD BE EF  A4 83 7B 3C  D2 F3 1F 4B  8B 9E ED B4  12 34 56 78  00 00 00 00
```

### RSA modulus unscramble

Deterministic input: `byte[i] = i` for `i ∈ [0, 0x80)`. The full 128-byte unscrambled modulus, in 16-byte rows. (See [RSA-1024 for credential submission](#rsa-1024-for-credential-submission).)

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

### Game XOR stream cipher

Encrypt a 5-byte plaintext with a 16-byte key whose first 8 bytes are a trivial seed and whose last 8 are the static tail. After encryption, the DWORD at bytes `[8..12]` increases by `N = 5`. (See [Game XOR stream cipher](#game-xor-stream-cipher).)

```
key (before)     : 00 01 02 03  04 05 06 07  C8 27 93 01  A1 6C 31 97
plaintext        : 11 22 33 44 55
ciphertext (C→S) : 11 32 03 44 15
key (after N=5)  : 00 01 02 03  04 05 06 07  CD 27 93 01  A1 6C 31 97
```

Round-trip: running the S→C decrypt on `ciphertext` with `key (before)` reproduces `plaintext`.
