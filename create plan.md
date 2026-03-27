# План переписывания L2 HighFive Client (Login Flow) на Python 3.14

## Анализ исходного проекта

### Что представляет собой проект

**l2ts-highfive-client-l2jmobius** — это TypeScript-клиент для Lineage 2 (хроника High Five), совместимый с сервером L2JMobius. Проект основан на архитектуре `l2js-client` (npetrovski/l2js-client) и реализует сетевой протокол L2 для программного управления клиентом (боты, автотесты, утилиты).

### Архитектура оригинала (TypeScript)

```
src/
├── Client.ts                    # Главный фасад — метод enter() запускает весь flow
├── network/
│   ├── LoginClient.ts           # TCP-соединение с Login Server (порт 2106)
│   ├── GameClient.ts            # TCP-соединение с Game Server
│   ├── clientpackets/           # Пакеты от клиента к серверу
│   │   ├── AuthGameGuard.ts     # C/0x07 — подтверждение GameGuard
│   │   ├── RequestAuthLogin.ts  # C/0x00 — логин + пароль (RSA-шифрование)
│   │   ├── RequestServerList.ts # C/0x05 — запрос списка серверов
│   │   ├── RequestServerLogin.ts# C/0x02 — выбор сервера
│   │   └── ...game packets...
│   ├── serverpackets/           # Пакеты от сервера к клиенту
│   │   ├── Init.ts              # S/0x00 — инициализация (Blowfish-ключ, RSA-ключ)
│   │   ├── GGAuth.ts            # S/0x0b — ответ на GameGuard
│   │   ├── LoginOk.ts           # S/0x03 — авторизация успешна
│   │   ├── ServerList.ts        # S/0x04 — список серверов
│   │   ├── PlayOk.ts            # S/0x07 — можно подключаться к Game Server
│   │   └── ...game packets...
│   └── crypto/
│       ├── BlowfishEngine.ts    # Blowfish-шифрование (блоки 8 байт)
│       ├── LoginCrypt.ts        # Крипто для Login Server
│       ├── GameCrypt.ts         # XOR-шифрование для Game Server
│       └── RSA.ts               # RSA для шифрования логина/пароля
├── entities/                    # Игровые объекты
│   ├── L2User.ts
│   ├── L2Character.ts
│   └── ...
├── events/                      # Система событий
│   └── EventTypes.ts
├── commands/                    # Команды (say, moveTo, hit...)
│   └── AbstractGameCommand.ts
└── enums/                       # Перечисления
```

### Полный flow входа персонажа в игру

```
┌─────────────────────────────────────────────────────────┐
│ ФАЗА 1: LOGIN SERVER (TCP порт 2106)                   │
├─────────────────────────────────────────────────────────┤
│ 1. Клиент подключается к Login Server                   │
│ 2. S/0x00 Init ← сервер: Blowfish-ключ сессии + RSA-ключ│
│ 3. C/0x07 AuthGameGuard → клиент: session_id            │
│ 4. S/0x0b GGAuth ← сервер: подтверждение                │
│ 5. C/0x00 RequestAuthLogin → клиент: логин+пароль (RSA) │
│ 6. S/0x03 LoginOk ← сервер: login_ok1 + login_ok2      │
│ 7. C/0x05 RequestServerList → клиент: login_ok1/ok2     │
│ 8. S/0x04 ServerList ← сервер: список серверов          │
│ 9. C/0x02 RequestServerLogin → клиент: server_id        │
│10. S/0x07 PlayOk ← сервер: play_ok1 + play_ok2         │
│ → Отключение от Login Server                            │
├─────────────────────────────────────────────────────────┤
│ ФАЗА 2: GAME SERVER (TCP порт из ServerList)            │
├─────────────────────────────────────────────────────────┤
│11. Клиент подключается к Game Server                    │
│12. C: ProtocolVersion → клиент (НЕ шифруется)          │
│13. S: KeyPacket ← сервер: XOR-ключ для шифрования      │
│14. C: AuthLogin → клиент: session keys из Login Server  │
│15. S: CharSelectionInfo ← сервер: список персонажей     │
│16. C: CharacterSelect → клиент: slot_index              │
│17. S: CharSelected ← сервер: данные выбранного перса    │
│18. C: EnterWorld → клиент                               │
│19. S: UserInfo ← сервер: полная информация о персонаже  │
│ → Персонаж в игре, событие "LoggedIn"                   │
└─────────────────────────────────────────────────────────┘
```

### Криптография

