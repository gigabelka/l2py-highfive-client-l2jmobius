
"""Пакеты от Login Server к клиенту.

Содержит все пакеты, которые клиент получает от Login Server
в процессе авторизации.
"""

from typing import ClassVar

from l2py.models.server import GameServer
from l2py.protocol.base import ServerPacket


class InitPacket(ServerPacket):
    """Пакет инициализации S/0x00.

    Первый пакет от Login Server после подключения.
    Содержит session_id, RSA-ключ и Blowfish-ключ сессии.
    """

    opcode: ClassVar[int] = 0x00
    __slots__ = (
        "session_id",
        "protocol_version",
        "rsa_key",
        "blowfish_key",
    )

    def __init__(self, data: bytes) -> None:
        """Инициализация и парсинг пакета.

        Args:
            data: Данные пакета (без опкода).
        """
        self.session_id: int = 0
        self.protocol_version: int = 0
        self.rsa_key: bytes = b""
        self.blowfish_key: bytes = b""
        super().__init__(data)

    def _read(self) -> None:
        """Парсит поля пакета."""
        self.session_id = self._reader.read_int32()
        self.protocol_version = self._reader.read_int32()
        self.rsa_key = self._reader.read_bytes(128)

        self._reader.skip(16)
        self.blowfish_key = self._reader.read_bytes(16)



class GGAuthPacket(ServerPacket):
    """Пакет ответа GameGuard S/0x0b.

    Ответ на AuthGameGuard от клиента.
    """

    opcode: ClassVar[int] = 0x0B
    __slots__ = ("response",)

    def __init__(self, data: bytes) -> None:
        """Инициализация и парсинг пакета.

        Args:
            data: Данные пакета (без опкода).
        """
        self.response: int = 0
        super().__init__(data)

    def _read(self) -> None:
        """Парсит поля пакета."""
        self.response = self._reader.read_int32()


class LoginOkPacket(ServerPacket):
    """Пакет успешной авторизации S/0x03.

    Отправляется после успешного логина.
    Содержит session keys для дальнейших операций.
    """

    opcode: ClassVar[int] = 0x03
    __slots__ = ("login_ok1", "login_ok2")

    def __init__(self, data: bytes) -> None:
        """Инициализация и парсинг пакета.

        Args:
            data: Данные пакета (без опкода).
        """
        self.login_ok1: int = 0
        self.login_ok2: int = 0
        super().__init__(data)

    def _read(self) -> None:
        """Парсит поля пакета."""
        self.login_ok1 = self._reader.read_int32()
        self.login_ok2 = self._reader.read_int32()


class ServerListPacket(ServerPacket):
    """Пакет списка серверов S/0x04.

    Содержит информацию о доступных игровых серверах.
    """

    opcode: ClassVar[int] = 0x04
    __slots__ = ("servers", "last_server")

    def __init__(self, data: bytes) -> None:
        """Инициализация и парсинг пакета.

        Args:
            data: Данные пакета (без опкода).
        """
        self.servers: list[GameServer] = []
        self.last_server: int = 0
        super().__init__(data)

    def _read(self) -> None:
        """Парсит поля пакета."""
        count = self._reader.read_byte()
        self.last_server = self._reader.read_byte()

        for _ in range(count):
            server_id = self._reader.read_byte()


            ip_bytes = self._reader.read_bytes(4)
            ip = f"{ip_bytes[0]}.{ip_bytes[1]}.{ip_bytes[2]}.{ip_bytes[3]}"

            port = self._reader.read_int32()
            age_limit = self._reader.read_byte() != 0
            is_pvp = self._reader.read_byte() != 0
            online = self._reader.read_uint16()
            max_online = self._reader.read_uint16()
            status = self._reader.read_byte() != 0


            server = GameServer(
                id=server_id,
                ip=ip,
                port=port,
                online=online,
                max_online=max_online,
                status=status,
                is_pvp=is_pvp,
                age_limit=age_limit,
            )
            self.servers.append(server)



            if self._reader.remaining() >= 7:
                self._reader.skip(7)


class PlayOkPacket(ServerPacket):
    """Пакет подтверждения выбора сервера S/0x07.

    Отправляется после выбора сервера.
    Содержит keys для подключения к Game Server.
    """

    opcode: ClassVar[int] = 0x07
    __slots__ = ("play_ok1", "play_ok2")

    def __init__(self, data: bytes) -> None:
        """Инициализация и парсинг пакета.

        Args:
            data: Данные пакета (без опкода).
        """
        self.play_ok1: int = 0
        self.play_ok2: int = 0
        super().__init__(data)

    def _read(self) -> None:
        """Парсит поля пакета."""
        self.play_ok1 = self._reader.read_int32()
        self.play_ok2 = self._reader.read_int32()


class LoginFailPacket(ServerPacket):
    """Пакет ошибки авторизации S/0x01.

    Отправляется при неудачной попытке входа.
    """

    opcode: ClassVar[int] = 0x01
    __slots__ = ("reason",)

    def __init__(self, data: bytes) -> None:
        """Инициализация и парсинг пакета.

        Args:
            data: Данные пакета (без опкода).
        """
        self.reason: int = 0
        super().__init__(data)

    def _read(self) -> None:
        """Парсит поля пакета."""
        self.reason = self._reader.read_byte()


__all__ = [
    "InitPacket",
    "GGAuthPacket",
    "LoginOkPacket",
    "ServerListPacket",
    "PlayOkPacket",
    "LoginFailPacket",
]
