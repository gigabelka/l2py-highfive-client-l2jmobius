# Implementation checklist

Use this list when porting to a new language. Tick every box to have a working auto-login client. Opcode and constant reference: [CONSTANTS.md](CONSTANTS.md); per-packet specs: [PROTOCOL.md](PROTOCOL.md); crypto primitives: [CRYPTOGRAPHY.md](CRYPTOGRAPHY.md).

- [ ] TCP connection with `u16 LE` length-prefixed frame reassembly.
- [ ] Blowfish ECB 16-round cipher, little-endian byte-to-DWORD conversion.
- [ ] Static login Blowfish key — see [Login Blowfish keys](CRYPTOGRAPHY.md#login-blowfish-keys).
- [ ] Init packet decryption = Blowfish(static) + rolling XOR reverse + drop trailing 8 bytes.
- [ ] Per-packet NewCrypt XOR checksum (compute on send, verify on recv) over 4-byte DWORDs with last 4 bytes holding the result.
- [ ] Login-packet padding: 4-byte align → +8 zeros → 8-byte align → write checksum → Blowfish encrypt.
- [ ] RSA modulus unscrambler (C^-1, B^-1, A^-1, D^-1 in that order).
- [ ] RSA-1024 encryption with `RSA_NO_PADDING`, exponent 65537, 128-byte plaintext layout — see [RSA-1024](CRYPTOGRAPHY.md#rsa-1024-for-credential-submission).
- [ ] Login state machine with all 7 packets (see [Login Server protocol](PROTOCOL.md#login-server-protocol)). On HighFive,
      body sizes are: Init 184, GGAuth 32 (only first i32
      matters), LoginOk 56 (only first 9 bytes matter), ServerList
      3+N·21+trailer, PlayOk 16 (only first 9 bytes matter), RequestGGAuth
      32 (or 21 minimal), RequestAuthLogin 184 (or 137 minimal),
      RequestServerList 24 (or 10 minimal), RequestServerLogin 24 (or 10
      minimal).
- [ ] ServerList parsing with 21-byte records (see [ServerList](PROTOCOL.md#serverlist-s-c-opcode-0x04)); skip the trailing
      block — it is per-server character counts that auto-login does not need.
- [ ] Transition to Game Server using `gameServerIp:gameServerPort` from the matched ServerList record.
- [ ] Game packet framing same as login; XOR cipher only after CryptInit.
- [ ] Static game XOR tail — see [Game XOR stream cipher](CRYPTOGRAPHY.md#game-xor-stream-cipher).
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
- [ ] Rotate `key_sc[8..12]` by the body size for **every** decrypted packet — even the ones whose opcode is unrecognised — or the XOR stream desynchronises (see [Server-to-client packets beyond the handshake](PROTOCOL.md#server-to-client-packets-beyond-the-handshake)).
- [ ] Never disconnect on an unknown opcode; log and drop the packet instead (see [Server-to-client packets beyond the handshake](PROTOCOL.md#server-to-client-packets-beyond-the-handshake)).
