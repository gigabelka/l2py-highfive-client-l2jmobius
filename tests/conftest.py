# -*- coding: utf-8 -*-
"""Фикстуры для тестов.

Содержит мок-серверы и вспомогательные фикстуры.
"""

import asyncio
from collections.abc import AsyncGenerator

import pytest

from l2py.config import Credentials, LoginConfig
from l2py.crypto.blowfish import L2Blowfish
from l2py.crypto.login_crypt import LoginCrypt


@pytest.fixture
def sample_credentials() -> Credentials:
    """Фикстура с тестовыми учётными данными."""
    return Credentials(username="testuser", password="testpass")


@pytest.fixture
def sample_login_config() -> LoginConfig:
    """Фикстура с тестовой конфигурацией."""
    return LoginConfig(host="192.168.0.33", port=2106, server_id=2)


@pytest.fixture
def login_crypt() -> LoginCrypt:
    """Фикстура с настроенной криптографией."""
    crypt = LoginCrypt()
    # Устанавливаем тестовый сессионный ключ
    crypt.set_key(b"test_key_16bytes")
    return crypt


@pytest.fixture
async def mock_login_server() -> AsyncGenerator[tuple[str, int], None]:
    """Фикстура с мок Login Server.

    Запускает простой TCP-сервер на свободном порту.
    """
    # Создаём криптографию для сервера
    crypt = LoginCrypt()
    crypt.set_key(b"session_key_16by")
    blowfish = L2Blowfish(b"session_key_16by")

    async def handle_client(reader: asyncio.StreamReader, writer: asyncio.StreamWriter) -> None:
        """Обработчик клиентских соединений."""
        try:
            # Отправляем Init пакет
            init_data = (
                b"\x01\x00\x00\x00"  # session_id = 1
                b"\x0B\x01\x00\x00"  # protocol_version = 267
                + b"\x00" * 128  # rsa_key
                + b"\x00" * 16  # gg data
                + b"session_key_16by"  # blowfish_key
            )

            # Шифруем Init пакет
            encrypted_init = crypt._static_cipher.encrypt(init_data)
            length = len(encrypted_init) + 2
            writer.write(length.to_bytes(2, "little") + encrypted_init)
            await writer.drain()

            # Читаем и отвечаем на остальные пакеты (упрощённо)
            while True:
                try:
                    length_bytes = await asyncio.wait_for(
                        reader.readexactly(2), timeout=1.0
                    )
                    length = int.from_bytes(length_bytes, "little")

                    if length < 2:
                        break

                    body = await asyncio.wait_for(
                        reader.readexactly(length - 2), timeout=1.0
                    )

                    # Дешифруем
                    decrypted = blowfish.decrypt(body)
                    opcode = decrypted[0]

                    # Отвечаем в зависимости от опкода
                    if opcode == 0x07:  # AuthGameGuard
                        # Отправляем GGAuth (0x0B)
                        response = bytes([0x0B]) + b"\x00\x00\x00\x00"
                        encrypted = blowfish.encrypt(response)
                        writer.write((len(encrypted) + 2).to_bytes(2, "little") + encrypted)
                        await writer.drain()

                    elif opcode == 0x00:  # RequestAuthLogin
                        # Отправляем LoginOk (0x03)
                        response = bytes([0x03]) + b"\x11\x11\x11\x11" + b"\x22\x22\x22\x22"
                        encrypted = blowfish.encrypt(response)
                        writer.write((len(encrypted) + 2).to_bytes(2, "little") + encrypted)
                        await writer.drain()

                    elif opcode == 0x05:  # RequestServerList
                        # Отправляем ServerList (0x04)
                        response = bytes([0x04, 0x01, 0x00])  # count=1, last_server=0
                        response += bytes([0x01])  # server_id=2
                        response += bytes([127, 0, 0, 1])  # ip
                        response += (30000).to_bytes(4, "little")  # port
                        response += bytes([0, 0])  # age_limit, pvp
                        response += (100).to_bytes(2, "little")  # online
                        response += (400).to_bytes(2, "little")  # max_online
                        response += bytes([1])  # status
                        response += b"\x00" * 7  # padding

                        encrypted = blowfish.encrypt(response)
                        writer.write((len(encrypted) + 2).to_bytes(2, "little") + encrypted)
                        await writer.drain()

                    elif opcode == 0x02:  # RequestServerLogin
                        # Отправляем PlayOk (0x07)
                        response = bytes([0x07]) + b"\xAA\xAA\xAA\xAA" + b"\xBB\xBB\xBB\xBB"
                        encrypted = blowfish.encrypt(response)
                        writer.write((len(encrypted) + 2).to_bytes(2, "little") + encrypted)
                        await writer.drain()
                        break  # Закрываем соединение

                except asyncio.TimeoutError:
                    break

        finally:
            writer.close()
            await writer.wait_closed()

    # Запускаем сервер на случайном порту
    server = await asyncio.start_server(handle_client, "192.168.0.33", 0)
    addr = server.sockets[0].getsockname()

    yield addr[0], addr[1]

    server.close()
    await server.wait_closed()


@pytest.fixture
async def mock_game_server() -> AsyncGenerator[tuple[str, int], None]:
    """Фикстура с мок Game Server."""
    async def handle_client(reader: asyncio.StreamReader, writer: asyncio.StreamWriter) -> None:
        """Обработчик клиентских соединений."""
        try:
            # Читаем ProtocolVersion
            length_bytes = await reader.readexactly(2)
            length = int.from_bytes(length_bytes, "little")
            await reader.readexactly(length - 2)

            # Отправляем KeyPacket (0x2E)
            key_packet = bytes([0x2E, 0x01])  # opcode, enabled=1
            key_packet += b"key12345"  # xor_key (8 bytes)
            key_packet += b"\x00\x00\x00\x00"  # unknown
            key_packet += (1).to_bytes(4, "little")  # server_id
            key_packet += b"\x00\x00\x00\x00"  # obfuscation_key

            writer.write((len(key_packet) + 2).to_bytes(2, "little") + key_packet)
            await writer.drain()

            # Остальные пакеты шифруются — упрощаем тест
            await asyncio.sleep(0.1)

        finally:
            writer.close()
            await writer.wait_closed()

    server = await asyncio.start_server(handle_client, "192.168.0.33", 0)
    addr = server.sockets[0].getsockname()

    yield addr[0], addr[1]

    server.close()
    await server.wait_closed()