| Этап                     | Алгоритм       | Детали                                                    |
| ------------------------ | -------------- | --------------------------------------------------------- |
| Login Init (S/0x00)      | XOR + Blowfish | Шифруется статическим Blowfish-ключом (зашит в клиент)    |
| Login остальные пакеты   | Blowfish       | Ключ из Init-пакета, checksum перед шифрованием           |
| Login → RequestAuthLogin | RSA            | Логин и пароль дополнительно RSA-шифруются                |
| Game первый пакет        | Без шифрования | ProtocolVersion отправляется открыто                      |
| Game остальные пакеты    | XOR            | Двухчастный ключ: динамический (от сервера) + статический |

### Целевая структура Python-проекта

```
l2py/
├── pyproject.toml
├── README.md
├── src/
│   └── l2py/
│       ├── __init__.py
│       ├── client.py              # Главный фасад L2Client
│       ├── config.py              # Pydantic-модели конфигурации
│       ├── protocol/
│       │   ├── __init__.py
│       │   ├── base.py            # Базовые классы пакетов + PacketBuffer
│       │   ├── login/
│       │   │   ├── __init__.py
│       │   │   ├── client_packets.py   # AuthGameGuard, RequestAuthLogin и т.д.
│       │   │   └── server_packets.py   # Init, GGAuth, LoginOk и т.д.
│       │   └── game/
│       │       ├── __init__.py
│       │       ├── client_packets.py   # ProtocolVersion, AuthLogin и т.д.
│       │       └── server_packets.py   # KeyPacket, CharSelectionInfo и т.д.
│       ├── network/
│       │   ├── __init__.py
│       │   ├── login_connection.py  # asyncio TCP к Login Server
│       │   └── game_connection.py   # asyncio TCP к Game Server
│       ├── crypto/
│       │   ├── __init__.py
│       │   ├── blowfish.py         # Blowfish ECB (блоки 8 байт)
│       │   ├── login_crypt.py      # Checksum + Blowfish для Login
│       │   ├── game_crypt.py       # XOR-шифрование для Game
│       │   └── rsa.py              # RSA для логина
│       ├── models/
│       │   ├── __init__.py
│       │   ├── server.py           # GameServer dataclass
│       │   └── character.py        # CharacterInfo dataclass
│       └── events.py               # Типизированная система событий
├── tests/
│   ├── __init__.py
│   ├── test_crypto/
│   │   ├── test_blowfish.py
│   │   ├── test_login_crypt.py
│   │   └── test_xor_cipher.py
│   ├── test_protocol/
│   │   ├── test_packet_buffer.py
│   │   └── test_login_packets.py
│   └── test_integration/
│       └── test_login_flow.py
└── examples/
    └── login_example.py
```

---

## Пошаговый план: промты для Kimi 2.5

> Каждый шаг — отдельный промт. Копируй и отправляй последовательно.
> Между шагами проверяй результат перед отправкой следующего.

---

### ШАГ 1. Инициализация проекта и конфигурация

```
Ты — опытный Python-разработчик. Мы создаём с нуля проект l2py — asyncio-клиент
для Lineage 2 High Five (совместимый с L2JMobius сервером) на Python 3.14.
Сейчас реализуем только login flow (вход персонажа в игру).

Создай структуру проекта:

1. pyproject.toml — используй:
   - build-system: hatchling
   - python >= 3.14
   - dependencies: pycryptodome >= 3.20 (для Blowfish и RSA)
   - dev dependencies: pytest, pytest-asyncio, ruff
   - ruff config: line-length = 99, target-version = "py314"

2. src/l2py/__init__.py — экспортируй L2Client (пока заглушка)

3. src/l2py/config.py — Pydantic-подобные dataclass'ы (используй
   стандартные dataclasses, без внешних зависимостей):
   - LoginConfig: host (str), port (int = 2106)
   - Credentials: username (str), password (str)
   - ConnectionConfig: server_id (int = 1), char_slot (int = 0)

4. README.md — краткое описание проекта на русском + usage example

Принципы:
- Type hints везде
- Docstrings на русском в Google-стиле
- Код на английском, комментарии на русском
- Используй __all__ в каждом __init__.py
```

---

### ШАГ 2. PacketBuffer — работа с бинарными данными

