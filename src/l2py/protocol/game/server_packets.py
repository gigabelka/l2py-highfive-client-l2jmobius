
"""Пакеты от Game Server к клиенту.

Содержит пакеты, которые клиент получает от Game Server
в процессе входа в игровой мир.

TODO: Опкоды нужно уточнить по исходникам L2JMobius.
"""

from typing import ClassVar

from l2py.models.character import CharacterInfo
from l2py.protocol.base import PacketReader, ServerPacket


class KeyPacket(ServerPacket):
    """Пакет с XOR-ключом (S).

    Отправляется после ProtocolVersion.
    Содержит динамическую часть XOR-ключа для шифрования.

    TODO: Уточнить опкод для High Five.
    """

    opcode: ClassVar[int] = 0x2E
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
            self._reader.skip(1)

        if self._reader.remaining() >= 4:
            self.obfuscation_key = self._reader.read_int32()


class CharSelectionInfoPacket(ServerPacket):
    """Пакет списка персонажей (S).

    Отправляется после AuthLogin.
    Содержит информацию о всех персонажах на аккаунте.

    TODO: Уточнить опкод для High Five (0x09 или 0x13).
    """

    opcode: ClassVar[int] = 0x09
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

        char_count = self._reader.read_int32()


        max_chars = self._reader.read_int32()


        self._reader.read_byte()

        for i in range(char_count):
            name = self._reader.read_string()
            object_id = self._reader.read_int32()
            login_name = self._reader.read_string()
            session_id = self._reader.read_int32()
            clan_id = self._reader.read_int32()


            self._reader.read_int32()

            sex = self._reader.read_int32()
            race = self._reader.read_int32()
            base_class_id = self._reader.read_int32()


            self._reader.read_int32()

            x = self._reader.read_int32()
            y = self._reader.read_int32()
            z = self._reader.read_int32()


            hp = self._reader.read_double()
            mp = self._reader.read_double()

            sp = self._reader.read_int32()
            exp = self._reader.read_int64()


            self._reader.read_double()

            level = self._reader.read_int32()


            karma = self._reader.read_int32()
            pk_kills = self._reader.read_int32()
            pvp_kills = self._reader.read_int32()


            for _ in range(7):
                self._reader.read_int32()


            for _ in range(17):
                self._reader.read_int32()


            hair_style = self._reader.read_int32()
            hair_color = self._reader.read_int32()
            face = self._reader.read_int32()


            max_hp = self._reader.read_double()
            max_mp = self._reader.read_double()


            self._reader.read_int32()


            class_id = self._reader.read_int32()


            active = self._reader.read_int32() != 0


            self._reader.read_byte()


            self._reader.read_int32()


            self._reader.read_int32()


            for _ in range(5):
                self._reader.read_int32()
            self._reader.read_double()
            self._reader.read_double()


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

    opcode: ClassVar[int] = 0x0B
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
        self._reader.skip(4)
        self.sex = self._reader.read_int32()
        self.race = self._reader.read_int32()
        self.class_id = self._reader.read_int32()
        self._reader.skip(4)
        self.x = self._reader.read_int32()
        self.y = self._reader.read_int32()
        self.z = self._reader.read_int32()



