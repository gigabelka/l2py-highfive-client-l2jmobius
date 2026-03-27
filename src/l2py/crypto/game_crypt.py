# -*- coding: utf-8 -*-
"""XOR-шифрование для Game Server.

Используется после получения KeyPacket от Game Server.
Ключ состоит из двух частей:
  - dynamic_part (8 байт) — приходит от сервера
  - static_part (8 байт) — зашит в клиент

После каждой операции последние 4 байта dynamic_part
инкрементируются на количество обработанных байт.
"""

# Статическая часть ключа для High Five / L2JMobius
STATIC_KEY = bytes([0xA1, 0x6C, 0x54, 0x87, 0x09, 0xF1, 0x1C, 0x8D])


class GameCrypt:
    """XOR-шифрование для пакетов Game Server.

    Реализует двунаправленный XOR с динамически изменяющимся ключом.
    Отдельные ключи для encrypt и decrypt (разные состояния).
    """

    __slots__ = ("_decrypt_key", "_encrypt_key", "_enabled")

    def __init__(self) -> None:
        """Инициализация криптографии (disabled по умолчанию)."""
        self._decrypt_key: bytearray | None = None
        self._encrypt_key: bytearray | None = None
        self._enabled = False

    @property
    def enabled(self) -> bool:
        """Возвращает True если шифрование включено."""
        return self._enabled

    def set_key(self, dynamic_key: bytes) -> None:
        """Устанавливает XOR-ключ.

        Формирует полный ключ из dynamic_part + static_part.
        Создаёт отдельные копии для encrypt и decrypt.

        Args:
            dynamic_key: 8 байт динамической части от сервера.

        Raises:
            ValueError: Если dynamic_key не 8 байт.
        """
        if len(dynamic_key) != 8:
            raise ValueError(f"Dynamic key must be 8 bytes, got {len(dynamic_key)}")

        full_key = dynamic_key + STATIC_KEY
        self._decrypt_key = bytearray(full_key)
        self._encrypt_key = bytearray(full_key)
        self._enabled = True

    def _update_key(self, key: bytearray, length: int) -> None:
        """Обновляет ключ после операции.

        Инкрементирует последние 4 байта (позиции 12-15) на length.

        Args:
            key: Ключ для обновления.
            length: Количество обработанных байт.
        """
        # Последние 4 байта — little-endian счётчик
        current = int.from_bytes(key[12:16], "little")
        new_value = (current + length) & 0xFFFFFFFF
        key[12:16] = new_value.to_bytes(4, "little")

    def decrypt(self, data: bytes) -> bytes:
        """Дешифрует данные XOR.

        Алгоритм:
        1. Сохраняем исходный байт
        2. XOR с ключом
        3. Сохраняем исходный байт в ключ

        Args:
            data: Зашифрованные данные.

        Returns:
            Дешифрованные данные.
        """
        if not self._enabled or self._decrypt_key is None:
            return data

        key = self._decrypt_key
        key_len = len(key)
        result = bytearray(data)

        for i in range(len(result)):
            temp = result[i]
            result[i] ^= key[i % key_len]
            key[i % key_len] = temp

        self._update_key(key, len(result))
        return bytes(result)

    def encrypt(self, data: bytes) -> bytes:
        """Шифрует данные XOR.

        Алгоритм:
        1. XOR с ключом
        2. Сохраняем результат в ключ

        Args:
            data: Исходные данные.

        Returns:
            Зашифрованные данные.
        """
        if not self._enabled or self._encrypt_key is None:
            return data

        key = self._encrypt_key
        key_len = len(key)
        result = bytearray(data)

        for i in range(len(result)):
            result[i] ^= key[i % key_len]
            key[i % key_len] = result[i]

        self._update_key(key, len(result))
        return bytes(result)


__all__ = ["GameCrypt", "STATIC_KEY"]