```
Контекст: мы создаём l2py — Python 3.14 asyncio-клиент для Lineage 2 High Five.
Все данные передаются по TCP как байтовые массивы в Little Endian.

Создай файл src/l2py/protocol/base.py:

Класс PacketReader:
- Обёртка над bytes/bytearray для последовательного чтения
- Внутренний offset (позиция чтения)
- Методы:
  - read_byte() -> int  # 1 байт unsigned
  - read_int16() -> int  # 2 байта signed, little-endian
  - read_uint16() -> int  # 2 байта unsigned
  - read_int32() -> int  # 4 байта signed
  - read_uint32() -> int  # 4 байта unsigned
  - read_int64() -> int  # 8 байт signed
  - read_bytes(n) -> bytes
  - read_string() -> str  # UTF-16LE строка, заканчивающаяся \x00\x00
  - remaining() -> int  # сколько байт осталось
  - skip(n)  # пропустить n байт

Класс PacketWriter:
- Обёртка над bytearray для последовательной записи
- Методы:
  - write_byte(value: int)
  - write_int16(value: int)
  - write_uint16(value: int)
  - write_int32(value: int)
  - write_uint32(value: int)
  - write_int64(value: int)
  - write_bytes(data: bytes)
  - write_string(value: str)  # UTF-16LE + \x00\x00
  - to_bytes() -> bytes  # финальный результат
  - __len__() -> int

Абстрактные базовые классы:
- ServerPacket(ABC):
  - opcode: ClassVar[int]
  - _reader: PacketReader
  - __init__(data: bytes) — создаёт reader, вызывает _read()
  - абстрактный _read() — парсинг полей из reader

- ClientPacket(ABC):
  - opcode: ClassVar[int]
  - _writer: PacketWriter
  - __init__() — создаёт writer, пишет opcode, вызывает _write()
  - абстрактный _write() — запись полей в writer
  - to_bytes() -> bytes — возвращает writer.to_bytes()

Используй struct.pack / struct.unpack для числовых типов.
Все методы с type hints. Docstrings на русском.
Напиши юнит-тесты в tests/test_protocol/test_packet_buffer.py:
- Тест записи и обратного чтения каждого типа данных
- Тест строки UTF-16LE
- Тест PacketReader с offset'ом
```

---

### ШАГ 3. Криптография — Blowfish + Login Crypt

```
Контекст: проект l2py, Python 3.14. Мы реализуем криптографию Login Server.

Протокол Login Server:
- Первый пакет (Init, S/0x00) шифруется статическим Blowfish-ключом
  и дополнительно XOR-ом (не checksum).
- Все остальные пакеты шифруются Blowfish с ключом из Init-пакета.
  Перед шифрованием к данным добавляется checksum.

Статический Blowfish-ключ (hex, 21 байт):
  6b 60 cb 5b 82 ce 90 b1 cc 8b 6b 55 6e 95 87 03 33 00 00 00 00

Создай файл src/l2py/crypto/blowfish.py:
- Класс L2Blowfish:
  - __init__(key: bytes)
  - encrypt(data: bytes) -> bytes  # ECB, блоки по 8 байт
  - decrypt(data: bytes) -> bytes  # ECB, блоки по 8 байт
  - Использовать pycryptodome: Crypto.Cipher.Blowfish, MODE_ECB
  - ВАЖНО: данные должны быть кратны 8 байтам, дополнять нулями

Создай файл src/l2py/crypto/login_crypt.py:
- Класс LoginCrypt:
  - __init__(static_key: bytes | None = None)
    Если None — использовать STATIC_BLOWFISH_KEY
  - set_key(key: bytes) — установить сессионный Blowfish-ключ
  - decrypt_init(data: bytes) -> bytes:
    1. Blowfish decrypt со статическим ключом
    2. XOR-дешифрование (последние 4 байта перед паддингом = XOR-ключ)
  - decrypt(data: bytes) -> bytes:
    1. Blowfish decrypt с сессионным ключом
    2. Проверка checksum
  - encrypt(data: bytes) -> bytes:
    1. Дополнить до кратности 8
    2. Вычислить checksum и добавить (клиент добавляет 16 байт после данных:
       4 байта checksum + 12 байт нулей)
    3. Blowfish encrypt с сессионным ключом

Checksum (XOR-based):
  def _checksum(data: bytes) -> int:
      checksum = 0
      for i in range(0, len(data) - 8, 4):
          checksum ^= int.from_bytes(data[i:i+4], 'little')
      return checksum

Verify checksum:
  - Последние 8 байт: [checksum(4), padding(4)]
  - Вычислить checksum по data[:-8], сравнить с сохранённым

Напиши тесты в tests/test_crypto/test_blowfish.py:
- Тест encrypt/decrypt roundtrip
- Тест с данными некратными 8 (padding)

Напиши тесты в tests/test_crypto/test_login_crypt.py:
- Тест checksum вычисления
- Тест encrypt/decrypt roundtrip через LoginCrypt
```

