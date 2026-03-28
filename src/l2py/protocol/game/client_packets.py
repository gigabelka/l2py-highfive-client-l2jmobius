# -*- coding: utf-8 -*-
"""Пакеты от клиента к Game Server.

Содержит пакеты, которые клиент отправляет на Game Server
в процессе входа в игровой мир.

TODO: Опкоды нужно уточнить по исходникам L2JMobius.
"""

from typing import ClassVar

from l2py.protocol.base import ClientPacket


class ProtocolVersionPacket(ClientPacket):
    """Пакет версии протокола (C).

    Первый пакет после подключения к Game Server.
    Отправляется без шифрования.

    TODO: Уточнить опкод (обычно 0x0E или без опкода).
    """

    opcode: ClassVar[int] = 0x0E  # TODO: Verify for High Five
    __slots__ = ("protocol_version",)

    # Версия протокола для High Five
    HIGH_FIVE_PROTOCOL = 267  # 0x10B

    def __init__(self, protocol_version: int = HIGH_FIVE_PROTOCOL) -> None:
        """Инициализация пакета.

        Args:
            protocol_version: Версия протокола (по умолчанию 267 для High Five).
        """
        self.protocol_version = protocol_version
        super().__init__()

    def _write(self) -> None:
        """Записывает поля пакета."""
        self._writer.write_int32(self.protocol_version)
        # TODO: Для L2JMobius могут быть дополнительные байты


class AuthLoginPacket(ClientPacket):
    """Пакет авторизации на Game Server (C).

    Содержит session keys из Login Server.

    TODO: Уточнить опкод для High Five (обычно 0x2B).
    """

    opcode: ClassVar[int] = 0x2B  # TODO: Verify for High Five
    __slots__ = ("login", "play_ok1", "play_ok2", "login_ok1", "login_ok2")

    def __init__(
        self,
        login: str,
        play_ok1: int,
        play_ok2: int,
        login_ok1: int,
        login_ok2: int,
    ) -> None:
        """Инициализация пакета.

        Args:
            login: Логин пользователя.
            play_ok1: Первый PlayOk ключ из Login Server.
            play_ok2: Второй PlayOk ключ из Login Server.
            login_ok1: Первый LoginOk ключ из Login Server.
            login_ok2: Второй LoginOk ключ из Login Server.
        """
        self.login = login
        self.play_ok1 = play_ok1
        self.play_ok2 = play_ok2
        self.login_ok1 = login_ok1
        self.login_ok2 = login_ok2
        super().__init__()

    def _write(self) -> None:
        """Записывает поля пакета."""
        self._writer.write_string(self.login)
        self._writer.write_uint32(self.play_ok2)
        self._writer.write_uint32(self.play_ok1)
        self._writer.write_uint32(self.login_ok1)
        self._writer.write_uint32(self.login_ok2)


class CharacterSelectPacket(ClientPacket):
    """Пакет выбора персонажа (C).

    Отправляется после получения списка персонажей.
    """

    opcode: ClassVar[int] = 0x12  # High Five
    __slots__ = ("slot_index",)

    def __init__(self, slot_index: int) -> None:
        """Инициализация пакета.

        Args:
            slot_index: Индекс слота персонажа (0-6).
        """
        self.slot_index = slot_index
        super().__init__()

    def _write(self) -> None:
        """Записывает поля пакета.
        
        Формат: cd (int slot, short unk1, int unk2, int unk3, int unk4)
        """
        self._writer.write_int32(self.slot_index)
        self._writer.write_int16(0)  # unk1
        self._writer.write_int32(0)  # unk2
        self._writer.write_int32(0)  # unk3
        self._writer.write_int32(0)  # unk4


class EnterWorldPacket(ClientPacket):
    """Пакет входа в мир (C).

    Финальный пакет для входа персонажа в игровой мир.

    TODO: Уточнить опкод для High Five (обычно 0x11).
    """

    opcode: ClassVar[int] = 0x11  # TODO: Verify for High Five
    __slots__ = ()

    def _write(self) -> None:
        """Записывает поля пакета."""
        # Минимальный payload (8 нулей)
        self._writer.write_bytes(b"\x00" * 8)


__all__ = [
    "ProtocolVersionPacket",
    "AuthLoginPacket",
    "CharacterSelectPacket",
    "EnterWorldPacket",
]
