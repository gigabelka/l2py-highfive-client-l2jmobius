# -*- coding: utf-8 -*-
"""Интеграционные тесты для Game Flow.

Тестируют полный процесс входа в мир на мок Game Server.
"""

import asyncio
import struct

import pytest

from l2py.crypto.game_crypt import GameCrypt
from l2py.models.character import CharacterInfo
from l2py.models.server import GameServer
from l2py.network.game_connection import GameConnection
from l2py.network.game_flow import GameError, GameFlow
from l2py.network.login_flow import LoginResult
from l2py.protocol.game.client_packets import (
    AuthLoginPacket,
    CharacterSelectPacket,
    EnterWorldPacket,
    ProtocolVersionPacket,
)
from l2py.protocol.game.server_packets import (
    CharSelectedPacket,
    CharSelectionInfoPacket,
    KeyPacket,
    UserInfoPacket,
)


class MockGameServer:
    """Мок Game Server для тестирования."""

    def __init__(self, host: str = "127.0.0.1", port: int = 0):
        self.host = host
        self.port = port
        self.server = None
        self.xor_key = b"xorkey12"
        self.crypt = GameCrypt()

    async def start(self):
        """Запускает мок-сервер."""
        self.server = await asyncio.start_server(
            self._handle_client, self.host, self.port
        )
        addr = self.server.sockets[0].getsockname()
        self.host = addr[0]
        self.port = addr[1]

    async def stop(self):
        """Останавливает мок-сервер."""
        if self.server:
            self.server.close()
            await self.server.wait_closed()

    async def _handle_client(self, reader, writer):
        """Обрабатывает клиентское соединение."""
        # Читаем ProtocolVersion (не шифруется)
        length_bytes = await reader.readexactly(2)
        length = int.from_bytes(length_bytes, "little")
        await reader.readexactly(length - 2)

        # Отправляем KeyPacket (не шифруется)
        key_packet = bytes([0x2E, 0x01]) + self.xor_key
        key_packet += struct.pack("<I", 1)  # server_id
        key_packet += struct.pack("<I", 0)  # obfuscation_key

        writer.write((len(key_packet) + 2).to_bytes(2, "little") + key_packet)
        await writer.drain()

        # Включаем шифрование
        self.crypt.set_key(self.xor_key)

        # Обрабатываем остальные пакеты
        try:
            while True:
                try:
                    opcode, data = await self._read_packet(reader)
                except (asyncio.TimeoutError, asyncio.IncompleteReadError):
                    break

                if opcode == 0x2B:  # AuthLogin
                    await self._send_char_selection_info(writer)

                elif opcode == 0x0D:  # CharacterSelect
                    await self._send_char_selected(writer)

                elif opcode == 0x11:  # EnterWorld
                    await self._send_user_info(writer)
                    break

        finally:
            writer.close()
            await writer.wait_closed()

    async def _send_char_selection_info(self, writer):
        """Отправляет CharSelectionInfo."""
        # Упрощённая структура пакета
        response = bytes([0x13, 0x01])  # opcode, count=1
        response += b"T\x00e\x00s\x00t\x00\x00\x00"  # name = "Test"
        response += b"u\x00s\x00e\x00r\x00\x00\x00"  # login = "user"
        response += struct.pack("<I", 12345)  # session_id
        response += struct.pack("<I", 0)  # clan_id
        response += struct.pack("<I", 0)  # constructType
        response += struct.pack("<I", 0)  # sex
        response += struct.pack("<I", 0)  # race
        response += struct.pack("<I", 0)  # class_id
        response += bytes([1])  # active
        response += struct.pack("<I", 100)  # x
        response += struct.pack("<I", 200)  # y
        response += struct.pack("<I", 300)  # z
        response += struct.pack("<f", 100.0)  # hp
        response += struct.pack("<f", 100.0)  # mp
        response += struct.pack("<I", 0)  # sp
        response += struct.pack("<Q", 0)  # exp
        response += struct.pack("<I", 1)  # level

        encrypted = self.crypt.encrypt(response)
        length = len(encrypted) + 2
        writer.write(length.to_bytes(2, "little") + encrypted)
        await writer.drain()

    async def _send_char_selected(self, writer):
        """Отправляет CharSelected."""
        response = bytes([0x15])
        response += b"T\x00e\x00s\x00t\x00\x00\x00"  # name
        response += struct.pack("<I", 12345)  # session_id
        response += struct.pack("<I", 0)  # clan_id
        response += struct.pack("<I", 0)  # unknown
        response += struct.pack("<I", 0)  # sex
        response += struct.pack("<I", 0)  # race
        response += struct.pack("<I", 0)  # class_id
        response += struct.pack("<I", 0)  # active
        response += struct.pack("<I", 100)  # x
        response += struct.pack("<I", 200)  # y
        response += struct.pack("<I", 300)  # z

        encrypted = self.crypt.encrypt(response)
        length = len(encrypted) + 2
        writer.write(length.to_bytes(2, "little") + encrypted)
        await writer.drain()

    async def _send_user_info(self, writer):
        """Отправляет UserInfo."""
        # Упрощённая версия
        response = bytes([0x32])
        response += b"T\x00e\x00s\x00t\x00\x00\x00"  # name

        encrypted = self.crypt.encrypt(response)
        length = len(encrypted) + 2
        writer.write(length.to_bytes(2, "little") + encrypted)
        await writer.drain()

    async def _read_packet(self, reader) -> tuple[int, bytes]:
        """Читает пакет от клиента."""
        length_bytes = await reader.readexactly(2)
        length = int.from_bytes(length_bytes, "little")

        body = await reader.readexactly(length - 2)
        decrypted = self.crypt.decrypt(body)

        return decrypted[0], decrypted[1:]


