
"""Оркестрация входа в игровой мир.

Реализует полный flow от подключения к Game Server
до получения UserInfo (персонаж в игре).
"""

import asyncio
import logging
from dataclasses import dataclass, field
from typing import TYPE_CHECKING

from l2py.crypto.game_crypt import GameCrypt

if TYPE_CHECKING:
    from l2py.events import EventEmitter
from l2py.models.character import CharacterInfo
from l2py.network.game_connection import GameConnection
from l2py.network.login_flow import LoginResult
from l2py.protocol.game.client_packets import (
    AuthLoginPacket,
    CharacterSelectPacket,
    EnterWorldPacket,
    NetPingPacket,
    ProtocolVersionPacket,
    RequestKeyMappingPacket,
)
from l2py.protocol.game.server_packets import (
    CharSelectedPacket,
    CharSelectionInfoPacket,
    KeyPacket,
    NetPingRequestPacket,
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
        super().__init__(message)


@dataclass
class GameSession:
    """Сессия игрового мира.

    Содержит активное соединение и информацию о персонаже.
    """

    connection: GameConnection
    character: CharacterInfo
    session_id: int
    _reader_task: asyncio.Task | None = field(default=None, repr=False)
    emitter: "EventEmitter | None" = field(default=None, repr=False)

    async def run_keepalive(self) -> None:
        """Читает пакеты в цикле и отвечает на NetPingRequest.

        Если задан `emitter`, на каждый входящий пакет эмитится
        `PacketReceivedEvent` — это канал для внешних потребителей (например, API).

        Завершается при закрытии соединения. Предназначен для удержания
        сессии «в игре» — без ответа на ping сервер разрывает соединение.
        """
        from l2py.events import PacketReceivedEvent

        while True:
            try:
                opcode, data = await self.connection.read_packet()
            except (ConnectionError, asyncio.IncompleteReadError):
                logger.info("Game connection closed, stopping keepalive loop")
                return

            if self.emitter is not None:
                try:
                    await self.emitter.emit(
                        PacketReceivedEvent(opcode=opcode, data=data, source="game")
                    )
                except Exception:
                    logger.exception("Error while emitting PacketReceivedEvent")

            if opcode == NetPingRequestPacket.opcode:
                ping = NetPingRequestPacket(data)
                logger.debug(f"NetPingRequest pingId={ping.ping_id}")
                try:
                    await self.connection.send_packet(NetPingPacket(ping.ping_id))
                except ConnectionError:
                    logger.info("Game connection closed while answering ping")
                    return
            else:
                logger.debug(
                    f"Unhandled in-game packet: opcode=0x{opcode:02X}, "
                    f"len={len(data)}"
                )


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

    __slots__ = ("_login_result", "_char_slot", "_debug_packets")

    def __init__(self, login_result: LoginResult, char_slot: int = 0, debug_packets: bool = False) -> None:
        """Инициализация flow.

        Args:
            login_result: Результат авторизации на Login Server.
            char_slot: Индекс слота персонажа (0-6).
            debug_packets: Включить отладку пакетов.
        """
        self._login_result = login_result
        self._char_slot = char_slot
        self._debug_packets = debug_packets

    async def execute(self) -> GameSession:
        """Выполняет полный процесс входа в мир.

        Returns:
            Игровая сессия с активным соединением.

        Raises:
            GameError: Если вход не удался.
            ConnectionError: Если проблемы с соединением.
        """

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


            logger.debug("Sending ProtocolVersion...")
            await conn.send_packet(
                ProtocolVersionPacket(),
                raw=True,
            )


            logger.debug("Waiting for KeyPacket...")
            key_packet = await self._wait_for_packet(conn, KeyPacket)
            logger.debug(f"Received KeyPacket: enabled={key_packet.enabled}")
            if key_packet.enabled:
                logger.debug(f"KeyPacket xor_key: {key_packet.xor_key.hex()}")


            if key_packet.enabled:
                crypt.set_key(key_packet.xor_key)
                logger.debug(f"Encryption enabled, full key: {crypt._decrypt_key.hex()}")


            logger.debug("Sending AuthLogin...")
            auth_packet = AuthLoginPacket(
                login=self._login_result.username,
                play_ok1=self._login_result.play_ok1,
                play_ok2=self._login_result.play_ok2,
                login_ok1=self._login_result.login_ok1,
                login_ok2=self._login_result.login_ok2,
            )
            auth_bytes = auth_packet.to_bytes()
            logger.debug(f"AuthLogin raw bytes: {auth_bytes.hex()}")
            logger.debug(f"Key before send: {crypt._encrypt_key.hex() if crypt._encrypt_key else 'not set'}")
            await conn.send_packet(auth_packet)
            logger.debug(f"Key after send: {crypt._encrypt_key.hex() if crypt._encrypt_key else 'not set'}")


            logger.debug("Waiting for CharSelectionInfo...")
            try:
                char_info = await self._wait_for_packet(conn, CharSelectionInfoPacket)
                logger.debug(f"Received {len(char_info.characters)} characters")
            except asyncio.TimeoutError:
                raise GameError(
                    "Game Server did not respond. "
                    "Check Game <-> Login Server connection configuration."
                )


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


            logger.debug(f"Sending CharacterSelect (slot {self._char_slot})...")
            await conn.send_packet(CharacterSelectPacket(self._char_slot))





            logger.debug("Waiting for CharSelected or UserInfo...")
            user_info: UserInfoPacket | None = None
            session_id = selected_char.session_id

            while True:
                opcode, data = await conn.read_packet()
                logger.debug(f"Received opcode=0x{opcode:02X}, len={len(data)}")

                if opcode == CharSelectedPacket.opcode:
                    char_selected = CharSelectedPacket(data)
                    logger.debug(f"CharSelected: {char_selected.name}")
                    session_id = char_selected.session_id
                    break
                if opcode == UserInfoPacket.opcode:
                    logger.debug("Server skipped CharSelected, got UserInfo directly")
                    user_info = UserInfoPacket(data)
                    break
                logger.debug(
                    f"Skipping intermediate packet 0x{opcode:02X} "
                    f"while waiting for CharSelected"
                )


            logger.debug("Sending RequestKeyMapping...")
            await conn.send_packet(RequestKeyMappingPacket())


            logger.debug("Sending EnterWorld...")
            await conn.send_packet(EnterWorldPacket())




            if user_info is None:
                logger.debug("Waiting for UserInfo...")
                while True:
                    opcode, data = await conn.read_packet()
                    logger.debug(f"Received opcode=0x{opcode:02X}, len={len(data)}")
                    if opcode == UserInfoPacket.opcode:
                        user_info = UserInfoPacket(data)
                        break
                    logger.debug(
                        f"Skipping intermediate packet 0x{opcode:02X} "
                        f"while waiting for UserInfo"
                    )

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
                session_id=session_id,
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
        logger.debug(f"Received raw packet: opcode=0x{opcode:02X}, data={data.hex()}")

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
