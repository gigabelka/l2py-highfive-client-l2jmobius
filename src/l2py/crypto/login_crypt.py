# -*- coding: utf-8 -*-
"""Криптография для Login Server.

Содержит LoginCrypt — комбинированная система шифрования:
- Первый пакет (Init) шифруется статическим Blowfish + XOR
- Остальные пакеты — Blowfish с сессионным ключом + checksum
"""

from l2py.crypto.blowfish import L2Blowfish

# Статический Blowfish-ключ для первого пакета (Init)
# Используется для дешифрования начального пакета от сервера
STATIC_BLOWFISH_KEY = bytes(
    [0x6B, 0x60, 0xCB, 0x5B, 0x82, 0xCE, 0x90, 0xB1,
     0xCC, 0x8B, 0x6B, 0x55, 0x6E, 0x95, 0x87, 0x03,
     0x33, 0x00, 0x00, 0x00, 0x00]
)


class LoginCrypt:
    """Криптография Login Server.

    Реализует:
    - Статическое Blowfish шифрование для Init пакета
    - Сессионное Blowfish шифрование с checksum
    - XOR для первого пакета
    """

    __slots__ = ("_static_cipher", "_session_cipher", "_key")

    def __init__(self, static_key: bytes | None = None) -> None:
        """Инициализация криптографии.

        Args:
            static_key: Статический Blowfish-ключ. Если None — используется
                встроенный STATIC_BLOWFISH_KEY.
        """
        key = static_key if static_key is not None else STATIC_BLOWFISH_KEY
        self._static_cipher = L2Blowfish(key)
        self._session_cipher: L2Blowfish | None = None
        self._key: bytes | None = None

    def set_key(self, key: bytes) -> None:
        """Устанавливает сессионный Blowfish-ключ.

        Вызывается после получения Init пакета от сервера.

        Args:
            key: 16-байтный сессионный ключ.
        """
        self._key = key
        self._session_cipher = L2Blowfish(key)

    def _checksum(self, data: bytes) -> int:
        """Вычисляет XOR-based checksum для данных.

        Алгоритм L2: XOR всех 4-байтных слов кроме последних 8 байт.

        Args:
            data: Данные для вычисления checksum.

        Returns:
            Значение checksum (32-bit).
        """
        checksum = 0
        # XOR-им по 4 байта, кроме последних 8 (там checksum + padding)
        for i in range(0, len(data) - 8, 4):
            word = int.from_bytes(data[i : i + 4], "little")
            checksum ^= word
        return checksum & 0xFFFFFFFF

    def _verify_checksum(self, data: bytes) -> bool:
        """Проверяет checksum в данных.

        Args:
            data: Данные с checksum в последних 8 байтах.

        Returns:
            True если checksum совпадает.
        """
        if len(data) < 8:
            return False
        stored_checksum = int.from_bytes(data[-8:-4], "little")
        computed_checksum = self._checksum(data)
        return stored_checksum == computed_checksum

    def decrypt_init(self, data: bytes) -> bytes:
        """Дешифрует Init пакет (первый пакет от сервера).

        Использует статический Blowfish + XOR.

        Args:
            data: Зашифрованные данные.

        Returns:
            Дешифрованные данные.
        """
        # Сначала Blowfish decrypt
        decrypted = self._static_cipher.decrypt(data)

        # Затем XOR-дешифрование
        # Последние 4 байта перед паддингом = XOR-ключ
        # Для простоты применяем XOR ко всему пакету
        xor_key_start = len(decrypted) - 8
        xor_key = int.from_bytes(decrypted[xor_key_start : xor_key_start + 4], "little")

        result = bytearray(decrypted)
        for i in range(0, len(result), 4):
            if i + 4 <= len(result):
                block = int.from_bytes(result[i : i + 4], "little")
                block ^= xor_key
                result[i : i + 4] = block.to_bytes(4, "little")

        return bytes(result)

    def decrypt(self, data: bytes) -> bytes:
        """Дешифрует обычный пакет с сессионным ключом.

        Args:
            data: Зашифрованные данные.

        Returns:
            Дешифрованные данные.

        Raises:
            ValueError: Если сессионный ключ не установлен.
            RuntimeError: Если checksum не совпадает.
        """
        if self._session_cipher is None:
            raise ValueError("Session key not set")

        # Blowfish decrypt
        decrypted = self._session_cipher.decrypt(data)

        # Проверка checksum
        if not self._verify_checksum(decrypted):
            raise RuntimeError("Checksum verification failed")

        # Возвращаем данные без checksum (последние 8 байт)
        return decrypted[:-8]

    def encrypt(self, data: bytes) -> bytes:
        """Шифрует пакет сессионным ключом.

        Добавляет checksum перед шифрованием.

        Args:
            data: Исходные данные.

        Returns:
            Зашифрованные данные.

        Raises:
            ValueError: Если сессионный ключ не установлен.
        """
        if self._session_cipher is None:
            raise ValueError("Session key not set")

        # Дополняем до кратности 8
        padding_needed = 8 - (len(data) % 8)
        if padding_needed == 8:
            padding_needed = 0
        padded = data + b"\x00" * padding_needed

        # Вычисляем и добавляем checksum
        checksum = self._checksum(padded + b"\x00" * 8)
        checksum_bytes = checksum.to_bytes(4, "little")

        # Данные + checksum + padding (4 байта нулей)
        full_data = padded + checksum_bytes + b"\x00" * 4

        # Blowfish encrypt
        return self._session_cipher.encrypt(full_data)


__all__ = ["LoginCrypt", "STATIC_BLOWFISH_KEY"]
