
"""TCP-соединение с Login Server.

Асинхронное соединение с использованием asyncio.
Поддерживает шифрование LoginCrypt.
"""

import asyncio
import logging
from typing import TYPE_CHECKING

from l2py.debug.packet_inspector import create_inspector

if TYPE_CHECKING:
    from l2py.crypto.login_crypt import LoginCrypt
    from l2py.protocol.base import ClientPacket

logger = logging.getLogger(__name__)

DEFAULT_TIMEOUT = 10.0


class LoginConnection:
    """TCP-соединение с Login Server.

    Управляет подключением, чтением и записью пакетов.
    Использует LoginCrypt для шифрования/дешифрования.
    """

    __slots__ = (
        "_host",
        "_port",
        "_crypt",
        "_reader",
        "_writer",
        "_is_first_packet",
        "_connected",
        "_packet_inspector",
        "_debug_enabled",
    )

    def __init__(self, host: str, port: int, crypt: "LoginCrypt", debug_packets: bool = False) -> None:
        """Инициализация соединения.

        Args:
            host: Адрес Login Server.
            port: Порт Login Server (обычно 2106).
            crypt: Объект криптографии.
            debug_packets: Включить детальную отладку пакетов.
        """
        self._host = host
        self._port = port
        self._crypt = crypt
        self._reader: asyncio.StreamReader | None = None
        self._writer: asyncio.StreamWriter | None = None
        self._is_first_packet = True
        self._connected = False
        self._debug_enabled = debug_packets
        self._packet_inspector = create_inspector(debug_packets) if debug_packets else None

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
            logger.info(f"Connected to Login Server at {self._host}:{self._port}")
        except (asyncio.TimeoutError, OSError) as e:
            raise ConnectionError(
                f"Failed to connect to Login Server: {e}"
            ) from e

    async def read_packet(self, expected_opcode: int | None = None) -> tuple[int, bytes]:
        """Читает пакет от сервера.

        Читает длину (2 байта), затем тело пакета.
        Дешифрует данные согласно протоколу:
        - Первый пакет (Init) — через decrypt_init
        - Остальные пакеты — через decrypt с checksum

        Args:
            expected_opcode: Ожидаемый opcode для отладки (опционально).

        Returns:
            Кортеж (opcode, data), где data — тело пакета без опкода.

        Raises:
            ConnectionError: Если соединение закрыто.
            asyncio.TimeoutError: Если превышен таймаут.
        """
        if not self._connected or self._reader is None:
            raise ConnectionError("Not connected")

        raw_packet_data = b""
        decrypted_data = None
        context = f"{'First packet (Init)' if self._is_first_packet else 'Regular packet'}"

        try:

            length_bytes = await asyncio.wait_for(
                self._reader.readexactly(2),
                timeout=DEFAULT_TIMEOUT,
            )
            length = int.from_bytes(length_bytes, "little")

            if length < 2:
                error_msg = f"Invalid packet length: {length}"
                logger.error(f"[Login] {error_msg}")
                raise ConnectionError(error_msg)


            body = await asyncio.wait_for(
                self._reader.readexactly(length - 2),
                timeout=DEFAULT_TIMEOUT,
            )

            raw_packet_data = length_bytes + body


            logger.debug(f"[Login] Raw packet: length={length}, body={body.hex()}")


            try:
                if self._is_first_packet:
                    decrypted_data = self._crypt.decrypt_init(body)


                    if expected_opcode is not None and (not decrypted_data or decrypted_data[0] != expected_opcode):
                        logger.warning(
                            f"[Login] First packet opcode mismatch: expected 0x{expected_opcode:02X}, "
                            f"got 0x{decrypted_data[0] if decrypted_data else 'None':02X}. "
                            f"Attempting auto-detection of static Blowfish key..."
                        )

                        results = self._crypt.test_decrypt_with_all_keys(body)
                        found_key = False
                        for key_name, (success, final_data, msg) in results.items():
                            if success and final_data and final_data[0] == expected_opcode:
                                logger.info(f"[Login] AUTO-DETECTED correct static key: {key_name}")
                                from l2py.crypto.login_crypt import AVAILABLE_KEYS
                                self._crypt.update_static_key(AVAILABLE_KEYS[key_name])
                                decrypted_data = final_data
                                found_key = True
                                break

                        if not found_key:
                            logger.error("[Login] Auto-detection failed: no suitable key found for this packet.")

                    self._is_first_packet = False
                    logger.debug(f"[Login] Used decrypt_init for first packet")
                else:
                    decrypted_data = self._crypt.decrypt(body)
                    logger.debug(f"[Login] Used decrypt for regular packet")

                logger.debug(f"[Login] Decryption successful, {len(decrypted_data)} bytes")

            except Exception as e:
                decryption_error = e
                logger.error(f"[Login] Decryption failed: {e}")


                if self._packet_inspector:
                    analysis = self._packet_inspector.analyze_packet(
                        raw_data=raw_packet_data,
                        decrypted_data=None,
                        expected_opcode=expected_opcode,
                        packet_source="login"
                    )
                    self._packet_inspector.log_packet_analysis(analysis, f"DECRYPTION FAILED: {context}")

                    issues = self._packet_inspector.detect_potential_issues(analysis)
                    if issues:
                        logger.error(f"[Login] Potential issues detected: {'; '.join(issues)}")

                raise ConnectionError(f"Packet decryption failed: {e}") from e

            if not decrypted_data or len(decrypted_data) == 0:
                error_msg = "Decrypted packet is empty"
                logger.error(f"[Login] {error_msg}")
                raise ConnectionError(error_msg)


            opcode = decrypted_data[0]
            data = decrypted_data[1:]


            if self._packet_inspector:
                analysis = self._packet_inspector.analyze_packet(
                    raw_data=raw_packet_data,
                    decrypted_data=decrypted_data,
                    expected_opcode=expected_opcode,
                    packet_source="login"
                )
                self._packet_inspector.log_packet_analysis(analysis, context)


                issues = self._packet_inspector.detect_potential_issues(analysis)
                if issues:
                    logger.warning(f"[Login] Potential issues detected: {'; '.join(issues)}")


                if self._is_first_packet and opcode == 0x00:
                    is_valid, validation_msg = self._packet_inspector.validate_init_packet_structure(decrypted_data)
                    if not is_valid:
                        logger.error(f"[Login] InitPacket validation failed: {validation_msg}")
                    else:
                        logger.debug(f"[Login] InitPacket validation: {validation_msg}")

            logger.debug(
                f"[Login] Received packet: opcode=0x{opcode:02X}, length={len(data)}"
            )


            if expected_opcode is not None and opcode != expected_opcode:
                logger.error(
                    f"[Login] OPCODE MISMATCH: expected 0x{expected_opcode:02X}, "
                    f"got 0x{opcode:02X}. Context: {context}"
                )


                if opcode == 0x15:
                    logger.error(
                        f"[Login] CRITICAL: Received CharSelectedPacket (0x15) from Login Server! "
                        f"This is a Game Server packet - possible connection or protocol issue."
                    )

            return opcode, data

        except asyncio.IncompleteReadError as e:
            error_msg = f"Connection closed while reading packet: {e}"
            logger.error(f"[Login] {error_msg}")


            if raw_packet_data:
                logger.debug(f"[Login] Partial data received: {raw_packet_data.hex()}")

            raise ConnectionError(error_msg) from e
        except asyncio.TimeoutError:
            logger.error(f"[Login] Timeout while reading packet. Context: {context}")
            raise
        except Exception as e:
            logger.error(f"[Login] Unexpected error reading packet: {e}. Context: {context}")


            if self._packet_inspector and raw_packet_data:
                analysis = self._packet_inspector.analyze_packet(
                    raw_data=raw_packet_data,
                    decrypted_data=decrypted_data,
                    expected_opcode=expected_opcode,
                    packet_source="login"
                )
                self._packet_inspector.log_packet_analysis(analysis, f"UNEXPECTED ERROR: {context}")

            raise

    async def send_packet(self, packet: "ClientPacket") -> None:
        """Отправляет пакет на сервер.

        Args:
            packet: Пакет для отправки.

        Raises:
            ConnectionError: Если не подключены.
        """
        if not self._connected or self._writer is None:
            raise ConnectionError("Not connected")


        data = packet.to_bytes()


        encrypted = self._crypt.encrypt(data)


        length = len(encrypted) + 2
        packet_bytes = length.to_bytes(2, "little") + encrypted


        self._writer.write(packet_bytes)
        await self._writer.drain()

        logger.debug(
            f"[Login] Sent packet: opcode=0x{packet.opcode:02X}, "
            f"length={len(data)}"
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
        logger.info("Disconnected from Login Server")

    async def __aenter__(self) -> "LoginConnection":
        """Асинхронный контекстный менеджер — вход."""
        await self.connect()
        return self

    async def __aexit__(self, exc_type, exc_val, exc_tb) -> None:
        """Асинхронный контекстный менеджер — выход."""
        await self.close()


__all__ = ["LoginConnection"]
