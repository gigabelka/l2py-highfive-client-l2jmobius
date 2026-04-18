
"""l2py — asyncio-клиент для Lineage 2 High Five (L2JMobius).

Проект реализует полный login flow:
- Подключение к Login Server (порт 2106)
- Авторизация с RSA-шифрованием
- Выбор сервера из списка
- Подключение к Game Server
- Выбор персонажа и вход в мир

Пример использования:
    import asyncio
    from l2py import L2Client

    async def main():
        client = L2Client()
        session = await client.enter(
            username="qwerty",
            password="qwerty",
            host="192.168.0.33",
        )
        print(f"Вошёл как: {session.character.name}")

    asyncio.run(main())
"""

from l2py.client import L2Client
from l2py.config import ConnectionConfig, Credentials, LoginConfig
from l2py.crypto import GameCrypt, L2Blowfish, L2RSA, LoginCrypt, unscramble_modulus
from l2py.events import (
    EventEmitter,
    EventMixin,
    LoggedInEvent,
    LoginFailedEvent,
    PacketReceivedEvent,
    ServerListEvent,
)
from l2py.models import CharacterInfo, GameServer
from l2py.network import GameConnection, LoginConnection
from l2py.network.game_flow import GameError, GameFlow, GameSession
from l2py.network.login_flow import LOGIN_FAIL_REASONS, LoginError, LoginFlow, LoginResult
from l2py.protocol import ClientPacket, PacketReader, PacketWriter, ServerPacket

__version__ = "0.1.0"

__all__ = [

    "L2Client",

    "LoginConfig",
    "Credentials",
    "ConnectionConfig",

    "L2Blowfish",
    "LoginCrypt",
    "GameCrypt",
    "L2RSA",
    "unscramble_modulus",

    "LoginConnection",
    "GameConnection",
    "LoginFlow",
    "LoginResult",
    "LoginError",
    "LOGIN_FAIL_REASONS",
    "GameFlow",
    "GameSession",
    "GameError",

    "PacketReader",
    "PacketWriter",
    "ServerPacket",
    "ClientPacket",

    "GameServer",
    "CharacterInfo",

    "EventEmitter",
    "EventMixin",
    "LoggedInEvent",
    "PacketReceivedEvent",
    "LoginFailedEvent",
    "ServerListEvent",
]
