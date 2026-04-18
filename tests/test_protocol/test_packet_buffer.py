
"""Тесты для PacketReader и PacketWriter."""

import struct

import pytest

from l2py.protocol.base import PacketReader, PacketWriter


class TestPacketWriter:
    """Тесты для PacketWriter."""

    def test_write_byte(self):
        """Тест записи одного байта."""
        writer = PacketWriter()
        writer.write_byte(0xAB)
        assert writer.to_bytes() == b"\xab"

    def test_write_int16(self):
        """Тест записи int16 (little-endian)."""
        writer = PacketWriter()
        writer.write_int16(0x1234)
        assert writer.to_bytes() == b"\x34\x12"

    def test_write_uint16(self):
        """Тест записи uint16 (little-endian)."""
        writer = PacketWriter()
        writer.write_uint16(0x1234)
        assert writer.to_bytes() == b"\x34\x12"

    def test_write_int32(self):
        """Тест записи int32 (little-endian)."""
        writer = PacketWriter()
        writer.write_int32(0x12345678)
        assert writer.to_bytes() == b"\x78\x56\x34\x12"

    def test_write_uint32(self):
        """Тест записи uint32 (little-endian)."""
        writer = PacketWriter()
        writer.write_uint32(0x12345678)
        assert writer.to_bytes() == b"\x78\x56\x34\x12"

    def test_write_int64(self):
        """Тест записи int64 (little-endian)."""
        writer = PacketWriter()
        writer.write_int64(0x123456789ABCDEF0)
        expected = struct.pack("<q", 0x123456789ABCDEF0)
        assert writer.to_bytes() == expected

    def test_write_bytes(self):
        """Тест записи произвольных байт."""
        writer = PacketWriter()
        data = b"\x01\x02\x03\x04"
        writer.write_bytes(data)
        assert writer.to_bytes() == data

    def test_write_string_utf16le(self):
        """Тест записи UTF-16LE строки с завершающим нулём."""
        writer = PacketWriter()
        writer.write_string("Hi")
        expected = b"H\x00i\x00\x00\x00"
        assert writer.to_bytes() == expected

    def test_write_string_russian(self):
        """Тест записи русской строки в UTF-16LE."""
        writer = PacketWriter()
        writer.write_string("Привет")
        expected = "Привет".encode("utf-16le") + b"\x00\x00"
        assert writer.to_bytes() == expected

    def test_len(self):
        """Тест метода __len__."""
        writer = PacketWriter()
        assert len(writer) == 0
        writer.write_int32(42)
        assert len(writer) == 4
        writer.write_byte(1)
        assert len(writer) == 5


class TestPacketReader:
    """Тесты для PacketReader."""

    def test_read_byte(self):
        """Тест чтения одного байта."""
        reader = PacketReader(b"\xab")
        assert reader.read_byte() == 0xAB

    def test_read_int16(self):
        """Тест чтения int16 (little-endian)."""
        reader = PacketReader(b"\x34\x12")
        assert reader.read_int16() == 0x1234

    def test_read_uint16(self):
        """Тест чтения uint16 (little-endian)."""
        reader = PacketReader(b"\x34\x12")
        assert reader.read_uint16() == 0x1234

    def test_read_int32(self):
        """Тест чтения int32 (little-endian)."""
        reader = PacketReader(b"\x78\x56\x34\x12")
        assert reader.read_int32() == 0x12345678

    def test_read_uint32(self):
        """Тест чтения uint32 (little-endian)."""
        reader = PacketReader(b"\x78\x56\x34\x12")
        assert reader.read_uint32() == 0x12345678

    def test_read_int64(self):
        """Тест чтения int64 (little-endian)."""
        data = struct.pack("<q", 0x123456789ABCDEF0)
        reader = PacketReader(data)
        assert reader.read_int64() == 0x123456789ABCDEF0

    def test_read_bytes(self):
        """Тест чтения произвольных байт."""
        data = b"\x01\x02\x03\x04"
        reader = PacketReader(data)
        assert reader.read_bytes(4) == data

    def test_read_string_utf16le(self):
        """Тест чтения UTF-16LE строки."""
        data = b"H\x00i\x00\x00\x00"
        reader = PacketReader(data)
        assert reader.read_string() == "Hi"

    def test_read_string_russian(self):
        """Тест чтения русской строки в UTF-16LE."""
        data = "Привет".encode("utf-16le") + b"\x00\x00"
        reader = PacketReader(data)
        assert reader.read_string() == "Привет"

    def test_remaining(self):
        """Тест метода remaining."""
        reader = PacketReader(b"\x01\x02\x03\x04\x05")
        assert reader.remaining() == 5
        reader.read_byte()
        assert reader.remaining() == 4
        reader.read_int32()
        assert reader.remaining() == 0

    def test_skip(self):
        """Тест метода skip."""
        reader = PacketReader(b"\x01\x02\x03\x04\x05")
        reader.skip(2)
        assert reader.read_byte() == 0x03


class TestRoundTrip:
    """Тесты записи и обратного чтения."""

    def test_byte_roundtrip(self):
        """Тест roundtrip для byte."""
        writer = PacketWriter()
        writer.write_byte(0xAB)

        reader = PacketReader(writer.to_bytes())
        assert reader.read_byte() == 0xAB

    def test_int16_roundtrip(self):
        """Тест roundtrip для int16."""
        writer = PacketWriter()
        writer.write_int16(-12345)

        reader = PacketReader(writer.to_bytes())
        assert reader.read_int16() == -12345

    def test_uint16_roundtrip(self):
        """Тест roundtrip для uint16."""
        writer = PacketWriter()
        writer.write_uint16(54321)

        reader = PacketReader(writer.to_bytes())
        assert reader.read_uint16() == 54321

    def test_int32_roundtrip(self):
        """Тест roundtrip для int32."""
        writer = PacketWriter()
        writer.write_int32(-123456789)

        reader = PacketReader(writer.to_bytes())
        assert reader.read_int32() == -123456789

    def test_uint32_roundtrip(self):
        """Тест roundtrip для uint32."""
        writer = PacketWriter()
        writer.write_uint32(1234567890)

        reader = PacketReader(writer.to_bytes())
        assert reader.read_uint32() == 1234567890

    def test_int64_roundtrip(self):
        """Тест roundtrip для int64."""
        writer = PacketWriter()
        writer.write_int64(-9223372036854775808)

        reader = PacketReader(writer.to_bytes())
        assert reader.read_int64() == -9223372036854775808

    def test_string_roundtrip(self):
        """Тест roundtrip для строки."""
        writer = PacketWriter()
        writer.write_string("Test String 123")

        reader = PacketReader(writer.to_bytes())
        assert reader.read_string() == "Test String 123"

    def test_complex_roundtrip(self):
        """Тест roundtrip для сложной структуры."""
        writer = PacketWriter()
        writer.write_int32(12345)
        writer.write_string("Test")
        writer.write_byte(0xFF)
        writer.write_int16(-100)

        reader = PacketReader(writer.to_bytes())
        assert reader.read_int32() == 12345
        assert reader.read_string() == "Test"
        assert reader.read_byte() == 0xFF
        assert reader.read_int16() == -100
