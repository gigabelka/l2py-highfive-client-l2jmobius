
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

    opcode: ClassVar[int] = 0x0E
    __slots__ = ("protocol_version",)


    HIGH_FIVE_PROTOCOL = 273

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



class AuthLoginPacket(ClientPacket):
    """Пакет авторизации на Game Server (C).

    Содержит session keys из Login Server.

    TODO: Уточнить опкод для High Five (обычно 0x2B).
    """

    opcode: ClassVar[int] = 0x2B
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
        """Записывает поля пакета.

        Логин кодируется как UTF-16LE с двойным null-terminator (как стандартная строка L2).
        Сервер использует readString() который читает UTF-16LE до \x00\x00.
        """

        self._writer.write_string(self.login)
        self._writer.write_uint32(self.play_ok2)
        self._writer.write_uint32(self.play_ok1)
        self._writer.write_uint32(self.login_ok1)
        self._writer.write_uint32(self.login_ok2)


class CharacterSelectPacket(ClientPacket):
    """Пакет выбора персонажа (C).

    Отправляется после получения списка персонажей.
    """

    opcode: ClassVar[int] = 0x12
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
        self._writer.write_int16(0)
        self._writer.write_int32(0)
        self._writer.write_int32(0)
        self._writer.write_int32(0)


class EnterWorldPacket(ClientPacket):
    """Пакет входа в мир (C).

    Финальный пакет для входа персонажа в игровой мир.

    TODO: Уточнить опкод для High Five (обычно 0x11).
    """

    opcode: ClassVar[int] = 0x11
    __slots__ = ()

    def _write(self) -> None:
        """Записывает поля пакета.

        L2J Mobius требует 104 нулевых байта после опкода (hardware info /
        traceroute blob) — иначе BufferUnderflowException.
        """
        self._writer.write_bytes(b"\x00" * 104)


class RequestKeyMappingPacket(ClientPacket):
    """Запрос клиентского key mapping (расширенный опкод 0xD0 0x21).

    Отправляется между CharSelected и EnterWorld — обязателен для L2JMobius.
    """

    opcode: ClassVar[int] = 0xD0
    __slots__ = ()

    def _write(self) -> None:
        """Записывает поля пакета."""
        self._writer.write_uint16(0x0021)


class NetPingPacket(ClientPacket):
    """Ответ на NetPingRequest сервера (опкод 0xB1, CT 2.6 HighFive).

    5-байтовая форма: opcode + echoed pingId.
    """

    opcode: ClassVar[int] = 0xB1
    __slots__ = ("ping_id",)

    def __init__(self, ping_id: int) -> None:
        """Инициализация пакета.

        Args:
            ping_id: Идентификатор пинга из NetPingRequest.
        """
        self.ping_id = ping_id
        super().__init__()

    def _write(self) -> None:
        """Записывает поля пакета."""
        self._writer.write_int32(self.ping_id)


class ActionPacket(ClientPacket):
    """Action (C→S, opcode 0x1F): клик по объекту / pick-up предмета.

    Body: i32 object_id, i32 origin_x, i32 origin_y, i32 origin_z, u8 action_id.
    См. docs/ACTIONS.md §1.
    """

    opcode: ClassVar[int] = 0x1F
    __slots__ = ("object_id", "origin_x", "origin_y", "origin_z", "action_id")

    def __init__(
        self,
        object_id: int,
        origin_x: int,
        origin_y: int,
        origin_z: int,
        action_id: int = 0,
    ) -> None:
        self.object_id = object_id
        self.origin_x = origin_x
        self.origin_y = origin_y
        self.origin_z = origin_z
        self.action_id = action_id
        super().__init__()

    def _write(self) -> None:
        self._writer.write_int32(self.object_id)
        self._writer.write_int32(self.origin_x)
        self._writer.write_int32(self.origin_y)
        self._writer.write_int32(self.origin_z)
        self._writer.write_byte(self.action_id & 0xFF)


class AttackRequestPacket(ClientPacket):
    """AttackRequest (C→S, opcode 0x32): атака по цели.

    Body: i32 object_id, i32 origin_x, i32 origin_y, i32 origin_z, u8 attack_id
    (0 = обычная, 1 = shift-click / forced). См. docs/ACTIONS.md §3.

    Примечание: опкод 0x32 совпадает с серверным UserInfoPacket, но направления
    разные — конфликта нет.
    """

    opcode: ClassVar[int] = 0x32
    __slots__ = ("object_id", "origin_x", "origin_y", "origin_z", "attack_id")

    def __init__(
        self,
        object_id: int,
        origin_x: int,
        origin_y: int,
        origin_z: int,
        attack_id: int = 0,
    ) -> None:
        self.object_id = object_id
        self.origin_x = origin_x
        self.origin_y = origin_y
        self.origin_z = origin_z
        self.attack_id = attack_id
        super().__init__()

    def _write(self) -> None:
        self._writer.write_int32(self.object_id)
        self._writer.write_int32(self.origin_x)
        self._writer.write_int32(self.origin_y)
        self._writer.write_int32(self.origin_z)
        self._writer.write_byte(self.attack_id & 0xFF)


class RequestActionUsePacket(ClientPacket):
    """RequestActionUse (C→S, opcode 0x56): активация action_id (sit/stand, social,
    pet/summon/airship команды и т.д.).

    Body: i32 action_id, i32 ctrl_pressed, u8 shift_pressed. См. docs/ACTIONS.md §9.1.
    """

    opcode: ClassVar[int] = 0x56
    __slots__ = ("action_id", "ctrl", "shift")

    def __init__(self, action_id: int, ctrl: bool = False, shift: bool = False) -> None:
        self.action_id = action_id
        self.ctrl = ctrl
        self.shift = shift
        super().__init__()

    def _write(self) -> None:
        self._writer.write_int32(self.action_id)
        self._writer.write_int32(1 if self.ctrl else 0)
        self._writer.write_byte(1 if self.shift else 0)


class RequestMagicSkillUsePacket(ClientPacket):
    """RequestMagicSkillUse (C→S, opcode 0x39): применение скилла.

    Body: i32 skill_id, i32 ctrl_pressed, u8 shift_pressed.
    """

    opcode: ClassVar[int] = 0x39
    __slots__ = ("skill_id", "ctrl", "shift")

    def __init__(self, skill_id: int, ctrl: bool = False, shift: bool = False) -> None:
        self.skill_id = skill_id
        self.ctrl = ctrl
        self.shift = shift
        super().__init__()

    def _write(self) -> None:
        self._writer.write_int32(self.skill_id)
        self._writer.write_int32(1 if self.ctrl else 0)
        self._writer.write_byte(1 if self.shift else 0)


class UseItemPacket(ClientPacket):
    """UseItem (C→S, opcode 0x19 на CT 2.6 HighFive): использование предмета.

    Body: i32 object_id, i32 ctrl_pressed.
    """

    opcode: ClassVar[int] = 0x19
    __slots__ = ("object_id", "ctrl")

    def __init__(self, object_id: int, ctrl: bool = False) -> None:
        self.object_id = object_id
        self.ctrl = ctrl
        super().__init__()

    def _write(self) -> None:
        self._writer.write_int32(self.object_id)
        self._writer.write_int32(1 if self.ctrl else 0)


__all__ = [
    "ProtocolVersionPacket",
    "AuthLoginPacket",
    "CharacterSelectPacket",
    "EnterWorldPacket",
    "RequestKeyMappingPacket",
    "NetPingPacket",
    "ActionPacket",
    "AttackRequestPacket",
    "RequestActionUsePacket",
    "RequestMagicSkillUsePacket",
    "UseItemPacket",
]
