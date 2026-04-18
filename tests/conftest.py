
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
    return LoginConfig(host="192.168.0.33", port=2106)


@pytest.fixture
def login_crypt() -> LoginCrypt:
    """Фикстура с настроенной криптографией."""
    crypt = LoginCrypt()

    crypt.set_key(b"test_key_16bytes")
    return crypt


@pytest.fixture
async def mock_login_server() -> AsyncGenerator[tuple[str, int], None]:
    """Фикстура с мок Login Server.

    Запускает простой TCP-сервер на свободном порту.
    """

    crypt = LoginCrypt()
    crypt.set_key(b"session_key_16by")
    blowfish = L2Blowfish(b"session_key_16by")

    async def handle_client(reader: asyncio.StreamReader, writer: asyncio.StreamWriter) -> None:
        """Обработчик клиентских соединений."""
        try:


            init_data = (
                bytes([0x00])
                + b"\x01\x00\x00\x00"
                + b"\x0B\x01\x00\x00"
                + b"\x00" * 128
                + b"\x00" * 16
                + b"session_key_16by"
                + b"\x00" * 7
                + b"\x00" * 8
            )


            encrypted_init = crypt._static_cipher.encrypt(init_data)
            length = len(encrypted_init) + 2
            writer.write(length.to_bytes(2, "little") + encrypted_init)
            await writer.drain()


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


                    decrypted = blowfish.decrypt(body)
                    opcode = decrypted[0]


                    if opcode == 0x07:

                        response = bytes([0x0B]) + b"\x00\x00\x00\x00"
                        encrypted = blowfish.encrypt(response)
                        writer.write((len(encrypted) + 2).to_bytes(2, "little") + encrypted)
                        await writer.drain()

                    elif opcode == 0x00:

                        response = bytes([0x03]) + b"\x11\x11\x11\x11" + b"\x22\x22\x22\x22"
                        encrypted = blowfish.encrypt(response)
                        writer.write((len(encrypted) + 2).to_bytes(2, "little") + encrypted)
                        await writer.drain()

                    elif opcode == 0x05:

                        response = bytes([0x04, 0x01, 0x00])
                        response += bytes([0x01])
                        response += bytes([127, 0, 0, 1])
                        response += (30000).to_bytes(4, "little")
                        response += bytes([0, 0])
                        response += (100).to_bytes(2, "little")
                        response += (400).to_bytes(2, "little")
                        response += bytes([1])
                        response += b"\x00" * 7

                        encrypted = blowfish.encrypt(response)
                        writer.write((len(encrypted) + 2).to_bytes(2, "little") + encrypted)
                        await writer.drain()

                    elif opcode == 0x02:

                        response = bytes([0x07]) + b"\xAA\xAA\xAA\xAA" + b"\xBB\xBB\xBB\xBB"
                        encrypted = blowfish.encrypt(response)
                        writer.write((len(encrypted) + 2).to_bytes(2, "little") + encrypted)
                        await writer.drain()
                        break

                except asyncio.TimeoutError:
                    break

        finally:
            writer.close()
            await writer.wait_closed()


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

            length_bytes = await reader.readexactly(2)
            length = int.from_bytes(length_bytes, "little")
            await reader.readexactly(length - 2)


            key_packet = bytes([0x2E, 0x01])
            key_packet += b"key12345"
            key_packet += b"\x00\x00\x00\x00"
            key_packet += (1).to_bytes(4, "little")
            key_packet += b"\x00\x00\x00\x00"

            writer.write((len(key_packet) + 2).to_bytes(2, "little") + key_packet)
            await writer.drain()


            await asyncio.sleep(0.1)

        finally:
            writer.close()
            await writer.wait_closed()

    server = await asyncio.start_server(handle_client, "192.168.0.33", 0)
    addr = server.sockets[0].getsockname()

    yield addr[0], addr[1]

    server.close()
    await server.wait_closed()
