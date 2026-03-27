# -*- coding: utf-8 -*-
"""Пакеты от Game Server к клиенту.

Содержит пакеты, которые клиент получает от Game Server
в процессе входа в игровой мир.

TODO: Опкоды нужно уточнить по исходникам L2JMobius.
"""

from typing import ClassVar

from l2py.models.character import CharacterInfo
from l2py.protocol.base import ServerPacket


class KeyPacket(ServerPacket):
    """Пакет с XOR-ключом (S).

    Отправляется после ProtocolVersion.
    Содержит динамическую часть XOR-ключа для шифрования.

    TODO: Уточнить опкод для High Five.
    """

    opcode: ClassVar[int] = 0x2E  # TODO: Verify for High Five
    __slots__ = ("enabled", "xor_key", "server_id", "obfuscation_key")

    def __init__(self, data: bytes) -> None:
        """Инициализация и парсинг пакета.

        Args:
            data: Данные пакета (без опкода).
        """
        self.enabled: bool = False
        self.xor_key: bytes = b""
        self.server_id: int = 0
        self.obfuscation_key: int = 0
        super().__init__(data)

    def _read(self) -> None:
        """Парсит поля пакета."""
        # Первая версия парсинга (может отличаться для L2JMobius)
        self.enabled = self._reader.read_byte() != 0
        self.xor_key = self._reader.read_bytes(8)
        # Пропускаем промежуточные поля если есть
        if self._reader.remaining() >= 4:
            self._reader.skip(4)  # Unknown
        if self._reader.remaining() >= 4:
            self.server_id = self._reader.read_int32()
        if self._reader.remaining() >= 4:
            self.obfuscation_key = self._reader.read_int32()


class CharSelectionInfoPacket(ServerPacket):
    """Пакет списка персонажей (S).

    Отправляется после AuthLogin.
    Содержит информацию о всех персонажах на аккаунте.

    TODO: Уточнить опкод для High Five (0x09 или 0x13).
    """

    opcode: ClassVar[int] = 0x13  # TODO: Verify for High Five (0x09 или 0x13)
    __slots__ = ("characters",)

    def __init__(self, data: bytes) -> None:
        """Инициализация и парсинг пакета.

        Args:
            data: Данные пакета (без опкода).
        """
        self.characters: list[CharacterInfo] = []
        super().__init__(data)

    def _read(self) -> None:
        """Парсит поля пакета."""
        # Количество персонажей
        char_count = self._reader.read_byte()

        for _ in range(char_count):
            name = self._reader.read_string()
            login = self._reader.read_string()
            session_id = self._reader.read_int32()
            clan_id = self._reader.read_int32()

            # Пропускаем constructType и other data
            self._reader.skip(4)  # constructType

            sex = self._reader.read_int32()
            race = self._reader.read_int32()
            base_class_id = self._reader.read_int32()

            # Active (1 = active, 0 = inactive)
            active = self._reader.read_byte() != 0

            # Пропускаем x, y, z (3 * 4 байта)
            x = self._reader.read_int32()
            y = self._reader.read_int32()
            z = self._reader.read_int32()

            # HP/MP (float)
            hp = self._reader.read_float()
            mp = self._reader.read_float()

            sp = self._reader.read_int32()
            exp = self._reader.read_int64()
            level = self._reader.read_int32()

            # Karma и другие поля пропускаем
            # TODO: Допарсить оставшиеся поля для полной структуры

            char = CharacterInfo(
                name=name,
                race=race,
                class_id=base_class_id,
                level=level,
                sex=sex,
                x=x,
                y=y,
                z=z,
                hp=hp,
                mp=mp,
                sp=sp,
                exp=exp,
                session_id=session_id,
                clan_id=clan_id,
            )
            self.characters.append(char)


class CharSelectedPacket(ServerPacket):
    """Пакет выбора персонажа (S).

    Отправляется после CharacterSelect.
    Подтверждает выбор персонажа.

    TODO: Уточнить опкод для High Five (обычно 0x15).
    """

    opcode: ClassVar[int] = 0x15  # TODO: Verify for High Five
    __slots__ = (
        "name",
        "session_id",
        "clan_id",
        "sex",
        "race",
        "class_id",
        "x",
        "y",
        "z",
    )

    def __init__(self, data: bytes) -> None:
        """Инициализация и парсинг пакета.

        Args:
            data: Данные пакета (без опкода).
        """
        self.name: str = ""
        self.session_id: int = 0
        self.clan_id: int = 0
        self.sex: int = 0
        self.race: int = 0
        self.class_id: int = 0
        self.x: int = 0
        self.y: int = 0
        self.z: int = 0
        super().__init__(data)

    def _read(self) -> None:
        """Парсит поля пакета."""
        self.name = self._reader.read_string()
        self.session_id = self._reader.read_int32()
        self.clan_id = self._reader.read_int32()
        self._reader.skip(4)  # Unknown
        self.sex = self._reader.read_int32()
        self.race = self._reader.read_int32()
        self.class_id = self._reader.read_int32()
        self._reader.skip(4)  # Unknown (active?)
        self.x = self._reader.read_int32()
        self.y = self._reader.read_int32()
        self.z = self._reader.read_int32()
        # Остальные поля пропускаем (HP, MP и т.д.)


class UserInfoPacket(ServerPacket):
    """Пакет информации о пользователе (S).

    Отправляется после EnterWorld.
    Содержит полную информацию о персонаже в мире.

    TODO: Уточнить опкод для High Five.
    High Five использует inner opcode (обычно 0x04 внутри 0x32).
    """

    opcode: ClassVar[int] = 0x32  # TODO: Verify for High Five
    __slots__ = ("character",)

    def __init__(self, data: bytes) -> None:
        """Инициализация и парсинг пакета.

        Args:
            data: Данные пакета (без опкода).
        """
        self.character: CharacterInfo | None = None
        super().__init__(data)

    def _read(self) -> None:
        """Парсит поля пакета.

        TODO: Допарсить оставшиеся поля для полной структуры UserInfo.
        """
        # В High Five UserInfo имеет внутренний опкод
        # inner_opcode = self._reader.read_byte()

        # Парсим основные поля
        # TODO: Реализовать полный парсинг для High Five

        # Пока заглушка - парсим только имя
        try:
            name = self._reader.read_string()
            self.character = CharacterInfo(
                name=name,
                race=0,
                class_id=0,
                level=0,
                sex=0,
            )
        except Exception:
            # Если не получилось распарсить - оставляем None
            pass


__all__ = [
    "KeyPacket",
    "CharSelectionInfoPacket",
    "CharSelectedPacket",
    "UserInfoPacket",
]