---

### ШАГ 4. Криптография — RSA для авторизации

```
Контекст: проект l2py, Python 3.14. Реализуем RSA для Login Server.

В пакете Init (S/0x00) сервер L2JMobius присылает RSA public key
(128 байт = 1024-bit модуль). Клиент использует этот ключ для шифрования
логина и пароля перед отправкой в пакете RequestAuthLogin (C/0x00).

ВАЖНО: L2 использует "сырое" RSA (textbook RSA) без OAEP/PKCS1 padding.
Это означает: ciphertext = plaintext^e mod n, где e = 65537.

Создай файл src/l2py/crypto/rsa.py:

Класс L2RSA:
  - __init__(modulus: bytes)
    modulus — 128 байт (1024-bit) от сервера, big-endian
    e = 65537 (0x10001)
  - encrypt(data: bytes) -> bytes:
    - data максимум 128 байт, дополнить нулями справа до 128 если короче
    - plaintext_int = int.from_bytes(data, 'big')
    - cipher_int = pow(plaintext_int, self._e, self._n)
    - return cipher_int.to_bytes(128, 'big')

Реализация через стандартную математику Python (pow с тремя аргументами).
НЕ использовать pycryptodome RSA, так как L2 использует textbook RSA без padding.

ВАЖНО: модуль RSA от L2JMobius приходит в пакете Init в "скремблированном"
виде. Нужна функция unscramble_modulus(modulus: bytes) -> bytes:
  1. Взять 128 байт модуля
  2. Выполнить серию swap-операций:
     for i in range(64):
       modulus[0x00 + i], modulus[0x40 + i] = modulus[0x40 + i], modulus[0x00 + i]
  3. Затем серия XOR + swap по 4 байта (стандартная L2-дескремблировка)
     (см. исходники l2js-client/src/network/serverpackets/Init.ts)

  Если не найдёшь точный алгоритм — сделай заглушку с TODO,
  отметив что для L2JMobius скремблирование может быть отключено.

Напиши тесты:
- Тест encrypt: зашифровать известные данные, проверить длину = 128
- Тест что pow работает корректно с малыми числами
```

---

### ШАГ 5. Криптография — Game XOR Cipher

```
Контекст: проект l2py, Python 3.14. Реализуем XOR-шифрование Game Server.

После подключения к Game Server все пакеты (кроме первого) шифруются XOR.
Ключ состоит из двух частей:
  - dynamic_part (8 байт) — приходит от сервера в KeyPacket
  - static_part (8 байт) — зашит в клиент:
    hex: a1 6c 54 87 09 f1 1c 8d (для High Five / L2JMobius)

Полный ключ: dynamic_part + static_part = 16 байт.

Последние 4 байта dynamic_part инкрементируются на количество обработанных
байт после каждой операции.

Создай файл src/l2py/crypto/game_crypt.py:

Класс GameCrypt:
  - __init__()
  - set_key(dynamic_key: bytes):
    Формирует полный ключ = dynamic_key + STATIC_KEY
    Инициализирует два отдельных состояния:
    - _decrypt_key: bytearray(16)  # для входящих пакетов
    - _encrypt_key: bytearray(16)  # для исходящих пакетов
  - enabled: bool — по умолчанию False, True после set_key()

  - decrypt(data: bytes) -> bytes:
    Если не enabled — вернуть как есть.
    XOR каждый байт data[i] с key[i % len(key)]:
      temp = data[i]
      data[i] = data[i] ^ _decrypt_key[i % key_len]
      _decrypt_key[i % key_len] = temp
    После обработки: инкрементировать последние 4 байта ключа
    на len(data).

  - encrypt(data: bytes) -> bytes:
    Если не enabled — вернуть как есть.
    XOR каждый байт:
      data[i] = data[i] ^ _encrypt_key[i % key_len]
      _encrypt_key[i % key_len] = data[i]
    После обработки: инкрементировать последние 4 байта ключа
    на len(data).

Обрати внимание: при decrypt сначала сохраняем исходный байт, потом XOR-им.
При encrypt — наоборот: сначала XOR-им, потом сохраняем результат.

Напиши тесты в tests/test_crypto/test_xor_cipher.py:
- Тест encrypt → decrypt roundtrip
- Тест что ключ изменяется после каждой операции
- Тест с enabled = False (passthrough)
```

---

### ШАГ 6. Пакеты Login Server