@pytest.fixture
async def mock_game_server():
    """Фикстура с мок Game Server."""
    server = MockGameServer()
    await server.start()
    yield server
    await server.stop()


@pytest.mark.asyncio
async def test_full_game_flow(mock_game_server):
    """Тест полного game flow."""
    login_result = LoginResult(
        server=GameServer(
            id=1,
            ip=mock_game_server.host,
            port=mock_game_server.port,
            online=100,
            max_online=400,
        ),
        play_ok1=0xAAAAAAAA,
        play_ok2=0xBBBBBBBB,
        login_ok1=0x11111111,
        login_ok2=0x22222222,
        username="testuser",
    )

    session = await GameFlow(login_result, char_slot=0).execute()

    assert session.character is not None
    assert session.character.name == "Test"
    assert session.session_id == 12345


@pytest.mark.asyncio
async def test_game_connection(mock_game_server):
    """Тест GameConnection."""
    crypt = GameCrypt()
    conn = GameConnection(
        mock_game_server.host,
        mock_game_server.port,
        crypt,
    )

    async with conn:
        # Отправляем ProtocolVersion (raw)
        await conn.send_packet(ProtocolVersionPacket(), raw=True)

        # Получаем KeyPacket
        opcode, data = await conn.read_packet()
        assert opcode == 0x2E
        key_packet = KeyPacket(data)
        assert key_packet.enabled is True
        assert len(key_packet.xor_key) == 8

        # Включаем шифрование
        crypt.set_key(key_packet.xor_key)


@pytest.mark.asyncio
async def test_no_characters():
    """Тест когда нет персонажей."""
    async def handle_no_chars(reader, writer):
        try:
            # ProtocolVersion
            await reader.readexactly(2)
            await reader.readexactly(100)

            # KeyPacket
            key_packet = bytes([0x2E, 0x01]) + b"xorkey12"
            key_packet += struct.pack("<II", 1, 0)
            writer.write((len(key_packet) + 2).to_bytes(2, "little") + key_packet)
            await writer.drain()

            # AuthLogin
            await reader.readexactly(2)
            await reader.readexactly(100)

            # CharSelectionInfo с 0 персонажей
            response = bytes([0x13, 0x00])  # count=0
            writer.write((len(response) + 2).to_bytes(2, "little") + response)
            await writer.drain()

        finally:
            writer.close()
            await writer.wait_closed()

    server = await asyncio.start_server(handle_no_chars, "127.0.0.1", 0)
    addr = server.sockets[0].getsockname()

    try:
        login_result = LoginResult(
            server=GameServer(id=1, ip=addr[0], port=addr[1], online=0, max_online=0),
            play_ok1=1,
            play_ok2=2,
            login_ok1=3,
            login_ok2=4,
            username="test",
        )

        with pytest.raises(GameError, match="No characters on account"):
            await GameFlow(login_result, char_slot=0).execute()
    finally:
        server.close()
        await server.wait_closed()
