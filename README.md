# l2py — Lineage 2 High Five Client

[![Python 3.14+](https://img.shields.io/badge/python-3.14+-blue.svg)](https://www.python.org/downloads/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)

**l2py** — asyncio-клиент для Lineage 2 (хроника High Five, CT 2.6), совместимый с сервером [L2JMobius](https://github.com/L2JMobius/L2J_Mobius). Реализует сетевой протокол L2 (login + game) для программного управления клиентом и предоставляет внешний HTTP/WebSocket API поверх активной игровой сессии.

## Возможности

- ✅ Полный **login flow**: авторизация → выбор сервера → вход в мир
- ✅ **Game flow**: handshake, CharacterSelected → EnterWorld, keepalive
- 🔐 Вся криптография: Blowfish (login), NewCrypt XOR, RSA-1024, XOR stream (game)
- 📦 Типизированная система пакетов (login + game)
- ⚡ Полностью асинхронный (asyncio, Python 3.14+)
- 📡 Типизированная шина событий (`events.py`)
- 🌐 Встроенный HTTP + WebSocket API (FastAPI + uvicorn)
- 🧪 Покрытие тестами (pytest, `asyncio_mode = "auto"`)

## Требования

- Python **3.14+**
- Сервер L2JMobius (CT 2.6) или совместимая сборка High Five

## Установка

```bash
# Создать виртуальное окружение
python -m venv .venv

# Активировать (Windows)
.venv\Scripts\activate
# Активировать (Linux / macOS)
source .venv/bin/activate

# Установить в режиме разработки (с dev-зависимостями)
pip install -e ".[dev]"
```

## Запуск

```bash
python main.py
```

Параметры подключения и учётные данные сейчас заданы прямо в [main.py](main.py) — отредактируйте `username`, `password`, `host`, `port`, `server_id`, `char_slot` под свой сервер.

Хост/порт внешнего API переопределяются переменными окружения:

```bash
L2PY_API_HOST=0.0.0.0 L2PY_API_PORT=8080 python main.py
```

## Тесты и линт

```bash
pytest                                      # полный прогон
pytest tests/test_crypto                    # одна директория
pytest -k "blowfish"                        # фильтр по имени

ruff check .
ruff format .
```

## Быстрый старт

См. [docs/EXAMPLES.md](docs/EXAMPLES.md) — примеры использования клиента и HTTP/WebSocket API.

## Внешний API (HTTP + WebSocket)

При запуске `python main.py` вместе с игровой сессией поднимается FastAPI-сервер на `127.0.0.1:8000` (переопределяется `L2PY_API_HOST` / `L2PY_API_PORT`). Swagger UI — на `/docs`, стрим входящих пакетов — на `ws://.../ws/packets`.

Полный список эндпоинтов, форматы запросов/ответов и ограничения MVP — в [docs/API.md](docs/API.md). Примеры вызовов — в [docs/EXAMPLES.md](docs/EXAMPLES.md).

## Архитектура

```
l2py/
├── src/l2py/
│   ├── client.py              # Главный фасад L2Client (enter())
│   ├── config.py              # Конфигурация (LoginConfig, Credentials)
│   ├── events.py              # Типизированная шина событий
│   ├── protocol/
│   │   ├── base.py            # PacketReader / PacketWriter, ClientPacket / ServerPacket
│   │   ├── login/             # Пакеты Login Server
│   │   └── game/              # Пакеты Game Server
│   ├── network/
│   │   ├── login_connection.py
│   │   ├── game_connection.py
│   │   ├── login_flow.py      # Фаза 1: Init → GGAuth → AuthLogin → ServerList → PlayOk
│   │   └── game_flow.py       # Фаза 2: ProtocolVersion → CryptInit → AuthRequest → EnterWorld
│   ├── crypto/
│   │   ├── blowfish.py        # Blowfish ECB (login)
│   │   ├── login_crypt.py     # Padding + NewCrypt XOR + Blowfish
│   │   ├── game_crypt.py      # XOR stream cipher (game)
│   │   └── rsa.py             # RSA-1024 + unscramble модуса
│   ├── models/
│   │   ├── server.py
│   │   └── character.py
│   ├── api/                   # Внешний HTTP/WS API (FastAPI + uvicorn)
│   │   ├── server.py          # ApiServer, create_app
│   │   ├── routes.py          # HTTP-эндпоинты действий
│   │   ├── ws.py              # WebSocket-стрим пакетов
│   │   ├── schemas.py         # Pydantic-схемы запросов/ответов
│   │   └── state.py           # Shared runtime state (emitter, позиция, таргет)
│   └── debug/                 # Вспомогательные дампы и трассировка
├── docs/                      # Протокол, криптография, каталоги игровых данных
├── scripts/                   # Генераторы docs/ из исходников L2JMobius
└── tests/                     # test_crypto, test_protocol, test_integration
```

## Статус разработки

- ✅ **Login flow** — реализован
- ✅ **Game flow** — handshake, вход в мир, keepalive
- ✅ **HTTP / WS API** — MVP (status, sit/stand, attack, pick-up, target, F1–F12, packet stream)
- 🚧 Боевые сценарии высокого уровня, автоматический shortcut bar, цепочки действий — в работе

## Документация

Техническая документация по протоколу Lineage 2 HighFive (L2JMobius CT 2.6) и клиентской реализации l2py.

- [PROTOCOL.md](docs/PROTOCOL.md) — wire-протокол клиент ↔ сервер: общий обзор, примитивы (endianness, типы, framing), Login Server (state machine, все S→C и C→S пакеты, annotated hex dumps) и Game Server (handshake, keepalive, gameplay-пакеты).
- [CRYPTOGRAPHY.md](docs/CRYPTOGRAPHY.md) — криптография: Blowfish (login), NewCrypt XOR checksum и rolling XOR (Init), RSA-1024 (`RSA_NO_PADDING`) с unscramble модуса, ключи Blowfish, пайплайны шифрования, XOR stream game-канала, тест-векторы.
- [AUTOLOGIN.md](docs/AUTOLOGIN.md) — алгоритм автоматического входа персонажа: sequence diagram, детальный псевдокод всех трёх фаз (Login, Game, in-game), конфигурационные параметры, обработка ошибок.
- [CHECKLIST.md](docs/CHECKLIST.md) — чеклист реализации клиента: что нужно реализовать при портировании на новый язык.
- [CONSTANTS.md](docs/CONSTANTS.md) — справочник констант: магические значения, LoginFail / PlayFail reason-коды, RequestSocialAction action-ids, дублирующиеся опкоды.
- [API.md](docs/API.md) — внешний HTTP + WebSocket API: эндпоинты (`/api/status`, действия, F1–F12), WebSocket-стрим пакетов, ограничения MVP.
- [EXAMPLES.md](docs/EXAMPLES.md) — примеры использования клиента и HTTP/WebSocket API.
- [ACTIONS.md](docs/ACTIONS.md) — in-game действия: таргет (`Action 0x1F`), атака (`AttackRequest 0x32`), скил (`RequestMagicSkillUse 0x39`), предмет (`UseItem 0x19`), drop, bypass, target cancel, shortcuts, каталог action-id для `RequestActionUse 0x56`, F1–F12. Генерируется [scripts/gen_actions_doc.py](scripts/gen_actions_doc.py).
- [SKILLS.md](docs/SKILLS.md) — скилы всех классов (1st/2nd/3rd): id, название, макс. уровень, уровень изучения, суммарный SP. Генерируется [scripts/gen_skills_doc.py](scripts/gen_skills_doc.py).
- [INVENTORY.md](docs/INVENTORY.md) — спецификация инвентаря (оружие, броня, аксессуары, adena): 25 paperdoll-слотов, body-part битмаски, таксономии WeaponType/ArmorType/CrystalType, правила экипировки, on-wire формат item record, узкий набор пакетов (`ItemList`, `InventoryUpdate`, `ExStorageMaxCount`, `UseItem`, `RequestUnEquipItem`, `RequestDropItem`, `RequestDestroyItem`).
- [RACES_CLASSES.md](docs/RACES_CLASSES.md) — расы и полное дерево `classId` (103 класса), гейты смены профессии (L20/40/76), базовые статы и кривые роста HP/MP/CP, стартовый инвентарь, XP-вехи, лимиты слотов. Генерируется [scripts/gen_races_classes_doc.py](scripts/gen_races_classes_doc.py).
- [ITEMS.md](docs/ITEMS.md) — каталог всех предметов, которые могут попасть в инвентарь. Сгруппировано по weapon type / body slot / armor type / crystal grade; id, имя, вес, ключевые статы. Генерируется [scripts/gen_items_doc.py](scripts/gen_items_doc.py).
- [MOBS.md](docs/MOBS.md) — каталог боевых NPC (монстры, raid/grand-боссы, сундуки, festival/rift invaders, звери, стражи, quest guards, decoys, дружественные мобы): id, имя, уровень, раса, HP, pAtk/mAtk, pDef/mDef, радиус атаки, exp/sp, aggro radius, скиллы, drop/spoil; приложение с полными drop + spoil таблицами RaidBoss/GrandBoss. Генерируется [scripts/gen_mobs_doc.py](scripts/gen_mobs_doc.py).

## Лицензия

MIT License — см. файл [LICENSE](LICENSE).

## Благодарности

- Совместим с [L2JMobius](https://github.com/L2JMobius/L2J_Mobius)
