# -*- coding: utf-8 -*-
"""Оркестрация процесса авторизации на Login Server.

Реализует полный flow от подключения до получения PlayOk.
"""

import logging
from dataclasses import dataclass

from l2py.config import Credentials, LoginConfig
from l2py.crypto.login_crypt import LoginCrypt, create_login_crypt_for_l2jmobius
from l2py.crypto.rsa import L2RSA, unscramble_modulus, create_l2rsa_with_auto_descramble
from l2py.debug.packet_inspector import create_inspector
from l2py.models.server import GameServer
from l2py.network.login_connection import LoginConnection
from l2py.protocol.login.client_packets import (
    AuthGameGuardPacket,
    RequestAuthLoginPacket,
    RequestServerListPacket,
    RequestServerLoginPacket,
)
from l2py.protocol.login.server_packets import (
    GGAuthPacket,
    InitPacket,
    LoginFailPacket,
    LoginOkPacket,
    PlayOkPacket,
    ServerListPacket,
)

logger = logging.getLogger(__name__)

# Коды ошибок авторизации
LOGIN_FAIL_REASONS = {
    0x01: "Account does not exist",
    0x02: "Password is incorrect",
    0x03: "Password does not match this account",
    0x04: "Account is banned",
    0x05: "Account is already in use",
    0x06: "Server is under maintenance",
    0x07: "Account is already in use",
    0x08: "Server is full",
    0x09: "Server is under maintenance",
    0x0A: "Login is currently prohibited",
    0x0B: "Server is full (queue)",
}


class LoginError(Exception):
    """Ошибка авторизации."""

    def __init__(self, reason_code: int, message: str | None = None) -> None:
        """Инициализация ошибки.

        Args:
            reason_code: Код ошибки от сервера.
            message: Опциональное сообщение.
        """
        self.reason_code = reason_code
        self.reason_text = LOGIN_FAIL_REASONS.get(reason_code, f"Unknown error: 0x{reason_code:02X}")
        if message is None:
            message = self.reason_text
        super().__init__(message)


@dataclass(frozen=True, slots=True)
class LoginResult:
    """Результат успешной авторизации.

    Содержит все данные необходимые для подключения к Game Server.
    """

    server: GameServer
    play_ok1: int
    play_ok2: int
    login_ok1: int
    login_ok2: int
    username: str


