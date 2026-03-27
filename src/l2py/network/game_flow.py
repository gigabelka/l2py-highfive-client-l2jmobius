# -*- coding: utf-8 -*-
"""Оркестрация входа в игровой мир.

Реализует полный flow от подключения к Game Server
до получения UserInfo (персонаж в игре).
"""

import logging
from dataclasses import dataclass

from l2py.crypto.game_crypt import GameCrypt
from l2py.models.character import CharacterInfo
from l2py.network.game_connection import GameConnection
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

logger = logging.getLogger(__name__)


class GameError(Exception):
    """Ошибка входа в игру."""

    def __init__(self, message: str) -> None:
        """Инициализация ошибки.

        Args:
            message: Сообщение об ошибке.
        """
        super().__init__(f"Game flow failed: {message}")


@dataclass
class GameSession:
    """Сессия игрового мира.

    Содержит активное соединение и информацию о персонаже.
    """

    connection: GameConnection
    character: CharacterInfo
    session_id: int


class GameFlow:
    """Оркестрирует вход персонажа в игровой мир.

    Реализует следующий flow:
    1. Подключение к Game Server
    2. Отправка ProtocolVersion (без шифрования)
    3. Получение KeyPacket (XOR-ключ)
    4. Отправка AuthLogin (с session keys)
    5. Получение списка персонажей
    6. Выбор персонажа
    7. Получение подтверждения выбора
    8. Отправка EnterWorld
    9. Получение UserInfo (персонаж в игре)
    """

    __slots__ = ("_login_result", "_char_slot")

    def __init__(self, login_result: LoginResult, char_slot: int = 0) -> None:
        """Инициализация flow.

        Args:
            login_result: Результат авторизации на Login Server.
            char_slot: Индекс слота персонажа (0-6).
        """
        self._login_result = login_result
        self._char_slot = char_slot

    async def execute(self) -> GameSession:
        """Выполняет полный процесс входа в мир.

        Returns:
            Игровая сессия с активным соединением.

        Raises:
            GameError: Если вход не удался.
            ConnectionError: Если проблемы с соединением.
        """
        # Создаём криптографию и соединение
        crypt = GameCrypt()
        conn = GameConnection(
            self._login_result.server.ip,
            self._login_result.server.port,
            crypt,
        )

        try:
            await conn.connect()
            logger.info(
                f"Starting game flow for user: {self._login_result.username}, "
                f"server: {self._login_result.server.ip}:{self._login_result.server.port}"
            )

            # Шаг 1: Отправляем ProtocolVersion (не шифруется)
            logger.debug("Sending ProtocolVersion...")
            await conn.send_packet(
                ProtocolVersionPacket(),
                raw=True,
            )

            # Шаг 2: Получаем KeyPacket
            logger.debug("Waiting for KeyPacket...")
            key_packet = await self._wait_for_packet(conn, KeyPacket)
            logger.debug(f"Received KeyPacket: enabled={key_packet.enabled}")

            # Включаем шифрование
            if key_packet.enabled:
                crypt.set_key(key_packet.xor_key)
                logger.debug("Encryption enabled")

            # Шаг 3: Отправляем AuthLogin
            logger.debug("Sending AuthLogin...")
            await conn.send_packet(
                AuthLoginPacket(
                    login=self._login_result.username,
                    play_ok1=self._login_result.play_ok1,
                    play_ok2=self._login_result.play_ok2,
                    login_ok1=self._login_result.login_ok1,
                    login_ok2=self._login_result.login_ok2,
                )
            )

            # Шаг 4: Получаем список персонажей
            logger.debug("Waiting for CharSelectionInfo...")
            char_info = await self._wait_for_packet(conn, CharSelectionInfoPacket)
            logger.debug(f"Received {len(char_info.characters)} characters")

            # Выбираем персонажа
            if not char_info.characters:
                raise GameError("No characters on account")

            if self._char_slot >= len(char_info.characters):
                logger.warning(
                    f"Character slot {self._char_slot} not available, using slot 0"
                )
                self._char_slot = 0

            selected_char = char_info.characters[self._char_slot]
            logger.info(
                f"Selected character: {selected_char.name} (level {selected_char.level})"
            )

            # Шаг 5: Отправляем CharacterSelect
            logger.debug(f"Sending CharacterSelect (slot {self._char_slot})...")
            await conn.send_packet(CharacterSelectPacket(self._char_slot))

            # Шаг 6: Получаем подтверждение
            logger.debug("Waiting for CharSelected...")
            char_selected = await self._wait_for_packet(conn, CharSelectedPacket)
            logger.debug(f"CharSelected: {char_selected.name}")

            # Шаг 7: Отправляем EnterWorld
            logger.debug("Sending EnterWorld...")
            await conn.send_packet(EnterWorldPacket())

            # Шаг 8: Получаем UserInfo
            logger.debug("Waiting for UserInfo...")
            user_info = await self._wait_for_packet(conn, UserInfoPacket)

            if user_info.character is None:
                raise GameError("Failed to parse UserInfo")

            character = user_info.character
            logger.info(
                f"Entered world: {character.name}, level {character.level}, "
                f"coords=({character.x}, {character.y}, {character.z})"
            )

            return GameSession(
                connection=conn,
                character=character,
                session_id=char_selected.session_id,
            )

        except Exception:
            await conn.close()
            raise

    async def _wait_for_packet(
        self, conn: GameConnection, packet_class: type
    ) -> object:
        """Ждёт пакет определённого типа.

        Args:
            conn: Соединение.
            packet_class: Ожидаемый класс пакета.

        Returns:
            Распарсенный пакет.

        Raises:
            GameError: Если получен другой пакет.
        """
        opcode, data = await conn.read_packet()

        if opcode != packet_class.opcode:
            raise GameError(
                f"Expected packet 0x{packet_class.opcode:02X}, "
                f"got 0x{opcode:02X}"
            )

        return packet_class(data)


__all__ = [
    "GameFlow",
    "GameSession",
    "GameError",
]
