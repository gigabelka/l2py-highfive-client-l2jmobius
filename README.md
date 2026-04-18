# l2py — Lineage 2 High Five Client

[![Python 3.14+](https://img.shields.io/badge/python-3.14+-blue.svg)](https://www.python.org/downloads/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)

**l2py** — это asyncio-клиент для Lineage 2 (хроника High Five), совместимый с сервером [L2JMobius](https://github.com/L2JMobius/L2J_Mobius). Проект реализует сетевой протокол L2 для программного управления клиентом.

## Возможности

- ✅ Полный **login flow**: авторизация → выбор сервера → вход в мир
- 🔐 Реализована вся криптография: Blowfish, RSA, XOR
- 📦 Типизированная система пакетов (login + game)
- ⚡ Полностью асинхронный (asyncio)
- 📡 Типизированная система событий
- 🧪 Покрытие тестами

## Установка

# Создайте виртуальное окружение

python -m venv .venv

# Установите проект в режиме разработки

pip install -e ".[dev]"

# Запуск

.venv\Scripts\activate
python main.py

## Быстрый старт

```python
import asyncio
from l2py import L2Client

async def main():
    client = L2Client()
    session = await client.enter(
        username="qwerty",
        password="qwerty",
        host="192.168.0.33",
        port=2106,
        server_id=2,
        char_slot=0,
    )
    print(f"Вошёл в игру: {session.character.name}")
    print(f"Уровень: {session.character.level}")
    print(f"Координаты: ({session.character.x}, {session.character.y}, {session.character.z})")

if __name__ == "__main__":
    asyncio.run(main())
```

## Архитектура

```
l2py/
├── src/l2py/
│   ├── client.py              # Главный фасад L2Client
│   ├── config.py              # Конфигурация (LoginConfig, Credentials)
│   ├── protocol/
│   │   ├── base.py            # PacketReader/PacketWriter
│   │   ├── login/             # Пакеты Login Server
│   │   └── game/              # Пакеты Game Server
│   ├── network/
│   │   ├── login_connection.py
│   │   ├── game_connection.py
│   │   ├── login_flow.py
│   │   └── game_flow.py
│   ├── crypto/
│   │   ├── blowfish.py
│   │   ├── login_crypt.py
│   │   ├── game_crypt.py
│   │   └── rsa.py
│   ├── models/
│   │   ├── server.py
│   │   └── character.py
│   └── events.py              # Система событий
```

## Статус разработки

- ✅ **Login flow** — полностью реализован

## Лицензия

MIT License — см. файл [LICENSE](LICENSE) для подробностей.

## Благодарности

- Совместим с [L2JMobius](https://github.com/L2JMobius/L2J_Mobius)

# Документация l2py

Техническая документация по протоколу Lineage 2 HighFive (L2J Mobius CT 2.6) и клиентской реализации l2py. Документы извлечены из исторического [SPECIFICATION.md](../SPECIFICATION.md) и разделены по темам.

## Оглавление

- [PROTOCOL.md](docs/PROTOCOL.md) — wire-протокол клиент ↔ сервер: общий обзор, примитивы (endianness, типы, framing), Login Server (state machine, все S→C и C→S пакеты, annotated hex dumps) и Game Server (handshake, keepalive, gameplay-пакеты).
- [CRYPTOGRAPHY.md](docs/CRYPTOGRAPHY.md) — криптография: Blowfish (login phase), NewCrypt XOR checksum и rolling XOR (Init), RSA-1024 (`RSA_NO_PADDING`) с unscramble модуса, ключи Blowfish, пайплайны шифрования login-пакетов, XOR stream cipher game-канала, тест-векторы.
- [AUTOLOGIN.md](docs/AUTOLOGIN.md) — алгоритм автоматического входа персонажа в игру: sequence diagram, детальный псевдокод всех трёх фаз (Login Server, Game Server, in-game), требуемые конфигурационные параметры, cross-reference с реальными размерами пакетов, обработка ошибок.
- [CHECKLIST.md](docs/CHECKLIST.md) — чеклист реализации клиента: что нужно реализовать при портировании на новый язык.
- [CONSTANTS.md](docs/CONSTANTS.md) — справочник констант: магические значения, LoginFail / PlayFail reason-коды, RequestSocialAction action-ids, дублирующиеся опкоды.
- [SKILLS.md](docs/SKILLS.md) — скилы всех игровых классов (1st/2nd/3rd): id, название, макс. уровень, уровень изучения, суммарный SP. Генерируется из XML сервера L2JMobius скриптом [scripts/gen_skills_doc.py](scripts/gen_skills_doc.py).
- [INVENTORY.md](docs/INVENTORY.md) — спецификация инвентаря персонажа (только личные предметы: оружие, броня, аксессуары, adena): 25 paperdoll-слотов, body-part битмаски, таксономии WeaponType/ArmorType/CrystalType, правила экипировки по классам, on-wire формат item record, узкий набор пакетов (`ItemList`, `InventoryUpdate`, `ExStorageMaxCount`, `UseItem`, `RequestUnEquipItem`, `RequestDropItem`, `RequestDestroyItem`).
- [RACES_CLASSES.md](docs/RACES_CLASSES.md) — расы и полное дерево `classId` (103 класса), гейты смены профессии (L20/40/76), базовые статы и кривые роста HP/MP/CP, стартовый инвентарь на root-класс, XP-вехи, лимиты слотов. Генерируется из XML сервера и `PlayerClass.java` скриптом [scripts/gen_races_classes_doc.py](scripts/gen_races_classes_doc.py).
- [ITEMS.md](docs/ITEMS.md) — каталог всех предметов, которые могут попасть в инвентарь (оружие, броня, щиты/сигилы, украшения, пояс, хэир, adena). Сгруппировано по weapon type / body slot / armor type / crystal grade; id, имя, вес и ключевые статы. Генерируется скриптом [scripts/gen_items_doc.py](scripts/gen_items_doc.py).
- [MOBS.md](docs/MOBS.md) — каталог боевых NPC (монстры, raid/grand-боссы, сундуки, festival/rift invaders, звери, стражи/защитники/fort commanders, quest guards, decoys, дружественные мобы). Поля: id, имя, уровень, раса, HP, pAtk/mAtk, pDef/mDef, радиус атаки, exp/sp, aggro radius, число скиллов и drop/spoil-записей; приложение с полными drop + spoil таблицами для RaidBoss/GrandBoss. Генерируется скриптом [scripts/gen_mobs_doc.py](scripts/gen_mobs_doc.py).