```
Контекст: проект l2py, Python 3.14. Создаём пакеты Login Server.
Используй базовые классы ServerPacket, ClientPacket, PacketReader, PacketWriter
из src/l2py/protocol/base.py (созданы на шаге 2).

Создай src/l2py/protocol/login/server_packets.py:

1. InitPacket(ServerPacket):
   opcode = 0x00
   Поля после парсинга:
   - session_id: int (4 байта)
   - protocol_version: int (4 байта)
   - rsa_key: bytes (128 байт — сырой RSA-модуль)
   - blowfish_key: bytes (16 байт — сессионный ключ)
   Парсинг _read():
     - read_int32() → session_id
     - read_int32() → protocol_version
     - read_bytes(128) → rsa_key
     - пропустить 16 байт (GG-related)
     - read_bytes(16) → blowfish_key
     - пропустить до конца

2. GGAuthPacket(ServerPacket):
   opcode = 0x0b
   Поля: response: int (4 байта)

3. LoginOkPacket(ServerPacket):
   opcode = 0x03
   Поля: login_ok1: int, login_ok2: int (по 4 байта каждое)

4. ServerListPacket(ServerPacket):
   opcode = 0x04
   Поля: servers: list[GameServer]
   Парсинг:
     - size = read_byte() (кол-во серверов)
     - last_server = read_byte()
     - для каждого сервера:
       server_id: int (read_byte)
       ip: str (4 байта → "x.x.x.x")
       port: int (read_int32)
       age_limit: bool (read_byte)
       pvp: bool (read_byte)
       online: int (read_uint16)
       max_online: int (read_uint16)
       status: bool (read_byte)
       ...пропустить оставшиеся поля до следующего сервера

5. PlayOkPacket(ServerPacket):
   opcode = 0x07
   Поля: play_ok1: int, play_ok2: int (по 4 байта)

6. LoginFailPacket(ServerPacket):
   opcode = 0x01
   Поля: reason: int (1 байт — код ошибки)

Создай src/l2py/protocol/login/client_packets.py:

1. AuthGameGuardPacket(ClientPacket):
   opcode = 0x07
   _write(): write_int32(session_id), write_int32(0)*4 (16 нулей) — GG data

2. RequestAuthLoginPacket(ClientPacket):
   opcode = 0x00
   __init__(username, password, session_id, rsa: L2RSA, login_ok1=0, login_ok2=0)
   _write():
     - Сформировать 128-байтный блок:
       [0..13] = нули
       [14..14+len(username)] = username (ASCII)
       [14+username+1..] = password (ASCII)
       Остаток нулями до 128
     - RSA-зашифровать блок
     - write_bytes(rsa_encrypted_128_bytes)
     - write_int32(login_ok1)
     - write_int32(login_ok2)
     - write_bytes(8 нулей) — GG data

3. RequestServerListPacket(ClientPacket):
   opcode = 0x05
   __init__(login_ok1, login_ok2)
   _write(): write_int32(login_ok1), write_int32(login_ok2), write_byte(0x05)

4. RequestServerLoginPacket(ClientPacket):
   opcode = 0x02
   __init__(login_ok1, login_ok2, server_id)
   _write(): write_int32(login_ok1), write_int32(login_ok2), write_byte(server_id)

Создай src/l2py/models/server.py:
  @dataclass GameServer: id, ip, port, online, max_online, status

Напиши тесты для сериализации/десериализации пакетов с мок-данными.
```

---

### ШАГ 7. Пакеты Game Server (только для login flow)

