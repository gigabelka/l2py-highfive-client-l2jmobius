# -*- coding: utf-8 -*-
"""Криптография для Login Server.

Содержит LoginCrypt — комбинированная система шифрования:
- Первый пакет (Init) шифруется статическим Blowfish + XOR
- Остальные пакеты — Blowfish с сессионным ключом + checksum

Основано на l2js-client: https://github.com/npetrovski/l2js-client
"""

from l2py.crypto.blowfish import L2Blowfish

# Статический Blowfish-ключ для первого пакета (Init)
# Используется для дешифрования начального пакета от сервера
# Из l2js-client: src/network/LoginCrypt.ts
STATIC_BLOWFISH_KEY = bytes([
    0x6b, 0x60, 0xcb, 0x5b, 0x82, 0xce, 0x90, 0xb1,
    0xcc, 0x2b, 0x6c, 0x55, 0x6c, 0x6c, 0x6c, 0x6c
])


class LoginCrypt:
    """Криптография Login Server.

    Реализует:
    - Статическое Blowfish шифрование для Init пакета
    - Сессионное Blowfish шифрование с checksum
    - XOR для первого пакета
    """

    __slots__ = ("_static_cipher", "_session_cipher", "_key", "_is_static")

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
        self._is_static = True

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

        Алгоритм L2: XOR всех 4-байтных слов кроме последних 4 байт.

        Args:
            data: Данные для вычисления checksum.

        Returns:
            Значение checksum (32-bit).
        """
        checksum = 0
        # XOR-им по 4 байта, кроме последних 4
        for i in range(0, len(data) - 4, 4):
            word = int.from_bytes(data[i : i + 4], "little")
            checksum ^= word
        return checksum & 0xFFFFFFFF

    def _verify_checksum(self, data: bytes) -> bool:
        """Проверяет checksum в данных.

        Args:
            data: Данные с checksum в последних 4 байтах.

        Returns:
            True если checksum совпадает.
        """
        if len(data) < 4:
            return False
        stored_checksum = int.from_bytes(data[-4:], "little")
        computed_checksum = self._checksum(data)
        return stored_checksum == computed_checksum

    def _dec_xor_pass(self, data: bytearray, offset: int, size: int, key: int) -> None:
        """XOR дешифрование для Init пакета (обратный алгоритм).
        
        Из l2js-client: decXORPass
        Работает с конца данных, идёт к началу.
        
        Args:
            data: Данные для дешифрования (bytearray).
            offset: Начальное смещение.
            size: Размер данных.
            key: XOR ключ.
        """
        stop = 4 + offset
        pos = size - 12
        ecx = key
        
        while stop <= pos:
            # Читаем 4 байта
            edx = data[pos] & 0xff
            edx |= (data[pos + 1] & 0xff) << 8
            edx |= (data[pos + 2] & 0xff) << 16
            edx |= (data[pos + 3] & 0xff) << 24
            
            # XOR
            edx ^= ecx
            # Вычитаем (как в оригинале)
            ecx -= edx
            
            # Записываем обратно
            data[pos] = edx & 0xff
            data[pos + 1] = (edx >> 8) & 0xff
            data[pos + 2] = (edx >> 16) & 0xff
            data[pos + 3] = (edx >> 24) & 0xff
            
            pos -= 4

    def decrypt_init(self, data: bytes) -> bytes:
        """Дешифрует Init пакет (первый пакет от сервера).

        Использует статический Blowfish + XOR.
        Алгоритм из l2js-client.

        Args:
            data: Зашифрованные данные.

        Returns:
            Дешифрованные данные (без trailing 8-byte XOR блока).
        """
        # Сначала Blowfish decrypt
        decrypted = bytearray(self._static_cipher.decrypt(data))
        
        # Затем XOR-дешифрование
        # XOR ключ в последних 8 байтах (первые 4 из них)
        rnd_xor = decrypted[-8] & 0xff
        rnd_xor |= (decrypted[-7] << 8) & 0xff00
        rnd_xor |= (decrypted[-6] << 16) & 0xff0000
        rnd_xor |= (decrypted[-5] << 24) & 0xff000000
        
        self._dec_xor_pass(decrypted, 0, len(decrypted), rnd_xor)
        
        # Отрезаем trailing 8-byte XOR блок
        return bytes(decrypted[:-8])

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
        decrypted = bytearray(self._session_cipher.decrypt(data))

        # Проверка checksum (последние 4 байта)
        if not self._verify_checksum(decrypted):
            raise RuntimeError("Checksum verification failed")

        # Возвращаем данные без checksum
        return bytes(decrypted[:-4])

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
        padded = bytearray(data) + b"\x00" * padding_needed

        # Вычисляем и добавляем checksum
        checksum = self._checksum(padded + b"\x00" * 4)
        padded.extend([
            checksum & 0xff,
            (checksum >> 8) & 0xff,
            (checksum >> 16) & 0xff,
            (checksum >> 24) & 0xff,
        ])

        # Blowfish encrypt
        return self._session_cipher.encrypt(bytes(padded))


__all__ = ["LoginCrypt", "STATIC_BLOWFISH_KEY"]