class UserInfoPacket(ServerPacket):
    """UserInfo (S→C, opcode 0x32).

    Парсит документированный префикс HighFive (см. docs/PROTOCOL.md §UserInfo):
    координаты, heading, objectId, name, race/sex/class/level, exp, STR..MEN,
    maxHp/curHp, maxMp/curMp, sp, curLoad/maxLoad. Хвост (paperdoll, combat stats,
    speeds, title, clan, abnormals, vitality) не парсится детально — его точный
    layout зависит от сборки, поэтому после префикса поля не читаются, а остаток
    сохраняется в `raw_tail` для отладки.
    """

    opcode: ClassVar[int] = 0x32
    __slots__ = (
        "character",
        "x", "y", "z", "heading", "object_id", "name",
        "race", "sex", "class_id", "level",
        "exp",
        "str_", "dex", "con", "int_", "wit", "men",
        "max_hp", "cur_hp", "max_mp", "cur_mp",
        "sp", "cur_load", "max_load",
        "active_weapon_item",
        "raw_tail",
    )

    def __init__(self, data: bytes) -> None:
        self.character: CharacterInfo | None = None
        self.x = 0
        self.y = 0
        self.z = 0
        self.heading = 0
        self.object_id = 0
        self.name = ""
        self.race = 0
        self.sex = 0
        self.class_id = 0
        self.level = 0
        self.exp = 0
        self.str_ = 0
        self.dex = 0
        self.con = 0
        self.int_ = 0
        self.wit = 0
        self.men = 0
        self.max_hp = 0
        self.cur_hp = 0
        self.max_mp = 0
        self.cur_mp = 0
        self.sp = 0
        self.cur_load = 0
        self.max_load = 0
        self.active_weapon_item = 0
        self.raw_tail = b""
        super().__init__(data)

    def _read(self) -> None:
        r = self._reader
        try:
            self.x = r.read_int32()
            self.y = r.read_int32()
            self.z = r.read_int32()
            self.heading = r.read_int32()
            self.object_id = r.read_int32()
            self.name = r.read_string()
            self.race = r.read_int32()
            self.sex = r.read_int32()
            self.class_id = r.read_int32()
            self.level = r.read_int32()
            self.exp = r.read_int64()
            self.str_ = r.read_int32()
            self.dex = r.read_int32()
            self.con = r.read_int32()
            self.int_ = r.read_int32()
            self.wit = r.read_int32()
            self.men = r.read_int32()
            self.max_hp = r.read_int32()
            self.cur_hp = r.read_int32()
            self.max_mp = r.read_int32()
            self.cur_mp = r.read_int32()
            self.sp = r.read_int32()
            self.cur_load = r.read_int32()
            self.max_load = r.read_int32()
            self.active_weapon_item = r.read_int32()
        except Exception:
            pass

        self.character = CharacterInfo(
            name=self.name,
            race=self.race,
            class_id=self.class_id,
            level=self.level,
            sex=self.sex,
            x=self.x,
            y=self.y,
            z=self.z,
            hp=float(self.cur_hp),
            mp=float(self.cur_mp),
            max_hp=float(self.max_hp),
            max_mp=float(self.max_mp),
            sp=self.sp,
            exp=self.exp,
            object_id=self.object_id,
        )

        try:
            self.raw_tail = r.read_bytes(r.remaining())
        except Exception:
            self.raw_tail = b""


class NetPingRequestPacket(ServerPacket):
    """Запрос keep-alive от сервера (опкод 0xD9, CT 2.6 HighFive).

    На CT 2.6 HighFive `0xD3 = EARTHQUAKE`, ping-request перенесён на `0xD9`.
    Клиент обязан ответить NetPing (0xB1) с тем же ping_id, иначе сервер
    закроет соединение через ~60 секунд.
    """

    opcode: ClassVar[int] = 0xD9
    __slots__ = ("ping_id",)

    def __init__(self, data: bytes) -> None:
        """Инициализация и парсинг пакета."""
        self.ping_id: int = 0
        super().__init__(data)

    def _read(self) -> None:
        """Парсит поля пакета."""
        self.ping_id = self._reader.read_int32()


class MyTargetSelectedPacket(ServerPacket):
    """MyTargetSelected (S→C, opcode 0xB9 на L2JMobius HighFive).

    На L2JMobius HighFive сервер шлёт подтверждение выбора цели с опкодом
    0xB9 (а не 0xA6, как в «каноническом» HighFive-протоколе / docs/ACTIONS.md §1).
    Body: i32 object_id, i32 color_distance, [u16 tail].
    """

    opcode: ClassVar[int] = 0xB9
    __slots__ = ("object_id", "color_distance")

    def __init__(self, data: bytes) -> None:
        self.object_id: int = 0
        self.color_distance: int = 0
        super().__init__(data)

    def _read(self) -> None:
        self.object_id = self._reader.read_int32()
        if self._reader.remaining() >= 4:
            self.color_distance = self._reader.read_int32()


class ShortCutInitPacket(ServerPacket):
    """ShortCutInit (S→C, opcode 0x45): начальная раскладка action-bar.

    Body: `i32 count` + `count` записей по 5×i32: `type, slot, id, level, characterType`.
    `slot` закодирован как `slot + page*12` (0..119). См. docs/ACTIONS.md §10.4.
    """

    opcode: ClassVar[int] = 0x45
    __slots__ = ("entries",)

    def __init__(self, data: bytes) -> None:
        self.entries: list[tuple[int, int, int, int]] = []
        super().__init__(data)

    def _read(self) -> None:
        count = self._reader.read_int32()
        for _ in range(count):
            if self._reader.remaining() < 20:
                break
            sc_type = self._reader.read_int32()
            slot = self._reader.read_int32()
            sc_id = self._reader.read_int32()
            level = self._reader.read_int32()
            self._reader.read_int32()  # characterType
            self.entries.append((sc_type, slot, sc_id, level))


