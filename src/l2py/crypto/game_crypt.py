# -*- coding: utf-8 -*-
"""XOR-шифрование для Game Server.

Точная копия алгоритма из L2JMobius Encryption.java
"""

# Статическая часть ключа для High Five / L2JMobius (последние 8 байт)
STATIC_KEY = bytes([0xC8, 0x27, 0x93, 0x01, 0xA1, 0x6C, 0x31, 0x97])


class GameCrypt:
    """XOR-шифрование для пакетов Game Server.
    
    Реализует точный алгоритм из L2JMobius:
    - Отдельные ключи для encrypt (_outKey) и decrypt (_inKey)
    - Первый пакет после включения шифрования не шифруется
    - Ключ обновляется после каждой операции
    """

    __slots__ = ("_in_key", "_out_key", "_enabled")

    def __init__(self) -> None:
        """Инициализация криптографии (disabled по умолчанию)."""
        self._in_key: bytearray | None = None
        self._out_key: bytearray | None = None
        self._enabled = False

    @property
    def enabled(self) -> bool:
        """Возвращает True если шифрование включено."""
        return self._enabled

    def set_key(self, dynamic_key: bytes) -> None:
        """Устанавливает XOR-ключ.

        Args:
            dynamic_key: 8 байт динамической части ключа от сервера.
                         Полный 16-байтный ключ собирается как:
                         [dynamic_key (8 bytes)] + [STATIC_KEY (8 bytes)]
        """
        if len(dynamic_key) != 8:
            raise ValueError(f"Dynamic key must be 8 bytes, got {len(dynamic_key)}")

        # Собираем полный 16-байтный ключ как в BlowFishKeygen.java
        full_key = bytearray(dynamic_key + STATIC_KEY)
        # Копируем ключ для decrypt (in) и encrypt (out)
        self._in_key = bytearray(full_key)
        self._out_key = bytearray(full_key)
        # ВАЖНО: шифрование НЕ включается здесь!
        # Оно включается при первом вызове encrypt() как в L2JMobius

    def decrypt(self, data: bytes) -> bytes:
        """Дешифрует данные (точно как в Encryption.decrypt).

        Args:
            data: Зашифрованные данные.

        Returns:
            Дешифрованные данные.
        """
        if not self._enabled or self._in_key is None:
            return data

        result = bytearray(data)
        size = len(result)
        
        x_or = 0
        for i in range(size):
            encrypted = result[i] & 0xFF
            result[i] = (encrypted ^ (self._in_key[i & 15] & 0xFF) ^ x_or) & 0xFF
            x_or = encrypted

        # Обновляем ключ (shift key)
        old = (self._in_key[8] & 0xFF) | \
              ((self._in_key[9] & 0xFF) << 8) | \
              ((self._in_key[10] & 0xFF) << 16) | \
              ((self._in_key[11] & 0xFF) << 24)
        old += size
        self._in_key[8] = old & 0xFF
        self._in_key[9] = (old >> 8) & 0xFF
        self._in_key[10] = (old >> 16) & 0xFF
        self._in_key[11] = (old >> 24) & 0xFF

        return bytes(result)

    def encrypt(self, data: bytes) -> bytes:
        """Шифрует данные (точно как в Encryption.encrypt).

        Args:
            data: Исходные данные.

        Returns:
            Зашифрованные данные.
        """
        # Если ключ не установлен - отправляем без шифрования
        if self._out_key is None:
            return data

        # Первый вызов encrypt() включает шифрование но НЕ шифрует пакет
        # (как в L2JMobius Encryption.java)
        if not self._enabled:
            self._enabled = True
            return data

        result = bytearray(data)
        size = len(result)
        
        encrypted = 0
        for i in range(size):
            raw = result[i] & 0xFF
            encrypted = (raw ^ (self._out_key[i & 15] & 0xFF) ^ encrypted) & 0xFF
            result[i] = encrypted

        # Обновляем ключ (shift key)
        old = (self._out_key[8] & 0xFF) | \
              ((self._out_key[9] & 0xFF) << 8) | \
              ((self._out_key[10] & 0xFF) << 16) | \
              ((self._out_key[11] & 0xFF) << 24)
        old += size
        self._out_key[8] = old & 0xFF
        self._out_key[9] = (old >> 8) & 0xFF
        self._out_key[10] = (old >> 16) & 0xFF
        self._out_key[11] = (old >> 24) & 0xFF

        return bytes(result)


__all__ = ["GameCrypt", "STATIC_KEY"]