```
Контекст: проект l2py, Python 3.14. Создаём пакеты Game Server,
необходимые ТОЛЬКО для входа персонажа в игру.

Создай src/l2py/protocol/game/server_packets.py:

1. KeyPacket(ServerPacket):
   opcode = 0x2e
   Поля:
   - enabled: bool (read_byte)
   - xor_key: bytes (8 байт — динамическая часть XOR-ключа)
   - server_id: int (4 байта)
   - obfuscation_key: int (4 байта)
   Парсинг: read_byte(), read_bytes(8), skip, read_int32()...
   (точная структура может варьироваться для L2JMobius,
    оставь TODO если не уверен в порядке полей)

2. CharSelectionInfoPacket(ServerPacket):
   opcode = 0x09 (или 0x13 для HF — уточни)
   Поля: characters: list[CharacterInfo]
   Для каждого персонажа парсить:
   - name: str (read_string)
   - login: str (read_string)
   - session_id: int
   - clan_id: int
   - sex: int
   - race: int
   - class_id: int
   - active: bool
   - x, y, z: int (координаты)
   - hp, mp: float
   - sp: int
   - exp: int
   - level: int
   - ...можно пропустить остальное (karma, slots и т.д.)

3. CharSelectedPacket(ServerPacket):
   opcode = 0x15 (уточни для HF)
   Поля: name, session_id, clan_id, sex, race, class_id, x, y, z

4. UserInfoPacket(ServerPacket) — заглушка:
   opcode = 0x32 (или 0x04 для inner opcode в HF)
   Пока только парсить имя и основные статы,
   остальное пометить TODO.

Создай src/l2py/protocol/game/client_packets.py:

1. ProtocolVersionPacket(ClientPacket):
   opcode = 0x0e (или без opcode — первый пакет)
   __init__(protocol_version: int = 267)  # High Five = 267 (0x10B)
   _write():
     write_int32(protocol_version)
     (могут быть дополнительные байты для L2JMobius — оставь TODO)

2. AuthLoginPacket(ClientPacket):
   opcode = 0x2b
   __init__(login, play_ok1, play_ok2, login_ok1, login_ok2)
   _write():
     write_string(login)
     write_int32(play_ok2)
     write_int32(play_ok1)
     write_int32(login_ok1)
     write_int32(login_ok2)

3. CharacterSelectPacket(ClientPacket):
   opcode = 0x12 (или 0x0d для HF — уточни)
   __init__(slot_index: int)
   _write(): write_int32(slot_index)

4. EnterWorldPacket(ClientPacket):
   opcode = 0x11 (уточни для HF)
   _write():
     write_bytes(b"\x00" * 8)  # минимальный payload

Создай src/l2py/models/character.py:
  @dataclass CharacterInfo: name, race, class_id, level, sex, x, y, z, ...

Помечай все опкоды TODO-комментариями с указанием что нужно уточнить
по исходникам L2JMobius.
```

---

### ШАГ 8. Сетевой слой — asyncio TCP-соединения

```
Контекст: проект l2py, Python 3.14. Создаём асинхронный сетевой слой.

Создай src/l2py/network/login_connection.py:

Класс LoginConnection:
  - Использует asyncio.open_connection() для TCP
  - __init__(host, port, crypt: LoginCrypt)
  - async connect()
  - async read_packet() -> tuple[int, bytes]:
    1. Прочитать 2 байта — длина пакета (uint16 LE)
    2. Прочитать (длина - 2) байт — тело пакета
    3. Если это первый пакет (Init) — decrypt_init()
       Иначе — decrypt()
    4. Первый байт тела = opcode, остальное = data
    5. Вернуть (opcode, data)
  - async send_packet(packet: ClientPacket):
    1. data = packet.to_bytes()
    2. encrypted = crypt.encrypt(data)
    3. length = len(encrypted) + 2
    4. Отправить: length (uint16 LE) + encrypted
  - async close()
  - Хранить _is_first_packet: bool для переключения decrypt

Создай src/l2py/network/game_connection.py:

Класс GameConnection:
  - __init__(host, port, crypt: GameCrypt)
  - async connect()
  - async read_packet() -> tuple[int, bytes]:
    1. Прочитать 2 байта — длина
    2. Прочитать тело
    3. Если crypt.enabled — decrypt
    4. Первый байт = opcode
    5. Вернуть (opcode, data)
  - async send_packet(packet: ClientPacket, raw: bool = False):
    1. data = packet.to_bytes()
    2. Если raw (первый пакет) — не шифровать
    3. Иначе — encrypt
    4. Отправить с длиной
  - async close()

Оба класса должны:
- Логировать пакеты через logging (уровень DEBUG: opcode, длина)
- Обрабатывать ConnectionError, asyncio.TimeoutError
- Поддерживать context manager (async with)
- Использовать asyncio.wait_for с таймаутом 10 сек на чтение

Напиши unit-тесты с мок-сокетами (asyncio streams mock).
```

---

### ШАГ 9. Login Flow — оркестрация авторизации