class ShortCutRegisterPacket(ServerPacket):
    """ShortCutRegister (S→C, opcode 0x44): одна запись action-bar.

    Body: `type, slot, id, level, characterType` — 5×i32. См. docs/ACTIONS.md §10.2.
    """

    opcode: ClassVar[int] = 0x44
    __slots__ = ("type", "slot", "id", "level")

    def __init__(self, data: bytes) -> None:
        self.type: int = 0
        self.slot: int = 0
        self.id: int = 0
        self.level: int = 0
        super().__init__(data)

    def _read(self) -> None:
        self.type = self._reader.read_int32()
        self.slot = self._reader.read_int32()
        self.id = self._reader.read_int32()
        self.level = self._reader.read_int32()
        if self._reader.remaining() >= 4:
            self._reader.read_int32()  # characterType


_ITEM_RECORD_FIXED = 62  # см. docs/INVENTORY.md §On-wire item record.


def _read_item_record(reader: PacketReader) -> dict:
    """Читает одну запись item record (фиксированные 62 байта).

    Поля по docs/INVENTORY.md §On-wire item record. Хвост `enchantOption[N]`
    не парсится: `N` на проводе не передаётся, его знает только клиент по шаблону
    item id.
    """
    return {
        "object_id": reader.read_uint32(),
        "item_id": reader.read_uint32(),
        "location": reader.read_uint32(),
        "count": reader.read_int64(),
        "type2": reader.read_uint16(),
        "custom_type1": reader.read_uint16(),
        "equipped": reader.read_uint16(),
        "body_part": reader.read_uint32(),
        "enchant": reader.read_uint16(),
        "custom_type2": reader.read_uint16(),
        "augmentation_id": reader.read_uint32(),
        "mana": reader.read_int32(),
        "time": reader.read_int32(),
        "attack_element_type": reader.read_int16(),
        "attack_element_power": reader.read_uint16(),
        "def_element": [reader.read_uint16() for _ in range(6)],
    }


class StatusUpdatePacket(ServerPacket):
    """StatusUpdate (S→C, opcode 0x18).

    Body: `i32 objectId`, `i32 count`, `count × (i32 attrId, i32 value)`.

    Attr ids (L2JMobius `StatusUpdate.java`): LEVEL=1, EXP=2, STR=3, DEX=4, CON=5,
    INT=6, WIT=7, MEN=8, CUR_HP=9, MAX_HP=10, CUR_MP=11, MAX_MP=12, SP=13,
    CUR_LOAD=14, MAX_LOAD=15, P_ATK=17, ATK_SPD=18, P_DEF=19, EVASION=20,
    ACCURACY=21, CRITICAL=22, M_ATK=23, CAST_SPD=24, M_DEF=25, PVP_FLAG=26,
    KARMA=27, CUR_CP=33, MAX_CP=34.
    """

    opcode: ClassVar[int] = 0x18
    __slots__ = ("object_id", "updates")

    def __init__(self, data: bytes) -> None:
        self.object_id: int = 0
        self.updates: dict[int, int] = {}
        super().__init__(data)

    def _read(self) -> None:
        try:
            self.object_id = self._reader.read_int32()
            count = self._reader.read_int32()
            for _ in range(count):
                if self._reader.remaining() < 8:
                    break
                attr_id = self._reader.read_int32()
                value = self._reader.read_int32()
                self.updates[attr_id] = value
        except Exception:
            pass


class ItemListPacket(ServerPacket):
    """ItemList (S→C, opcode 0x11) — полный снимок инвентаря.

    Body: `u16 showWindow`, `u16 itemCount`, `itemCount × item_record`.
    См. docs/INVENTORY.md §ItemList.
    """

    opcode: ClassVar[int] = 0x11
    __slots__ = ("show_window", "items")

    def __init__(self, data: bytes) -> None:
        self.show_window: int = 0
        self.items: list[dict] = []
        super().__init__(data)

    def _read(self) -> None:
        try:
            self.show_window = self._reader.read_uint16()
            count = self._reader.read_uint16()
            for _ in range(count):
                if self._reader.remaining() < _ITEM_RECORD_FIXED:
                    break
                self.items.append(_read_item_record(self._reader))
        except Exception:
            pass


