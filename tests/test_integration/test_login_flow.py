# -*- coding: utf-8 -*-
"""Интеграционные тесты для Login Flow.

Тестируют полный процесс авторизации на мок Login Server.
"""

import asyncio
import struct

import pytest

from l2py.config import Credentials, LoginConfig
from l2py.crypto.blowfish import L2Blowfish
from l2py.crypto.login_crypt import LoginCrypt
from l2py.crypto.rsa import L2RSA
from l2py.network.login_connection import LoginConnection
from l2py.network.login_flow import LoginError, LoginFlow, LoginResult
from l2py.protocol.login.client_packets import (
    AuthGameGuardPacket,
    RequestAuthLoginPacket,
    RequestServerListPacket,
    RequestServerLoginPacket,
)
from l2py.protocol.login.server_packets import (
    GGAuthPacket,
    InitPacket,
    LoginOkPacket,
    PlayOkPacket,
    ServerListPacket,
)


class MockLoginServer:
    """Мок Login Server для тестирования."""

    def __init__(self, host: str = "127.0.0.1", port: int = 0):
        self.host = host
        self.port = port
        self.server = None
        self.session_key = b"session_key_16by"
        self.crypt = LoginCrypt()
        self.crypt.set_key(self.session_key)
        self.blowfish = L2Blowfish(self.session_key)

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
        print(f"MockServer: Client connected")
        try:
            # Отправляем Init пакет
            await self._send_init(writer)
            print("MockServer: Sent InitPacket")

            # Обрабатываем последующие пакеты
            while True:
                try:
                    opcode, data = await self._read_packet(reader)
                    print(f"MockServer: Received packet: opcode=0x{opcode:02X}, length={len(data)}")
                except (asyncio.TimeoutError, asyncio.IncompleteReadError):
                    print("MockServer: Client disconnected")
                    break
                except Exception as e:
                    print(f"MockServer: Error reading packet: {e}")
                    break

                if opcode == 0x07:  # AuthGameGuard
                    print("MockServer: Handling AuthGameGuard (0x07)")
                    await self._send_gg_auth(writer)
                    print("MockServer: Sent GGAuth (0x0B)")

                elif opcode == 0x00:  # RequestAuthLogin
                    print("MockServer: Handling RequestAuthLogin (0x00)")
                    await self._send_login_ok(writer)
                    print("MockServer: Sent LoginOk (0x03)")

                elif opcode == 0x05:  # RequestServerList
                    print("MockServer: Handling RequestServerList (0x05)")
                    await self._send_server_list(writer)
                    print("MockServer: Sent ServerList (0x04)")

                elif opcode == 0x02:  # RequestServerLogin
                    print("MockServer: Handling RequestServerLogin (0x02)")
                    await self._send_play_ok(writer)
                    print("MockServer: Sent PlayOk (0x07)")
                    break
                else:
                    print(f"MockServer: Received UNKNOWN opcode 0x{opcode:02X}")

        finally:
            writer.close()
            await writer.wait_closed()
    async def _send_init(self, writer):
        """Отправляет Init пакет."""
        init_data = (
            bytes([0x00])  # Init opcode
            + struct.pack("<I", 0x12345678)  # session_id
            + struct.pack("<I", 267)  # protocol_version
            + b"\x00" * 128  # rsa_key
            + b"\x00" * 16  # gg data
            + self.session_key  # blowfish_key (16 bytes)
            + b"\x00" * 7  # align
            + b"\xDEADBEEF"  # XOR key (4 bytes)
            + b"\x00" * 4  # padding for XOR tail
        )
        
        # Используем новую функцию шифрования с XOR pass
        encrypted = self.crypt.encrypt_init(init_data)
        
        length = len(encrypted) + 2
        writer.write(length.to_bytes(2, "little") + encrypted)
        await writer.drain()

    async def _send_gg_auth(self, writer):
        """Отправляет GGAuth пакет."""
        response = bytes([0x0B]) + struct.pack("<I", 0)
        encrypted = self.crypt.encrypt(response)
        length = len(encrypted) + 2
        writer.write(length.to_bytes(2, "little") + encrypted)
        await writer.drain()

    async def _send_login_ok(self, writer):
        """Отправляет LoginOk пакет."""
        response = bytes([0x03]) + struct.pack("<II", 0x11111111, 0x22222222)
        encrypted = self.crypt.encrypt(response)
        length = len(encrypted) + 2
        writer.write(length.to_bytes(2, "little") + encrypted)
        await writer.drain()

    async def _send_server_list(self, writer):
        """Отправляет ServerList пакет."""
        # Opcode 0x04, Count 1, LastServer 1
        # Server: ID 1, IP 127.0.0.1, Port 7777, AgeLimit 0, PVP 0, Online 0, MaxOnline 1000, Status 1
        response = bytes([0x04, 0x01, 0x01]) + bytes([
            0x01, # ID
            127, 0, 0, 1, # IP
            0x39, 0x1E, 0x00, 0x00, # Port 7777
            0x00, # AgeLimit
            0x00, # PVP
            0x00, 0x00, # Online
            0xE8, 0x03, # MaxOnline 1000
            0x01, # Status
        ]) + b"\x00" * 10 # Extra bytes
        
        encrypted = self.crypt.encrypt(response)
        length = len(encrypted) + 2
        writer.write(length.to_bytes(2, "little") + encrypted)
        await writer.drain()

    async def _send_play_ok(self, writer):
        """Отправляет PlayOk пакет."""
        response = bytes([0x07]) + struct.pack("<II", 0xAAAAAAAA, 0xBBBBBBBB)
        encrypted = self.crypt.encrypt(response)
        length = len(encrypted) + 2
        writer.write(length.to_bytes(2, "little") + encrypted)
        await writer.drain()

    async def _read_packet(self, reader) -> tuple[int, bytes]:
        """Читает пакет от клиента."""
        length_bytes = await reader.readexactly(2)
        length = int.from_bytes(length_bytes, "little")

        body = await reader.readexactly(length - 2)
        # Используем LoginCrypt для дешифрования и проверки чексуммы
        decrypted = self.crypt.decrypt(body)

        return decrypted[0], decrypted[1:]