```
Контекст: проект l2py, Python 3.14. Собираем login flow воедино.

Создай src/l2py/network/login_flow.py:

Класс LoginFlow:
  """Оркестрирует полный процесс авторизации на Login Server."""

  - __init__(config: LoginConfig, credentials: Credentials)
  - async execute() -> LoginResult:
    Весь flow Login Server от начала до конца.
    Возвращает LoginResult с данными для подключения к Game Server.

  Внутренний flow:
    1. Создать LoginCrypt и LoginConnection
    2. Подключиться к серверу
    3. Ждать Init пакет (S/0x00):
       - Извлечь session_id, rsa_key, blowfish_key
       - Установить blowfish_key в LoginCrypt
       - Создать L2RSA из rsa_key
    4. Отправить AuthGameGuard (C/0x07) с session_id
    5. Ждать GGAuth (S/0x0b) — проверить response
    6. Отправить RequestAuthLogin (C/0x00) — логин+пароль через RSA
    7. Ждать LoginOk (S/0x03) — получить login_ok1, login_ok2
       Если получен LoginFail (S/0x01) — бросить LoginError
    8. Отправить RequestServerList (C/0x05)
    9. Ждать ServerList (S/0x04) — список серверов
    10. Выбрать сервер по server_id
    11. Отправить RequestServerLogin (C/0x02)
    12. Ждать PlayOk (S/0x07) — получить play_ok1, play_ok2
    13. Закрыть соединение
    14. Вернуть LoginResult

  @dataclass LoginResult:
    server: GameServer (ip, port)
    play_ok1: int
    play_ok2: int
    login_ok1: int
    login_ok2: int
    username: str

  Исключения:
  - LoginError(Exception) — ошибка авторизации с кодом причины
  - ConnectionError — проблемы с сетью

  Создай маппинг LOGIN_FAIL_REASONS:
    0x01: "Account does not exist"
    0x02: "Password is incorrect"
    0x04: "Account is banned"
    0x07: "Account already in use"
    ...

Добавь подробное логирование каждого шага через logging.
```

---

### ШАГ 10. Game Flow — вход в мир

```
Контекст: проект l2py, Python 3.14. Создаём flow входа в Game Server.

Создай src/l2py/network/game_flow.py:

Класс GameFlow:
  """Оркестрирует вход персонажа в игровой мир."""

  - __init__(login_result: LoginResult, char_slot: int = 0)
  - async execute() -> GameSession:
    Весь flow от подключения к Game Server до входа в мир.

  Внутренний flow:
    1. Создать GameCrypt и GameConnection
    2. Подключиться к Game Server (ip:port из login_result)
    3. Отправить ProtocolVersion (C) — НЕ шифруется (raw=True)
    4. Ждать KeyPacket (S/0x2e):
       - Извлечь xor_key
       - Установить ключ в GameCrypt → crypt.enabled = True
    5. Отправить AuthLogin (C/0x2b):
       - username, play_ok1, play_ok2, login_ok1, login_ok2
    6. Ждать CharSelectionInfo (S):
       - Получить список персонажей
       - Выбрать по char_slot
    7. Отправить CharacterSelect (C) — slot_index
    8. Ждать CharSelected (S) — подтверждение
    9. Отправить EnterWorld (C)
    10. Ждать UserInfo (S) — информация о персонаже в мире
    11. Вернуть GameSession

  @dataclass GameSession:
    connection: GameConnection
    character: CharacterInfo
    session_id: int

Важно: после шага 4 ВСЕ пакеты шифруются/дешифруются через GameCrypt.
Первый пакет (ProtocolVersion) отправляется без шифрования.

Логирование: имя персонажа, уровень, координаты при входе.
```

---

### ШАГ 11. Главный фасад — L2Client

```
Контекст: проект l2py, Python 3.14. Создаём главный класс-фасад.

Создай/обнови src/l2py/client.py:

Класс L2Client:
  """Главный фасад для подключения к L2 серверу."""

  - __init__()
  - async enter(
        username: str,
        password: str,
        host: str = "127.0.0.1",
        port: int = 2106,
        server_id: int = 1,
        char_slot: int = 0
    ) -> GameSession:
    """Выполняет полный login flow: авторизация → выбор сервера → вход в мир."""

    Последовательность:
    1. Создать LoginConfig, Credentials, ConnectionConfig
    2. login_result = await LoginFlow(config, creds).execute()
    3. session = await GameFlow(login_result, char_slot).execute()
    4. Вернуть session

  - Logging: при старте логировать username + host:port

Обнови src/l2py/__init__.py:
  from l2py.client import L2Client
  __all__ = ["L2Client"]

Создай examples/login_example.py:

  import asyncio
  from l2py import L2Client

  async def main():
      client = L2Client()
      session = await client.enter(
          username="admin",
          password="admin",
          host="127.0.0.1",
          server_id=1,
          char_slot=0,
      )
      print(f"Вошёл в игру: {session.character.name}, уровень {session.character.level}")
      print(f"Координаты: ({session.character.x}, {session.character.y}, {session.character.z})")

  asyncio.run(main())

Пример должен быть рабочим и понятным.
```