class InventoryUpdatePacket(ServerPacket):
    """InventoryUpdate (S→C, opcode 0x21) — инкрементальное изменение инвентаря.

    Body: `u16 changeCount`, `changeCount × (u16 changeType, item_record)`.
    changeType: 1=ADDED, 2=MODIFIED, 3=REMOVED.
    """

    opcode: ClassVar[int] = 0x21
    __slots__ = ("changes",)

    def __init__(self, data: bytes) -> None:
        self.changes: list[tuple[int, dict]] = []
        super().__init__(data)

    def _read(self) -> None:
        try:
            count = self._reader.read_uint16()
            for _ in range(count):
                if self._reader.remaining() < 2 + _ITEM_RECORD_FIXED:
                    break
                change_type = self._reader.read_uint16()
                record = _read_item_record(self._reader)
                self.changes.append((change_type, record))
        except Exception:
            pass


class SkillListPacket(ServerPacket):
    """SkillList (S→C, opcode 0x5F на HighFive).

    Body: `i32 count`, `count × (i32 passive, i32 level, i32 id, u8 disabled)`.
    """

    opcode: ClassVar[int] = 0x5F
    __slots__ = ("skills",)

    def __init__(self, data: bytes) -> None:
        self.skills: list[dict] = []
        super().__init__(data)

    def _read(self) -> None:
        try:
            count = self._reader.read_int32()
            for _ in range(count):
                if self._reader.remaining() < 13:
                    break
                passive = self._reader.read_int32()
                level = self._reader.read_int32()
                sid = self._reader.read_int32()
                disabled = self._reader.read_byte()
                self.skills.append(
                    {
                        "id": sid,
                        "level": level,
                        "passive": bool(passive),
                        "disabled": bool(disabled),
                    }
                )
        except Exception:
            pass


class NpcInfoPacket(ServerPacket):
    """NpcInfo (S→C, opcode 0x0C): появление / обновление NPC в поле зрения.

    Best-effort парсинг первых полей L2JMobius HighFive `NpcInfo.java`:
        writeC(0x0C);
        writeD(objectId);
        writeD(displayId + 1000000);
        writeD(isAutoAttackable ? 1 : 0);
        writeD(x); writeD(y); writeD(z);
        writeD(heading);
        ...

    Остальное (stats, строки, баффы, appearance) не читается —
    для таргетинга достаточно objectId + координат + флага attackable.
    """

    opcode: ClassVar[int] = 0x0C
    __slots__ = ("object_id", "template_id", "attackable", "x", "y", "z", "heading")

    def __init__(self, data: bytes) -> None:
        self.object_id: int = 0
        self.template_id: int = 0
        self.attackable: bool = False
        self.x: int = 0
        self.y: int = 0
        self.z: int = 0
        self.heading: int = 0
        super().__init__(data)

    def _read(self) -> None:
        self.object_id = self._reader.read_int32()
        self.template_id = self._reader.read_int32() - 1000000
        self.attackable = self._reader.read_int32() != 0
        self.x = self._reader.read_int32()
        self.y = self._reader.read_int32()
        self.z = self._reader.read_int32()
        self.heading = self._reader.read_int32()


class DeleteObjectPacket(ServerPacket):
    """DeleteObject (S→C, opcode 0x08): объект покинул зону видимости / умер.

    Body: i32 objectId, [i32 unknown].
    """

    opcode: ClassVar[int] = 0x08
    __slots__ = ("object_id",)

    def __init__(self, data: bytes) -> None:
        self.object_id: int = 0
        super().__init__(data)

    def _read(self) -> None:
        self.object_id = self._reader.read_int32()


__all__ = [
    "KeyPacket",
    "CharSelectionInfoPacket",
    "CharSelectedPacket",
    "UserInfoPacket",
    "NetPingRequestPacket",
    "MyTargetSelectedPacket",
    "ShortCutInitPacket",
    "ShortCutRegisterPacket",
    "StatusUpdatePacket",
    "ItemListPacket",
    "InventoryUpdatePacket",
    "SkillListPacket",
    "NpcInfoPacket",
    "DeleteObjectPacket",
]
