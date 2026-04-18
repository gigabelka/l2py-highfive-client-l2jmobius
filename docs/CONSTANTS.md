# Constants appendix

Reference tables: magic constants, reason codes, action ids, duplicated opcodes. Packet body specs live in [PROTOCOL.md](PROTOCOL.md); crypto primitives in [CRYPTOGRAPHY.md](CRYPTOGRAPHY.md).

| Name                              | Value                                                          | Used in                  |
| --------------------------------- | -------------------------------------------------------------- | ------------------------ |
| Protocol version (HighFive)       | `273` (also `267`, `268`, `271`)                               | [ProtocolVersion](PROTOCOL.md#protocolversion-c-s-opcode-0x0e--plaintext) |
| Expected Init protocol revision   | `0x0000C621`                                                   | [Init](PROTOCOL.md#init-s-c-opcode-0x00) |
| Static login Blowfish key         | `6B 60 CB 5B 82 CE 90 B1 CC 2B 6C 55 6C 6C 6C 6C`              | [Init decryption](CRYPTOGRAPHY.md#login-blowfish-keys) |
| Static game XOR tail              | `C8 27 93 01 A1 6C 31 97`                                      | [XOR key](CRYPTOGRAPHY.md#game-xor-stream-cipher) |
| RequestServerList minimal body    | 9 bytes (opcode + 2×i32); the server ignores any trailer       | [RequestServerList](PROTOCOL.md#requestserverlist-c-s-opcode-0x05) |
| RequestGGAuth body shape          | 32 bytes; server reads 21 (opcode + sessionId + 16 zeros)      | [RequestGGAuth](PROTOCOL.md#requestggauth-c-s-opcode-0x07) |
| RequestAuthLogin body shape       | 184 bytes; opcode + 128-byte RSA + 55-byte GG trailer          | [RequestAuthLogin](PROTOCOL.md#requestauthlogin-c-s-opcode-0x00) |
| RSA plaintext layout              | 94 zero / 14 login / 2 zero / 16 password / 2 zero = 128 bytes | [RSA-1024](CRYPTOGRAPHY.md#rsa-1024-for-credential-submission) |
| RSA public exponent               | `65537` (`0x10001`)                                            | [RSA-1024](CRYPTOGRAPHY.md#rsa-1024-for-credential-submission) |
| CharacterSelected trailing fields | `i16 + 3×i32` (= 14 bytes of typed zeros) after `slotIndex`    | [CharacterSelected](PROTOCOL.md#characterselected-c-s-opcode-0x12) |
| EnterWorld padding                | 104 zero bytes after opcode                                    | [EnterWorld](PROTOCOL.md#enterworld-c-s-opcode-0x11) |
| NetPingRequest opcode (S→C)       | `0xD9`                                                         | [NetPingRequest](PROTOCOL.md#netpingrequest-s-c-opcode-0xd9) |
| NetPing opcode (C→S)              | `0xB1`, 5-byte body (`u8 + i32 pingId`)                        | [NetPing](PROTOCOL.md#netping-c-s-opcode-0xb1) |
| Maximum packet length             | `0xFFFF` (= 65 533-byte body)                                  | [Packet framing](PROTOCOL.md#packet-framing) |

**LoginFail reason codes** (see [LoginFail](PROTOCOL.md#loginfail-s-c-opcode-0x01)):

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

**PlayFail reason codes** (see [PlayFail](PROTOCOL.md#playfail-s-c-opcode-0x06)):

| Code   | Meaning                 |
| ------ | ----------------------- |
| `0x03` | Password mismatch       |
| `0x04` | Access error, try later |
| `0x0F` | Too many players        |

**RequestSocialAction action ids** (see [Representative gameplay packets](PROTOCOL.md#representative-gameplay-packets)):

| Id  | Action    | Id   | Action  |
| --- | --------- | ---- | ------- |
| `1` | Stand/Sit | `8`  | Unaware |
| `2` | Greeting  | `9`  | Waiting |
| `3` | Victory   | `10` | Laugh   |
| `4` | Advance   | `11` | Think   |
| `5` | No        | `12` | Applaud |
| `6` | Yes       | `13` | Dance   |
| `7` | Bow       |      |         |

**Duplicated C→S opcodes on CT 2.6 HighFive** (see [Representative gameplay packets](PROTOCOL.md#representative-gameplay-packets)):

| Opcode | Handler class   | Notes                                                       |
| ------ | --------------- | ----------------------------------------------------------- |
| `0x01` | `AttackRequest` | basic attack; same class also registered at `0x32`          |
| `0x32` | `AttackRequest` | alternate attack opcode; identical behaviour to `0x01`      |

There is no body-length or phase-based opcode overloading on CT 2.6 — the
Interlude-era claims about `0x14` (UseItem/RequestItemList) and
`0xD0 0x0008` (EnterGameServer/RequestManorList) do not apply to this
chronicle.