---

### ШАГ 12. Система событий

```
Контекст: проект l2py, Python 3.14. Добавляем типизированную систему событий.

Создай src/l2py/events.py:

Используй dataclass-ы для каждого типа события:

  @dataclass
  class LoggedInEvent:
    character: CharacterInfo
    session: GameSession

  @dataclass
  class PacketReceivedEvent:
    opcode: int
    data: bytes
    source: str  # "login" | "game"

  @dataclass
  class LoginFailedEvent:
    reason: str
    code: int

  @dataclass
  class ServerListEvent:
    servers: list[GameServer]

Класс EventEmitter:
  - Типизированный через Protocol / TypeVar
  - _listeners: dict[type[T], list[Callable[[T], Awaitable[None] | None]]]
  - on(event_type: type[T], callback: Callable[[T], ...]) -> Self
    Поддержка как sync, так и async callback-ов.
  - async emit(event: T):
    Вызывает все зарегистрированные callback-и для type(event).
    Если callback — coroutine, await-ит его.
  - off(event_type, callback) — удалить listener
  - once(event_type, callback) — одноразовый listener

Добавь EventEmitter как mixin в L2Client:
  client = L2Client()
  client.on(LoggedInEvent, lambda e: print(f"Logged in as {e.character.name}"))

Обнови LoginFlow и GameFlow чтобы они принимали и вызывали emitter.
```

---

### ШАГ 13. Интеграционные тесты и финализация

```
Контекст: проект l2py, Python 3.14. Финальный шаг — тесты и polish.

1. Создай tests/test_integration/test_login_flow.py:
   - Мок Login Server через asyncio (простой TCP-сервер):
     - Принимает соединение
     - Отправляет Init с известным ключом
     - Ожидает AuthGameGuard, отвечает GGAuth
     - Ожидает RequestAuthLogin, отвечает LoginOk
     - Ожидает RequestServerList, отвечает ServerList (1 сервер)
     - Ожидает RequestServerLogin, отвечает PlayOk
   - Тест: полный LoginFlow → проверить LoginResult

2. Создай tests/test_integration/test_game_flow.py:
   - Мок Game Server:
     - Ожидает ProtocolVersion, отвечает KeyPacket
     - Ожидает AuthLogin, отвечает CharSelectionInfo (1 персонаж)
     - Ожидает CharacterSelect, отвечает CharSelected
     - Ожидает EnterWorld, отвечает UserInfo
   - Тест: полный GameFlow → проверить GameSession

3. Обнови pyproject.toml: добавь pytest config
   [tool.pytest.ini_options]
   asyncio_mode = "auto"
   testpaths = ["tests"]

4. Создай conftest.py с фикстурами:
   - mock_login_server (фикстура, запускает TCP на свободном порту)
   - mock_game_server
   - sample_credentials

5. Проверь что все __init__.py экспортируют нужные классы.

6. Проверь что все файлы имеют docstrings модуля.

7. Добавь py.typed маркер в src/l2py/py.typed (пустой файл).

8. Финальный README.md:
   - Описание проекта
   - Требования (Python >= 3.14, pycryptodome)
   - Установка
   - Quick start пример
   - Архитектура (ASCII-диаграмма структуры)
   - Статус: Login flow — реализован, Game actions — TODO
```

---

## Порядок проверки после каждого шага

После каждого промта проверяй:

1. **Файлы созданы** в правильных директориях
2. **Type hints** на всех публичных методах
3. **Тесты проходят**: `pytest tests/ -v`
4. **Ruff** не ругается: `ruff check src/`
5. **Импорты работают**: `python -c "from l2py import L2Client"`

## Зависимости от шагов

```
Шаг 1 (структура) ──→ Шаг 2 (PacketBuffer)
                   ├──→ Шаг 3 (Blowfish)
                   ├──→ Шаг 4 (RSA)
                   └──→ Шаг 5 (XOR)
Шаги 2-5 ──→ Шаг 6 (Login Packets)
         ──→ Шаг 7 (Game Packets)
Шаги 6-7 ──→ Шаг 8 (Network)
Шаг 8    ──→ Шаг 9 (Login Flow)
         ──→ Шаг 10 (Game Flow)
Шаги 9-10 ──→ Шаг 11 (L2Client)
          ──→ Шаг 12 (Events)
Все       ──→ Шаг 13 (Тесты + финализация)
```
