# -*- coding: utf-8 -*-
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
        # GameGuard данные (16 нулей)
        self._writer.write_bytes(b"\x00" * 16)


class RequestAuthLoginPacket(ClientPacket):
    """Пакет авторизации C/0x00.

    Содержит логин и пароль, зашифрованные RSA.
    """

    opcode: ClassVar[int] = 0x00
    __slots__ = ("username", "password", "session_id", "rsa", "login_ok1", "login_ok2")

    def __init__(
        self,
        username: str,
        password: str,
        session_id: int,
        rsa: L2RSA,
        login_ok1: int = 0,
        login_ok2: int = 0,
    ) -> None:
        """Инициализация пакета.

        Args:
            username: Логин пользователя.
            password: Пароль пользователя.
            session_id: ID сессии.
            rsa: RSA-объект для шифрования.
            login_ok1: Первый ключ сессии (пока 0).
            login_ok2: Второй ключ сессии (пока 0).
        """
        self.username = username
        self.password = password
        self.session_id = session_id
        self.rsa = rsa
        self.login_ok1 = login_ok1
        self.login_ok2 = login_ok2
        super().__init__()

    def _write(self) -> None:
        """Записывает поля пакета.
        
        Формат блока для RSA-шифрования (старый метод, 128 байт):
        - [0x5E..0x6B] = username (14 байт, дополнен пробелами/нулем)
        - [0x6C..0x7B] = password (16 байт)
        """
        # Формируем 128-байтный блок для RSA-шифрования
        block = bytearray(128)

        # Имя пользователя: смещение 0x5E (94), макс 14 байт
        username_bytes = self.username.encode("ascii")[:14]
        block[0x5E : 0x5E + len(username_bytes)] = username_bytes

        # Пароль: смещение 0x6C (108), макс 16 байт
        password_bytes = self.password.encode("ascii")[:16]
        block[0x6C : 0x6C + len(password_bytes)] = password_bytes

        # RSA-шифрование
        encrypted = self.rsa.encrypt(bytes(block))

        # Записываем в пакет
        self._writer.write_bytes(encrypted)
        self._writer.write_int32(self.login_ok1)
        self._writer.write_int32(self.login_ok2)
        # GameGuard данные (8 нулей)
        self._writer.write_bytes(b"\x00" * 8)


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
        # Неизвестный байт (всегда 0x05)
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