class LoginFlow:
    """Оркестрирует полный процесс авторизации на Login Server.

    Реализует следующий flow:
    1. Подключение к Login Server
    2. Получение Init (session_id, rsa_key, blowfish_key)
    3. Отправка AuthGameGuard
    4. Авторизация (RequestAuthLogin)
    5. Получение списка серверов
    6. Выбор сервера и получение PlayOk
    """

    __slots__ = ("_config", "_credentials", "_server_id", "_debug_enabled", "_packet_inspector")

    def __init__(self, config: LoginConfig, credentials: Credentials, server_id: int = 2, debug_packets: bool = False) -> None:
        """Инициализация flow.

        Args:
            config: Конфигурация подключения.
            credentials: Учётные данные.
            server_id: ID игрового сервера.
            debug_packets: Включить детальную отладку пакетов.
        """
        self._config = config
        self._credentials = credentials
        self._server_id = server_id
        self._debug_enabled = debug_packets
        self._packet_inspector = create_inspector(debug_packets) if debug_packets else None

    async def execute(self) -> LoginResult:
        """Выполняет полный процесс авторизации.

        Returns:
            Результат авторизации с данными для Game Server.

        Raises:
            LoginError: Если авторизация не удалась.
            ConnectionError: Если проблемы с соединением.
        """
        # Создаём криптографию с поддержкой L2JMobius и соединение
        crypt = create_login_crypt_for_l2jmobius()
        conn = LoginConnection(
            self._config.host,
            self._config.port,
            crypt,
            debug_packets=self._debug_enabled,
        )

        try:
            await conn.connect()
            logger.info(f"Starting login flow for user: {self._credentials.username}")

            # Шаг 1: Получаем Init пакет
            logger.debug("Waiting for Init packet...")
            init = await self._wait_for_packet(conn, InitPacket)
            logger.debug(
                f"Received Init: session_id={init.session_id}, "
                f"protocol_version={init.protocol_version}"
            )

            # Устанавливаем сессионный Blowfish-ключ
            crypt.set_key(init.blowfish_key)

            # Создаём RSA с автоматическим выбором алгоритма дескремблирования для L2JMobius
            rsa = create_l2rsa_with_auto_descramble(init.rsa_key)
            logger.debug("Using auto-descrambling RSA for L2JMobius compatibility")

            # Шаг 2: Отправляем AuthGameGuard
            logger.debug("Sending AuthGameGuard...")
            await conn.send_packet(AuthGameGuardPacket(init.session_id))

            # Шаг 3: Ждём GGAuth
            logger.debug("Waiting for GGAuth...")
            gg_auth = await self._wait_for_packet(conn, GGAuthPacket)
            logger.debug(f"GGAuth received: response=0x{gg_auth.response:08X} ({gg_auth.response})")
            # L2JMobius возвращает session_id как response (проверено в коде сервера)
            # Считаем успешным любой ответ, главное что пакет пришёл с opcode 0x0B
            logger.debug("GGAuth successful")

            # Шаг 4: Отправляем RequestAuthLogin
            logger.debug("Sending RequestAuthLogin...")
            await conn.send_packet(
                RequestAuthLoginPacket(
                    username=self._credentials.username,
                    password=self._credentials.password,
                    session_id=init.session_id,
                    rsa=rsa,
                )
            )

            # Шаг 5: Ждём LoginOk или LoginFail
            logger.debug("Waiting for LoginOk...")
            opcode, data = await conn.read_packet()

            if opcode == LoginFailPacket.opcode:
                fail = LoginFailPacket(data)
                reason_msg = LOGIN_FAIL_REASONS.get(fail.reason, f"Unknown error: 0x{fail.reason:02X}")
                if fail.reason == 0x07:
                    reason_msg += " (wait a few seconds and try again)"
                raise LoginError(fail.reason, reason_msg)

            if opcode != LoginOkPacket.opcode:
                raise LoginError(0xFF, f"Unexpected packet opcode: 0x{opcode:02X}")

            login_ok = LoginOkPacket(data)
            logger.info(
                f"Login successful: login_ok1={login_ok.login_ok1}, "
                f"login_ok2={login_ok.login_ok2}"
            )

            # Шаг 6: Запрашиваем список серверов
            logger.debug("Requesting server list...")
            await conn.send_packet(
                RequestServerListPacket(
                    login_ok1=login_ok.login_ok1,
                    login_ok2=login_ok.login_ok2,
                )
            )

            # Шаг 7: Получаем список серверов
            logger.debug("Waiting for ServerList...")
            server_list = await self._wait_for_packet(conn, ServerListPacket)
            logger.debug(f"Received {len(server_list.servers)} servers")

            # Выбираем сервер
            server = self._select_server(server_list.servers)
            if server is None:
                raise LoginError(0xFF, f"Server with ID not found")
            logger.info(f"Selected server: {server.ip}:{server.port}")

            # Шаг 8: Отправляем RequestServerLogin
            logger.debug(f"Requesting login to server {server.id}...")
            await conn.send_packet(
                RequestServerLoginPacket(
                    login_ok1=login_ok.login_ok1,
                    login_ok2=login_ok.login_ok2,
                    server_id=server.id,
                )
            )

            # Шаг 9: Получаем PlayOk
            logger.debug("Waiting for PlayOk...")
            play_ok = await self._wait_for_packet(conn, PlayOkPacket)
            logger.info(
                f"PlayOk received: play_ok1={play_ok.play_ok1}, "
                f"play_ok2={play_ok.play_ok2}"
            )

            return LoginResult(
                server=server,
                play_ok1=play_ok.play_ok1,
                play_ok2=play_ok.play_ok2,
                login_ok1=login_ok.login_ok1,
                login_ok2=login_ok.login_ok2,
                username=self._credentials.username,
            )

        finally:
            await conn.close()

    async def _wait_for_packet(
        self, conn: LoginConnection, packet_class: type
    ) -> object:
        """Ждёт пакет определённого типа с улучшенной диагностикой.

        Args:
            conn: Соединение.
            packet_class: Ожидаемый класс пакета.

        Returns:
            Распарсенный пакет.

        Raises:
            LoginError: Если получен другой пакет.
        """
        try:
            # Читаем пакет с передачей ожидаемого опкода для диагностики
            opcode, data = await conn.read_packet(expected_opcode=packet_class.opcode)

            # Проверяем на LoginFail
            if opcode == LoginFailPacket.opcode:
                fail = LoginFailPacket(data)
                reason_desc = LOGIN_FAIL_REASONS.get(fail.reason, f"Unknown error {fail.reason}")
                logger.error(f"Login failed: {reason_desc} (code: 0x{fail.reason:02X})")
                raise LoginError(fail.reason)

            # Проверяем соответствие ожидаемому опкоду
            if opcode != packet_class.opcode:
                packet_name = packet_class.__name__ if hasattr(packet_class, '__name__') else "Unknown"

                # Детальное логирование ошибки
                error_msg = (
                    f"Packet type mismatch: expected {packet_name} (0x{packet_class.opcode:02X}), "
                    f"got opcode 0x{opcode:02X}"
                )
                logger.error(f"[LoginFlow] {error_msg}")

                # Специальная обработка для опкода 0xEE (частый признак ошибки дешифрования Init)
                if opcode == 0xEE:
                    logger.error(
                        "[LoginFlow] ERROR: Received opcode 0xEE. This usually indicates a "
                        "DECRYPTION FAILURE of the initial packet. "
                        "Static Blowfish key might be incorrect for this server."
                    )

                # Специальная обработка для опкода 0x15 (CharSelectedPacket)
                if opcode == 0x15:
                    logger.error(
                        f"[LoginFlow] CRITICAL: Received CharSelectedPacket (0x15) from Login Server! "
                        f"This indicates a serious protocol issue - Game Server packet on Login Server connection."
                    )

                    if self._packet_inspector:
                        logger.error(
                            "[LoginFlow] Potential causes: "
                            "1. Wrong server port (connecting to Game Server instead of Login Server), "
                            "2. Blowfish key mismatch causing decryption failure, "
                            "3. RSA descrambling issue, "
                            "4. Server protocol version mismatch"
                        )

                # Дополнительная диагностика с packet inspector
                if self._packet_inspector:
                    # Анализируем полученные данные
                    raw_packet = opcode.to_bytes(1, 'little') + data
                    analysis = self._packet_inspector.analyze_packet(
                        raw_data=raw_packet,
                        decrypted_data=raw_packet,
                        expected_opcode=packet_class.opcode,
                        packet_source="login"
                    )

                    issues = self._packet_inspector.detect_potential_issues(analysis)
                    if issues:
                        logger.error(f"[LoginFlow] Diagnostic issues: {'; '.join(issues)}")

                raise LoginError(0xFF, error_msg)

            # Парсим пакет
            try:
                parsed_packet = packet_class(data)
                logger.debug(f"[LoginFlow] Successfully parsed {packet_class.__name__}")
                return parsed_packet
            except Exception as parse_error:
                error_msg = f"Failed to parse {packet_class.__name__}: {parse_error}"
                logger.error(f"[LoginFlow] {error_msg}")

                # Диагностика ошибки парсинга
                if self._packet_inspector and len(data) > 0:
                    logger.error(f"[LoginFlow] Packet data: {data.hex()}")

                raise LoginError(0xFF, error_msg) from parse_error

        except LoginError:
            # Повторно поднимаем LoginError без изменений
            raise
        except Exception as e:
            # Обрабатываем неожиданные ошибки
            error_msg = f"Unexpected error while waiting for {packet_class.__name__}: {e}"
            logger.error(f"[LoginFlow] {error_msg}")
            raise LoginError(0xFF, error_msg) from e

    def _select_server(self, servers: list[GameServer]) -> GameServer | None:
        """Выбирает сервер по ID.

        Args:
            servers: Список доступных серверов.

        Returns:
            Выбранный сервер или None.
        """
        for server in servers:
            if server.id == self._server_id:
                return server
        return servers[0] if servers else None


__all__ = [
    "LoginFlow",
    "LoginResult",
    "LoginError",
    "LOGIN_FAIL_REASONS",
]
