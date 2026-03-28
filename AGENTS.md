# AGENTS.md — l2py Project Guide

> This file contains essential information for AI coding agents working on the l2py project.
> Все комментарии и документация в проекте написаны на русском языке.

## Project Overview

**l2py** — это asyncio-клиент для Lineage 2 High Five, совместимый с сервером [L2JMobius](https://github.com/L2JMobius/L2J_Mobius). Проект реализует сетевой протокол L2 для программного управления клиентом.

### Key Features
- Полный **login flow**: авторизация → выбор сервера → вход в мир
- Реализована криптография: Blowfish, RSA, XOR
- Типизированная система пакетов (login + game)
- Полностью асинхронный (asyncio)
- Типизированная система событий
- Покрытие тестами

## Technology Stack

- **Language**: Python 3.14+
- **Build System**: Hatchling
- **Dependencies**:
  - `pycryptodome >= 3.20` — криптография
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
│   │   ├── blowfish.py          # Blowfish шифрование
│   │   ├── login_crypt.py       # Шифрование для Login Server
│   │   ├── game_crypt.py        # Шифрование для Game Server
│   │   └── rsa.py               # RSA шифрование
│   ├── models/                  # Модели данных
│   │   ├── character.py         # CharacterInfo
│   │   └── server.py            # GameServer
│   ├── network/                 # Сетевой слой
│   │   ├── login_connection.py  # Соединение с Login Server
│   │   ├── game_connection.py   # Соединение с Game Server
│   │   ├── login_flow.py        # Оркестрация авторизации
│   │   └── game_flow.py         # Оркестрация входа в мир
│   └── protocol/                # Протокол L2
│       ├── base.py              # PacketReader/PacketWriter, базовые классы пакетов
│       ├── login/               # Пакеты Login Server
│       │   ├── client_packets.py
│       │   └── server_packets.py
│       └── game/                # Пакеты Game Server
│           ├── client_packets.py
│           └── server_packets.py
├── tests/                       # Тесты
│   ├── conftest.py              # Фикстуры pytest (mock-серверы)
│   ├── test_crypto/             # Тесты криптографии
│   ├── test_protocol/           # Тесты протокола
│   └── test_integration/        # Интеграционные тесты
├── examples/                    # Примеры использования
│   └── login_example.py
├── pyproject.toml               # Конфигурация проекта
└── README.md                    # Документация для пользователей
```

## Build and Test Commands

### Installation
```bash
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

### Build
```bash
# Сборка wheel
python -m build
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
- `sample_credentials` — Тестовые учётные данные
- `sample_login_config` — Тестовая конфигурация
- `mock_login_server` — Mock Login Server на случайном порту
- `mock_game_server` — Mock Game Server на случайном порту

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
- `ClientPacket` — пакеты от клиента к серверу
- `ServerPacket` — пакеты от сервера к клиенту

### Flow Pattern
Оркестрация сложных процессов через Flow-классы:
- `LoginFlow` — авторизация на Login Server
- `GameFlow` — вход в игровой мир

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

## Security Considerations

### Криптография
- `L2Blowfish` — блочное шифрование (8-байтные блоки)
- `L2RSA` — асимметричное шифрование для авторизации
- `LoginCrypt` — Blowfish + XOR + checksum для Login Server
- `GameCrypt` — XOR шифрование для Game Server

### Важные замечания
- RSA-ключи могут требовать дескремблирования (`unscramble_modulus`)
- Статические ключи определены в соответствующих модулях криптографии
- Первый пакет (Init) шифруется иначе, чем последующие

## Development Status

- ✅ **Login flow** — полностью реализован
- 🚧 **Game actions** — в разработке (move, attack, skills)

## Common Tasks

### Добавление нового пакета
1. Определи опкод пакета
2. Создай класс в `protocol/login/` или `protocol/game/`
3. Унаследуй от `ClientPacket` или `ServerPacket`
4. Реализуй `_write()` или `_read()` метод
5. Добавь тесты

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
