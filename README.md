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

```bash
pip install l2py
```

Или из исходников:

```bash
git clone https://github.com/l2py/l2py-highfive-client.git
cd l2py-highfive-client
pip install -e ".[dev]"
```

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
        server_id=1,
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
- 🚧 **Game actions** — в разработке (move, attack, skills)

## Лицензия

MIT License — см. файл [LICENSE](LICENSE) для подробностей.

## Благодарности

- Проект основан на архитектуре [l2js-client](https://github.com/npetrovski/l2js-client)
- Совместим с [L2JMobius](https://github.com/L2JMobius/L2J_Mobius)
