# AGENTS.md — l2py Project Guide

> This file contains essential information for AI coding agents working on the l2py project.
> Все комментарии и документация в проекте написаны на русском языке.

## Project Overview

**l2py** — это asyncio-клиент для Lineage 2 High Five, совместимый с сервером [L2JMobius](https://github.com/L2JMobius/L2J_Mobius). Проект реализует сетевой протокол L2 для программного управления клиентом.

### Key Features

- Полный **login flow**: авторизация → выбор сервера → вход в мир
- Реализована криптография: Blowfish (ECB, 8-байтные блоки), RSA (textbook, без padding), XOR
- Типизированная система пакетов (login + game)
- Полностью асинхронный (asyncio)
- Типизированная система событий с поддержкой sync/async обработчиков
- Покрытие тестами с mock-серверами

## Technology Stack

- **Language**: Python 3.14+
- **Build System**: Hatchling
- **Dependencies**:
  - `pycryptodome >= 3.20` — криптография (используется частично)
- **Dev Dependencies**:
  - `pytest >= 8.0` — тестирование
  - `pytest-asyncio >= 0.23` — async тесты
  - `ruff >= 0.4.0` — линтинг и форматирование

## Project Structure

```
l2py/
├── src/l2py/                    # Основной код
│   ├── __init__.py              # Публичный API
│   ├── client.py                # Главный фасад L2Client
│   ├── config.py                # Конфигурация (LoginConfig, Credentials, ConnectionConfig)
│   ├── events.py                # Типизированная система событий
│   ├── crypto/                  # Криптографические модули
│   │   ├── blowfish.py          # Blowfish шифрование (ECB, 8-байтные блоки)
│   │   ├── blowfish_engine.py   # Движок Blowfish (порт из L2JMobius)
│   │   ├── login_crypt.py       # Шифрование для Login Server (Blowfish + XOR + checksum)
│   │   ├── game_crypt.py        # Шифрование для Game Server (XOR)
│   │   └── rsa.py               # RSA шифрование с авто-дескремблированием для L2JMobius
│   ├── models/                  # Модели данных
│   │   ├── character.py         # CharacterInfo (frozen dataclass)
│   │   └── server.py            # GameServer (frozen dataclass)
│   ├── network/                 # Сетевой слой
│   │   ├── login_connection.py  # Соединение с Login Server
│   │   ├── game_connection.py   # Соединение с Game Server
│   │   ├── login_flow.py        # Оркестрация авторизации (LoginFlow, LoginResult, LoginError)
│   │   └── game_flow.py         # Оркестрация входа в мир (GameFlow, GameSession, GameError)
│   ├── protocol/                # Протокол L2
│   │   ├── base.py              # PacketReader/PacketWriter, базовые классы пакетов
│   │   ├── login/               # Пакеты Login Server
│   │   │   ├── client_packets.py # AuthGameGuardPacket, RequestAuthLoginPacket, RequestServerListPacket, RequestServerLoginPacket
│   │   │   └── server_packets.py # InitPacket, GGAuthPacket, LoginOkPacket, LoginFailPacket, ServerListPacket, PlayOkPacket
│   │   └── game/                # Пакеты Game Server
│   │       ├── client_packets.py # ProtocolVersionPacket, AuthLoginPacket, CharacterSelectPacket, EnterWorldPacket
│   │       └── server_packets.py # KeyPacket, CharSelectionInfoPacket, CharSelectedPacket, UserInfoPacket
│   └── debug/                   # Отладочные утилиты
│       └── packet_inspector.py  # Анализ пакетов, hex dump, диагностика
├── tests/                       # Тесты
│   ├── conftest.py              # Фикстуры pytest (mock-серверы, credentials)
│   ├── test_crypto/             # Тесты криптографии
│   ├── test_protocol/           # Тесты сериализации/десериализации пакетов
│   └── test_integration/        # Интеграционные тесты с mock-серверами
├── main.py                      # Точка входа (пример использования)
├── pyproject.toml               # Конфигурация проекта
└── README.md                    # Документация для пользователей
```

## Build and Test Commands

### Installation

```bash
# Создание виртуального окружения
python -m venv .venv

# Активация (Windows)
.venv\Scripts\activate

# Установка в режиме разработки
pip install -e ".[dev]"
```

### Testing

```bash
# Запуск всех тестов
pytest

# Запуск с подробным выводом
pytest -v

# Запуск конкретного модуля
pytest tests/test_crypto/
```

### Linting and Formatting

```bash
# Проверка кода линтером
ruff check .

# Автоисправление ошибок
ruff check . --fix

# Форматирование
ruff format .
```

### Running

```bash
# Активация окружения и запуск
.venv\Scripts\activate
python main.py
```

## Code Style Guidelines

### General

- **Line length**: 99 символов (настраивается в `pyproject.toml`)
- **Encoding**: UTF-8 (всегда указывай `# -*- coding: utf-8 -*-` в начале файла)
- **Type hints**: Обязательны для всех публичных функций и методов
- **Docstrings**: Google convention, на русском языке

### Naming Conventions

- `CamelCase` для классов
- `snake_case` для функций, методов, переменных
- `UPPER_CASE` для констант
- `_private` для внутренних методов/переменных

### Memory Efficiency

Все классы используют `__slots__` для экономии памяти:

```python
class MyClass:
    __slots__ = ("field1", "field2")

    def __init__(self, field1, field2):
        self.field1 = field1
        self.field2 = field2
```

### Dataclasses

Используются `frozen=True, slots=True` для неизменяемых конфигурационных объектов:

```python
@dataclass(frozen=True, slots=True)
class LoginConfig:
    host: str
    port: int = 2106
```

### Imports

```python
# Стандартная структура импортов
from __future__ import annotations  # Для отложенных аннотаций типов

import asyncio
from dataclasses import dataclass
from typing import ClassVar, Generic, TypeVar

# Сторонние библиотеки
import pytest

# Внутренние модули
from l2py.crypto.blowfish import L2Blowfish
```

### Class Structure

```python
class ServerPacket(ABC):
    """Базовый класс для пакетов от сервера.

    Attributes:
        opcode: Опкод пакета (должен быть переопределён).
    """

    opcode: ClassVar[int] = 0x00
    __slots__ = ("_reader",)

    def __init__(self, data: bytes) -> None:
        """Инициализирует и парсит пакет.

        Args:
            data: Байты пакета (без опкода).
        """
        self._reader = PacketReader(data)
        self._read()

    @abstractmethod
    def _read(self) -> None:
        """Абстрактный метод для парсинга полей."""
        raise NotImplementedError
```

## Testing Instructions

### Test Organization

- `tests/test_crypto/` — Тесты криптографических модулей
- `tests/test_protocol/` — Тесты сериализации/десериализации пакетов
- `tests/test_integration/` — Интеграционные тесты с mock-серверами

### Fixtures (conftest.py)

- `sample_credentials` — Тестовые учётные данные (testuser/testpass)
- `sample_login_config` — Тестовая конфигурация
- `login_crypt` — Настроенная криптография с тестовым ключом
- `mock_login_server` — Mock Login Server на свободном порту (192.168.0.33)
- `mock_game_server` — Mock Game Server на свободном порту (192.168.0.33)

### Writing Tests

```python
class TestMyFeature:
    """Тесты для новой функциональности."""

    def test_basic_functionality(self):
        """Тест базовой функциональности."""
        result = my_function()
        assert result == expected

    async def test_async_functionality(self):
        """Тест async функциональности."""
        result = await my_async_function()
        assert result == expected
```

### Async Testing

- Используй `pytest-asyncio` (уже настроен в `pyproject.toml`)
- `asyncio_mode = "auto"` — автоматическое обнаружение async тестов

## Architecture Patterns

### Packet System

Все пакеты наследуются от базовых классов:

- `ClientPacket` — пакеты от клиента к серверу (реализуют `_write()`)
- `ServerPacket` — пакеты от сервера к клиенту (реализуют `_read()`)

### Flow Pattern

Оркестрация сложных процессов через Flow-классы:

- `LoginFlow` — авторизация на Login Server (LoginResult, LoginError)
- `GameFlow` — вход в игровой мир (GameSession, GameError)

### Event System

Типизированная система событий с поддержкой sync/async обработчиков:

```python
emitter = EventEmitter()
emitter.on(LoggedInEvent, lambda e: print(f"Logged in as {e.character.name}"))
await emitter.emit(LoggedInEvent(character=..., session=...))
```

### Connection Pattern

Асинхронные соединения с контекстными менеджерами:

```python
async with LoginConnection(host, port, crypt) as conn:
    opcode, data = await conn.read_packet()
    await conn.send_packet(packet)
```

### Debug Utilities

PacketInspector для диагностики проблем с пакетами:

```python
inspector = create_inspector(debug_packets=True)
analysis = inspector.analyze_packet(raw_data, decrypted_data, expected_opcode, "login")
inspector.log_packet_analysis(analysis, "context")
```

## Security Considerations

### Криптография

- `L2Blowfish` — блочное шифрование (8-байтные блоки, ECB режим), использует BlowfishEngine портированный из L2JMobius
- `L2RSA` — асимметричное шифрование для авторизации с авто-дескремблированием (L2JMobius scramble алгоритм)
- `LoginCrypt` — Blowfish + XOR + checksum для Login Server
- `GameCrypt` — XOR шифрование для Game Server (динамический ключ + статический STATIC_KEY)

### Важные замечания

- RSA-ключи требуют дескремблирования (`unscramble_modulus`) для L2JMobius (4 шага: XOR + swap)
- Статические ключи определены в `login_crypt.py` (STATIC_BLOWFISH_KEY, AVAILABLE_KEYS)
- Первый пакет (Init) шифруется иначе, чем последующие (через `decrypt_init` с XOR pass)
- Реализован авто-детект статического Blowfish-ключа при несоответствии опкода

## Login Flow Sequence

```
1. Подключение к Login Server (порт 2106)
2. Получение Init (session_id, rsa_key, blowfish_key)
3. Отправка AuthGameGuard
4. Получение GGAuth
5. Отправка RequestAuthLogin (RSA-шифрование)
6. Получение LoginOk (login_ok1, login_ok2)
7. Отправка RequestServerList
8. Получение ServerList
9. Отправка RequestServerLogin
10. Получение PlayOk (play_ok1, play_ok2)
11. Переподключение к Game Server
12. ProtocolVersion → KeyPacket → AuthLogin
13. CharSelectionInfo → CharacterSelect → CharSelected
14. EnterWorld → UserInfo (в игре!)
```

## Development Status

- ✅ **Login flow** — полностью реализован
- ✅ **Game flow** — полностью реализован (вход в мир с персонажем)
- 🚧 **Game actions** — в разработке (move, attack, skills)

## Common Tasks

### Добавление нового пакета

1. Определи опкод пакета
2. Создай класс в `protocol/login/` или `protocol/game/`
3. Унаследуй от `ClientPacket` (для исходящих) или `ServerPacket` (для входящих)
4. Реализуй `_write()` или `_read()` метод
5. Добавь в `__all__` модуля
6. Добавь тесты

### Добавление нового события

1. Создай dataclass в `events.py`
2. Добавь в `__all__` и публичный API в `__init__.py`

### Работа с тестами

- Mock-серверы запускаются на `192.168.0.33` со случайным портом
- Используй `asyncio.wait_for()` для таймаутов в тестах
- Криптография в тестах использует тестовые ключи

## External Resources

- **L2JMobius**: https://github.com/L2JMobius/L2J_Mobius
- **Python 3.14**: https://www.python.org/downloads/
