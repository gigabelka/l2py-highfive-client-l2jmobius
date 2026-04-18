
"""Blowfish шифрование для Login Server.

Реализация ECB режима с блоками по 8 байт.
Используется BlowfishEngine, совместимый с L2JMobius.
"""

from l2py.crypto.blowfish_engine import BlowfishEngine


class L2Blowfish:
    """Blowfish шифрование в ECB режиме.

    Lineage 2 использует Blowfish для шифрования пакетов на Login Server.
    Блоки фиксированного размера (8 байт), данные дополняются нулями.

    Использует BlowfishEngine, портированный из L2JMobius,
    для полной совместимости с сервером.
    """

    __slots__ = ("_engine",)

    BLOCK_SIZE = 8

    def __init__(self, key: bytes) -> None:
        """Инициализация Blowfish с заданным ключом.

        Args:
            key: Ключ шифрования (макс. 56 байт для Blowfish).
        """
        self._engine = BlowfishEngine()
        self._engine.init(key)

    def _pad(self, data: bytes) -> bytes:
        """Дополняет данные до кратности 8 байт.

        Args:
            data: Исходные данные.

        Returns:
            Дополненные данные.
        """
        padding_needed = self.BLOCK_SIZE - (len(data) % self.BLOCK_SIZE)
        if padding_needed != self.BLOCK_SIZE:
            data = data + b"\x00" * padding_needed
        return data

    def encrypt(self, data: bytes) -> bytes:
        """Шифрует данные Blowfish ECB.

        Args:
            data: Данные для шифрования.

        Returns:
            Зашифрованные данные.
        """
        padded = self._pad(data)
        return self._engine.encrypt(padded)

    def decrypt(self, data: bytes) -> bytes:
        """Дешифрует данные Blowfish ECB.

        Args:
            data: Данные для дешифрования (должны быть кратны 8).

        Returns:
            Дешифрованные данные.
        """
        return self._engine.decrypt(data)


__all__ = ["L2Blowfish"]
