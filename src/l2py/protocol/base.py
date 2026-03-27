# -*- coding: utf-8 -*-
"""Базовые классы для работы с бинарными пакетами L2.

Содержит PacketReader и PacketWriter для сериализации/десериализации
данных в Little Endian формате, а также абстрактные базовые классы
для пакетов клиента и сервера.
"""

from __future__ import annotations

import struct
from abc import ABC, abstractmethod
from typing import ClassVar


class PacketReader:
    """Чтение бинарных данных из байтового массива.

    Используется для парсинга пакетов от сервера.
    Все числовые типы читаются в Little Endian.
    """

    __slots__ = ("_data", "_offset")

    def __init__(self, data: bytes) -> None:
        """Инициализация reader'а.

        Args:
            data: Байтовый массив для чтения.
        """
        self._data = data
        self._offset = 0

    def read_byte(self) -> int:
        """Читает 1 байт (unsigned).

        Returns:
            Значение байта (0-255).

        Raises:
            IndexError: Если данных недостаточно.
        """
        value = self._data[self._offset]
        self._offset += 1
        return value

    def read_int16(self) -> int:
        """Читает 2 байта (signed int16, little-endian).

        Returns:
            Значение int16.
        """
        value = struct.unpack("<h", self._data[self._offset : self._offset + 2])[0]
        self._offset += 2
        return value

    def read_uint16(self) -> int:
        """Читает 2 байта (unsigned uint16, little-endian).

        Returns:
            Значение uint16.
        """
        value = struct.unpack("<H", self._data[self._offset : self._offset + 2])[0]
        self._offset += 2
        return value

    def read_int32(self) -> int:
        """Читает 4 байта (signed int32, little-endian).

        Returns:
            Значение int32.
        """
        value = struct.unpack("<i", self._data[self._offset : self._offset + 4])[0]
        self._offset += 4
        return value

    def read_uint32(self) -> int:
        """Читает 4 байта (unsigned uint32, little-endian).

        Returns:
            Значение uint32.
        """
        value = struct.unpack("<I", self._data[self._offset : self._offset + 4])[0]
        self._offset += 4
        return value

    def read_int64(self) -> int:
        """Читает 8 байт (signed int64, little-endian).

        Returns:
            Значение int64.
        """
        value = struct.unpack("<q", self._data[self._offset : self._offset + 8])[0]
        self._offset += 8
        return value

    def read_bytes(self, n: int) -> bytes:
        """Читает n байт.

        Args:
            n: Количество байт для чтения.

        Returns:
            Прочитанные байты.
        """
        value = self._data[self._offset : self._offset + n]
        self._offset += n
        return bytes(value)

    def read_string(self) -> str:
        """Читает UTF-16LE строку, заканчивающуюся \x00\x00.

        Returns:
            Декодированная строка.
        """
        # Ищем завершающий \x00\x00
        end = self._offset
        while end + 1 < len(self._data):
            if self._data[end] == 0 and self._data[end + 1] == 0:
                break
            end += 2

        # Читаем строку без завершающих нулей
        string_bytes = self._data[self._offset : end]
        result = string_bytes.decode("utf-16le", errors="ignore")
        self._offset = end + 2  # Пропускаем \x00\x00
        return result

    def remaining(self) -> int:
        """Возвращает количество оставшихся байт.

        Returns:
            Число непрочитанных байт.
        """
        return len(self._data) - self._offset

    def skip(self, n: int) -> None:
        """Пропускает n байт.

        Args:
            n: Количество байт для пропуска.
        """
        self._offset += n


class PacketWriter:
    """Запись бинарных данных в байтовый массив.

    Используется для сериализации пакетов клиента.
    Все числовые типы записываются в Little Endian.
    """

    __slots__ = ("_buffer",)

    def __init__(self) -> None:
        """Инициализация writer'а с пустым буфером."""
        self._buffer = bytearray()

    def write_byte(self, value: int) -> None:
        """Записывает 1 байт.

        Args:
            value: Значение для записи (0-255).
        """
        self._buffer.append(value & 0xFF)

    def write_int16(self, value: int) -> None:
        """Записывает 2 байта (signed int16, little-endian).

        Args:
            value: Значение для записи.
        """
        self._buffer.extend(struct.pack("<h", value))

    def write_uint16(self, value: int) -> None:
        """Записывает 2 байта (unsigned uint16, little-endian).

        Args:
            value: Значение для записи.
        """
        self._buffer.extend(struct.pack("<H", value))

    def write_int32(self, value: int) -> None:
        """Записывает 4 байта (signed int32, little-endian).

        Args:
            value: Значение для записи.
        """
        self._buffer.extend(struct.pack("<i", value))

    def write_uint32(self, value: int) -> None:
        """Записывает 4 байта (unsigned uint32, little-endian).

        Args:
            value: Значение для записи.
        """
        self._buffer.extend(struct.pack("<I", value))

    def write_int64(self, value: int) -> None:
        """Записывает 8 байт (signed int64, little-endian).

        Args:
            value: Значение для записи.
        """
        self._buffer.extend(struct.pack("<q", value))

    def write_bytes(self, data: bytes) -> None:
        """Записывает байты.

        Args:
            data: Байты для записи.
        """
        self._buffer.extend(data)

    def write_string(self, value: str) -> None:
        """Записывает UTF-16LE строку с завершающим \x00\x00.

        Args:
            value: Строка для записи.
        """
        encoded = value.encode("utf-16le")
        self._buffer.extend(encoded)
        self._buffer.extend(b"\x00\x00")  # Завершающий нуль

    def to_bytes(self) -> bytes:
        """Возвращает финальный байтовый массив.

        Returns:
            Собранные байты.
        """
        return bytes(self._buffer)

    def __len__(self) -> int:
        """Возвращает текущий размер буфера.

        Returns:
            Количество байт в буфере.
        """
        return len(self._buffer)


class ServerPacket(ABC):
    """Базовый класс для пакетов от сервера.

    Attributes:
        opcode: Опкод пакета (должен быть переопределён).
    """

    opcode: ClassVar[int] = 0x00
    __slots__ = ("_reader",)

    def __init__(self, data: bytes) -> None:
        """Инициализирует и парсит пакет.

        Args:
            data: Байты пакета (без опкода).
        """
        self._reader = PacketReader(data)
        self._read()

    @abstractmethod
    def _read(self) -> None:
        """Абстрактный метод для парсинга полей.

        Должен быть реализован в подклассах.
        """
        raise NotImplementedError


class ClientPacket(ABC):
    """Базовый класс для пакетов от клиента.

    Attributes:
        opcode: Опкод пакета (должен быть переопределён).
    """

    opcode: ClassVar[int] = 0x00
    __slots__ = ("_writer",)

    def __init__(self) -> None:
        """Инициализирует writer и записывает опкод."""
        self._writer = PacketWriter()
        self._writer.write_byte(self.opcode)
        self._write()

    @abstractmethod
    def _write(self) -> None:
        """Абстрактный метод для записи полей.

        Должен быть реализован в подклассах.
        """
        raise NotImplementedError

    def to_bytes(self) -> bytes:
        """Возвращает сериализованный пакет.

        Returns:
            Байты пакета с опкодом.
        """
        return self._writer.to_bytes()


__all__ = [
    "PacketReader",
    "PacketWriter",
    "ServerPacket",
    "ClientPacket",
]
