# -*- coding: utf-8 -*-
"""TCP-соединение с Game Server.

Асинхронное соединение с использованием asyncio.
Поддерживает XOR-шифрование GameCrypt.
"""

import asyncio
import logging
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from l2py.crypto.game_crypt import GameCrypt
    from l2py.protocol.base import ClientPacket

logger = logging.getLogger(__name__)

DEFAULT_TIMEOUT = 10.0  # seconds


class GameConnection:
    """TCP-соединение с Game Server.

    Управляет подключением, чтением и записью пакетов.
    Использует GameCrypt для XOR-шифрования.
    """

    __slots__ = (
        "_host",
        "_port",
        "_crypt",
        "_reader",
        "_writer",
        "_connected",
    )

    def __init__(self, host: str, port: int, crypt: "GameCrypt") -> None:
        """Инициализация соединения.

        Args:
            host: Адрес Game Server.
            port: Порт Game Server.
            crypt: Объект криптографии.
        """
        self._host = host
        self._port = port
        self._crypt = crypt
        self._reader: asyncio.StreamReader | None = None
        self._writer: asyncio.StreamWriter | None = None
        self._connected = False

    async def connect(self) -> None:
        """Устанавливает TCP-соединение с сервером.

        Raises:
            ConnectionError: Если не удалось подключиться.
            asyncio.TimeoutError: Если превышен таймаут.
        """
        try:
            self._reader, self._writer = await asyncio.wait_for(
                asyncio.open_connection(self._host, self._port),
                timeout=DEFAULT_TIMEOUT,
            )
            self._connected = True
            logger.info(f"Connected to Game Server at {self._host}:{self._port}")
        except (asyncio.TimeoutError, OSError) as e:
            raise ConnectionError(
                f"Failed to connect to Game Server: {e}"
            ) from e

    async def read_packet(self) -> tuple[int, bytes]:
        """Читает пакет от сервера.

        Читает длину (2 байта), затем тело пакета.
        Дешифрует данные если шифрование включено.

        Returns:
            Кортеж (opcode, data), где data — тело пакета без опкода.

        Raises:
            ConnectionError: Если соединение закрыто.
            asyncio.TimeoutError: Если превышен таймаут.
        """
        if not self._connected or self._reader is None:
            raise ConnectionError("Not connected")

        try:
            # Читаем длину (2 байта, uint16 LE)
            length_bytes = await asyncio.wait_for(
                self._reader.readexactly(2),
                timeout=DEFAULT_TIMEOUT,
            )
            length = int.from_bytes(length_bytes, "little")

            if length < 2:
                raise ConnectionError(f"Invalid packet length: {length}")

            # Читаем тело пакета
            body = await asyncio.wait_for(
                self._reader.readexactly(length - 2),
                timeout=DEFAULT_TIMEOUT,
            )

            # Дешифруем если включено
            # НО: проверяем, не пришёл ли пакет без шифрования
            # KeyPacket (0x2E) приходит без шифрования
            # Ожидаемые опкоды: 0x09 (CharSelectionInfo), 0x0B (CharSelected), etc.
            EXPECTED_OPCODES = {0x09, 0x0A, 0x0B, 0x0C, 0x32, 0x2E}
            if body[0] in EXPECTED_OPCODES:
                # Пакет не зашифрован
                decrypted = body
            else:
                decrypted = self._crypt.decrypt(body)

            # Первый байт = opcode
            opcode = decrypted[0]
            data = decrypted[1:]

            logger.debug(
                f"[Game] Received packet: opcode=0x{opcode:02X}, length={len(data)}"
            )

            return opcode, data

        except asyncio.IncompleteReadError as e:
            raise ConnectionError(
                f"Connection closed while reading packet: {e}"
            ) from e
        except asyncio.TimeoutError:
            raise

    async def send_packet(self, packet: "ClientPacket", raw: bool = False) -> None:
        """Отправляет пакет на сервер.

        Args:
            packet: Пакет для отправки.
            raw: Если True — не шифровать (для ProtocolVersion).

        Raises:
            ConnectionError: Если не подключены.
        """
        if not self._connected or self._writer is None:
            raise ConnectionError("Not connected")

        # Сериализуем пакет
        data = packet.to_bytes()

        # Шифруем если не raw
        if raw:
            encrypted = data
        else:
            encrypted = self._crypt.encrypt(data)

        # Формируем пакет с длиной
        length = len(encrypted) + 2
        packet_bytes = length.to_bytes(2, "little") + encrypted

        # Отправляем
        self._writer.write(packet_bytes)
        await self._writer.drain()

        logger.debug(
            f"[Game] Sent packet: opcode=0x{packet.opcode:02X}, "
            f"length={len(data)}, raw={raw}"
        )

    async def close(self) -> None:
        """Закрывает соединение."""
        if self._writer is not None:
            self._writer.close()
            try:
                await self._writer.wait_closed()
            except Exception:
                pass
        self._connected = False
        logger.info("Disconnected from Game Server")

    async def __aenter__(self) -> "GameConnection":
        """Асинхронный контекстный менеджер — вход."""
        await self.connect()
        return self

    async def __aexit__(self, exc_type, exc_val, exc_tb) -> None:
        """Асинхронный контекстный менеджер — выход."""
        await self.close()


__all__ = ["GameConnection"]
