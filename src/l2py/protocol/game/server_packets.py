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
    __slots__ = ("enabled", "xor_key", "server_id", "obfuscation_key", "result")

    def __init__(self, data: bytes) -> None:
        """Инициализирует и парсит пакет KeyPacket.

        Args:
            data: Данные пакета (без опкода).
        """
        self.result: int = 0
        self.enabled: bool = False
        self.xor_key: bytes = b""
        self.server_id: int = 0
        self.obfuscation_key: int = 0
        super().__init__(data)

    def _read(self) -> None:
        """Парсит поля пакета."""
        self.result = self._reader.read_byte()
        self.xor_key = self._reader.read_bytes(8)
        
        if self._reader.remaining() >= 4:
            self.enabled = self._reader.read_int32() != 0
            
        if self._reader.remaining() >= 4:
            self.server_id = self._reader.read_int32()
            
        if self._reader.remaining() >= 1:
            self._reader.skip(1)  # obfuscation flag
            
        if self._reader.remaining() >= 4:
            self.obfuscation_key = self._reader.read_int32()


class CharSelectionInfoPacket(ServerPacket):
    """Пакет списка персонажей (S).

    Отправляется после AuthLogin.
    Содержит информацию о всех персонажах на аккаунте.

    TODO: Уточнить опкод для High Five (0x09 или 0x13).
    """

    opcode: ClassVar[int] = 0x09  # High Five
    __slots__ = ("characters",)

    def __init__(self, data: bytes) -> None:
        """Инициализация и парсинг пакета.

        Args:
            data: Данные пакета (без опкода).
        """
        self.characters: list[CharacterInfo] = []
        super().__init__(data)

    def _read(self) -> None:
        """Парсит поля пакета (L2JMobius High Five формат)."""
        # Количество персонажей (Int, не Byte!)
        char_count = self._reader.read_int32()
        
        # Максимальное количество персонажей
        max_chars = self._reader.read_int32()
        
        # Unknown byte
        self._reader.read_byte()

        for i in range(char_count):
            name = self._reader.read_string()
            object_id = self._reader.read_int32()
            login_name = self._reader.read_string()
            session_id = self._reader.read_int32()
            clan_id = self._reader.read_int32()
            
            # Builder level
            self._reader.read_int32()
            
            sex = self._reader.read_int32()
            race = self._reader.read_int32()
            base_class_id = self._reader.read_int32()
            
            # GameServerName
            self._reader.read_int32()
            
            x = self._reader.read_int32()
            y = self._reader.read_int32()
            z = self._reader.read_int32()
            
            # HP/MP как double
            hp = self._reader.read_double()
            mp = self._reader.read_double()
            
            sp = self._reader.read_int32()
            exp = self._reader.read_int64()
            
            # High Five exp percentage
            self._reader.read_double()
            
            level = self._reader.read_int32()
            
            # Karma, PK, PVP kills
            karma = self._reader.read_int32()
            pk_kills = self._reader.read_int32()
            pvp_kills = self._reader.read_int32()
            
            # 7x int zeros
            for _ in range(7):
                self._reader.read_int32()
            
            # Paperdoll items (17 slots)
            for _ in range(17):
                self._reader.read_int32()
            
            # Hair style, color, face
            hair_style = self._reader.read_int32()
            hair_color = self._reader.read_int32()
            face = self._reader.read_int32()
            
            # Max HP/MP
            max_hp = self._reader.read_double()
            max_mp = self._reader.read_double()
            
            # Delete timer / ban status
            self._reader.read_int32()
            
            # Class ID
            class_id = self._reader.read_int32()
            
            # Active
            active = self._reader.read_int32() != 0
            
            # Enchant effect
            self._reader.read_byte()
            
            # Augmentation
            self._reader.read_int32()
            
            # Transform (0)
            self._reader.read_int32()
            
            # Pet info (5x int + 2x double)
            for _ in range(5):
                self._reader.read_int32()
            self._reader.read_double()
            self._reader.read_double()
            
            # Vitality
            vitality = self._reader.read_int32()

            char = CharacterInfo(
                name=name,
                race=race,
                class_id=class_id,
                level=level,
                sex=sex,
                x=x,
                y=y,
                z=z,
                hp=hp,
                mp=mp,
                max_hp=max_hp,
                max_mp=max_mp,
                sp=sp,
                exp=exp,
                session_id=session_id,
                clan_id=clan_id,
                karma=karma,
                pk_kills=pk_kills,
                pvp_kills=pvp_kills,
                hair_style=hair_style,
                hair_color=hair_color,
                face=face,
                vitality=vitality,
                object_id=object_id,
                active=active,
            )
            self.characters.append(char)


class CharSelectedPacket(ServerPacket):
    """Пакет выбора персонажа (S).

    Отправляется после CharacterSelect.
    Подтверждает выбор персонажа.

    TODO: Уточнить опкод для High Five (обычно 0x15).
    """

    opcode: ClassVar[int] = 0x0B  # High Five
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
        """Парсит начальные поля UserInfo по SPECIFICATION §5.3.9.

        Полные поля (paperdoll, abnormal effects и т.д.) опускаются —
        для состояния IN_GAME достаточно координат, имени и базовых атрибутов.
        """
        try:
            x = self._reader.read_int32()
            y = self._reader.read_int32()
            z = self._reader.read_int32()
            self._reader.read_int32()  # vehicleId
            object_id = self._reader.read_int32()
            name = self._reader.read_string()
            race = self._reader.read_int32()
            sex = self._reader.read_int32()
            class_id = self._reader.read_int32()
            level = self._reader.read_int32()

            self.character = CharacterInfo(
                name=name,
                race=race,
                class_id=class_id,
                level=level,
                sex=sex,
                x=x,
                y=y,
                z=z,
                object_id=object_id,
            )
        except Exception:
            pass


class NetPingRequestPacket(ServerPacket):
    """Запрос keep-alive от сервера (опкод 0xD3).

    Клиент обязан ответить NetPing (0xA8) с тем же ping_id, иначе
    сервер закроет соединение через ~60 секунд.
    """

    opcode: ClassVar[int] = 0xD3
    __slots__ = ("ping_id",)

    def __init__(self, data: bytes) -> None:
        """Инициализация и парсинг пакета."""
        self.ping_id: int = 0
        super().__init__(data)

    def _read(self) -> None:
        """Парсит поля пакета."""
        self.ping_id = self._reader.read_int32()


__all__ = [
    "KeyPacket",
    "CharSelectionInfoPacket",
    "CharSelectedPacket",
    "UserInfoPacket",
    "NetPingRequestPacket",
]