@pytest.fixture
async def mock_login_server():
    """Фикстура с мок Login Server."""
    server = MockLoginServer()
    await server.start()
    yield server
    await server.stop()


@pytest.mark.asyncio
async def test_full_login_flow(mock_login_server):
    """Тест полного login flow."""
    config = LoginConfig(
        host=mock_login_server.host,
        port=mock_login_server.port,
    )
    credentials = Credentials(username="testuser", password="testpass")

    result = await LoginFlow(config, credentials).execute()

    assert isinstance(result, LoginResult)
    assert result.server.id == 2
    assert result.server.ip == "127.0.0.1"
    assert result.server.port == 30000
    assert result.play_ok1 == 0xAAAAAAAA
    assert result.play_ok2 == 0xBBBBBBBB
    assert result.login_ok1 == 0x11111111
    assert result.login_ok2 == 0x22222222
    assert result.username == "testuser"


@pytest.mark.asyncio
async def test_login_connection(mock_login_server):
    """Тест LoginConnection."""
    crypt = LoginCrypt()
    conn = LoginConnection(
        mock_login_server.host,
        mock_login_server.port,
        crypt,
    )

    async with conn:
        # Получаем Init
        opcode, data = await conn.read_packet()
        assert opcode == 0x00
        init = InitPacket(data)
        assert init.session_id == 0x12345678
        crypt.set_key(init.blowfish_key)

        # Отправляем AuthGameGuard
        await conn.send_packet(AuthGameGuardPacket(init.session_id))

        # Получаем GGAuth
        opcode, data = await conn.read_packet()
        assert opcode == 0x0B
        gg_auth = GGAuthPacket(data)
        assert gg_auth.response == 0

        # Отправляем RequestAuthLogin
        rsa = L2RSA(b"\x00" * 128)
        await conn.send_packet(
            RequestAuthLoginPacket(
                username="test",
                password="test",
                session_id=init.session_id,
                rsa=rsa,
            )
        )

        # Получаем LoginOk
        opcode, data = await conn.read_packet()
        assert opcode == 0x03


@pytest.mark.asyncio
async def test_login_fail():
    """Тест обработки ошибки авторизации."""
    # Создаём сервер, который отправляет LoginFail
    async def handle_fail(reader, writer):
        try:
            # Init
            crypt = LoginCrypt()
            session_key = b"session_key_16by"
            crypt.set_key(session_key)

            init_data = (
                bytes([0x00])  # Init opcode
                + struct.pack("<I", 1)
                + struct.pack("<I", 267)
                + b"\x00" * 128
                + b"\x00" * 16
                + session_key
                + b"\x00" * 7  # align
                + b"\x00" * 8  # XOR tail
            )
            encrypted = crypt._static_cipher.encrypt(init_data)
            length = len(encrypted) + 2
            writer.write(length.to_bytes(2, "little") + encrypted)
            await writer.drain()

            # Читаем AuthGameGuard
            await reader.readexactly(2)
            await reader.readexactly(100)  # Приблизительно

            # Отправляем GGAuth
            blowfish = L2Blowfish(session_key)
            response = bytes([0x0B]) + struct.pack("<I", 0)
            encrypted = blowfish.encrypt(response)
            writer.write((len(encrypted) + 2).to_bytes(2, "little") + encrypted)
            await writer.drain()

            # Читаем RequestAuthLogin
            await reader.readexactly(2)
            await reader.readexactly(150)

            # Отправляем LoginFail
            response = bytes([0x01, 0x02])  # opcode=0x01, reason=0x02
            encrypted = blowfish.encrypt(response)
            writer.write((len(encrypted) + 2).to_bytes(2, "little") + encrypted)
            await writer.drain()

        finally:
            writer.close()
            await writer.wait_closed()

    server = await asyncio.start_server(handle_fail, "127.0.0.1", 0)
    addr = server.sockets[0].getsockname()

    try:
        config = LoginConfig(host=addr[0], port=addr[1])
        credentials = Credentials(username="test", password="test")

        with pytest.raises(LoginError) as exc_info:
            await LoginFlow(config, credentials).execute()

        assert "Password is incorrect" in str(exc_info.value)
    finally:
        server.close()
        await server.wait_closed()
