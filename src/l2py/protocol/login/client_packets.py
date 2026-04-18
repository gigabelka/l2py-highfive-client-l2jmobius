
"""Пакеты от клиента к Login Server.

Содержит все пакеты, которые клиент отправляет на Login Server
в процессе авторизации.
"""

from typing import ClassVar

from l2py.crypto.rsa import L2RSA
from l2py.protocol.base import ClientPacket


class AuthGameGuardPacket(ClientPacket):
    """Пакет подтверждения GameGuard C/0x07.

    Первый пакет клиента после получения Init.
    """

    opcode: ClassVar[int] = 0x07
    __slots__ = ("session_id",)

    def __init__(self, session_id: int) -> None:
        """Инициализация пакета.

        Args:
            session_id: ID сессии из Init пакета.
        """
        self.session_id = session_id
        super().__init__()

    def _write(self) -> None:
        """Записывает поля пакета."""
        self._writer.write_int32(self.session_id)

        self._writer.write_bytes(b"\x00" * 16)


class RequestAuthLoginPacket(ClientPacket):
    """Пакет авторизации C/0x00.

    Содержит логин и пароль, зашифрованные RSA, плюс sessionId и нулевой
    GameGuard-блок. Полный формат — см. SPECIFICATION.md §4.10 (тело 184 байта).
    """

    opcode: ClassVar[int] = 0x00
    __slots__ = ("username", "password", "session_id", "rsa")

    def __init__(
        self,
        username: str,
        password: str,
        session_id: int,
        rsa: L2RSA,
    ) -> None:
        """Инициализация пакета.

        Args:
            username: Логин пользователя.
            password: Пароль пользователя.
            session_id: ID сессии (echoed из Init).
            rsa: RSA-объект для шифрования.
        """
        self.username = username
        self.password = password
        self.session_id = session_id
        self.rsa = rsa
        super().__init__()

    def _write(self) -> None:
        """Записывает поля пакета.

        Формат блока для RSA-шифрования (128 байт):
        - [0x5E..0x6B] = username (14 байт, ASCII, null-padded)
        - [0x6C..0x7B] = password (16 байт, ASCII, null-padded)

        Тело пакета — 184 байта по SPECIFICATION.md §4.10:
        opcode(1) + RSA(128) + sessionId(4) + reserved(16) + 0x08(4) +
        reserved(3) + GG nonce(16) + reserved(4) + GG digest(4) + reserved(4).
        L2J Mobius CT 2.6 принимает GameGuard-поля заполненными нулями.
        """

        block = bytearray(128)

        username_bytes = self.username.encode("ascii")[:14]
        block[0x5E : 0x5E + len(username_bytes)] = username_bytes

        password_bytes = self.password.encode("ascii")[:16]
        block[0x6C : 0x6C + len(password_bytes)] = password_bytes

        encrypted = self.rsa.encrypt(bytes(block))

        self._writer.write_bytes(encrypted)
        self._writer.write_int32(self.session_id)
        self._writer.write_bytes(b"\x00" * 16)
        self._writer.write_int32(0x00000008)
        self._writer.write_bytes(b"\x00" * 3)
        self._writer.write_bytes(b"\x00" * 16)
        self._writer.write_bytes(b"\x00" * 4)
        self._writer.write_int32(0)
        self._writer.write_bytes(b"\x00" * 4)


class RequestServerListPacket(ClientPacket):
    """Пакет запроса списка серверов C/0x05."""

    opcode: ClassVar[int] = 0x05
    __slots__ = ("login_ok1", "login_ok2")

    def __init__(self, login_ok1: int, login_ok2: int) -> None:
        """Инициализация пакета.

        Args:
            login_ok1: Первый ключ сессии из LoginOk.
            login_ok2: Второй ключ сессии из LoginOk.
        """
        self.login_ok1 = login_ok1
        self.login_ok2 = login_ok2
        super().__init__()

    def _write(self) -> None:
        """Записывает поля пакета."""
        self._writer.write_uint32(self.login_ok1)
        self._writer.write_uint32(self.login_ok2)

        self._writer.write_byte(0x05)


class RequestServerLoginPacket(ClientPacket):
    """Пакет выбора сервера C/0x02."""

    opcode: ClassVar[int] = 0x02
    __slots__ = ("login_ok1", "login_ok2", "server_id")

    def __init__(self, login_ok1: int, login_ok2: int, server_id: int) -> None:
        """Инициализация пакета.

        Args:
            login_ok1: Первый ключ сессии из LoginOk.
            login_ok2: Второй ключ сессии из LoginOk.
            server_id: ID выбранного сервера.
        """
        self.login_ok1 = login_ok1
        self.login_ok2 = login_ok2
        self.server_id = server_id
        super().__init__()

    def _write(self) -> None:
        """Записывает поля пакета."""
        self._writer.write_uint32(self.login_ok1)
        self._writer.write_uint32(self.login_ok2)
        self._writer.write_byte(self.server_id)


__all__ = [
    "AuthGameGuardPacket",
    "RequestAuthLoginPacket",
    "RequestServerListPacket",
    "RequestServerLoginPacket",
]
