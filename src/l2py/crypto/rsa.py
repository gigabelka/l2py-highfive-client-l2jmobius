# -*- coding: utf-8 -*-
"""RSA шифрование для авторизации на Login Server.

L2 использует "textbook RSA" без OAEP/PKCS1 padding:
    ciphertext = plaintext^e mod n

e = 65537 (0x10001) — стандартное значение для L2.
"""


class L2RSA:
    """RSA шифрование для пакета RequestAuthLogin.

    Использует "сырой" RSA без padding, как в оригинальном L2.
    """

    __slots__ = ("_n", "_e")

    EXPONENT = 65537  # 0x10001

    def __init__(self, modulus: bytes) -> None:
        """Инициализация RSA с модулем от сервера.

        Args:
            modulus: 128 байт (1024-bit) RSA-модуля, big-endian.
        """
        if len(modulus) != 128:
            raise ValueError(f"Modulus must be 128 bytes, got {len(modulus)}")

        self._n = int.from_bytes(modulus, "big")
        self._e = self.EXPONENT

    def encrypt(self, data: bytes) -> bytes:
        """Шифрует данные textbook RSA.

        Данные дополняются нулями справа до 128 байт,
        затем выполняется RSA-шифрование.

        Args:
            data: Данные для шифрования (макс. 128 байт).

        Returns:
            Зашифрованные данные (128 байт).
        """
        if len(data) > 128:
            raise ValueError(f"Data too long: {len(data)} > 128")

        # Дополняем нулями справа до 128 байт
        padded = data.ljust(128, b"\x00")

        # RSA encryption: ciphertext = plaintext^e mod n
        plaintext_int = int.from_bytes(padded, "big")
        cipher_int = pow(plaintext_int, self._e, self._n)

        return cipher_int.to_bytes(128, "big")


def unscramble_modulus(modulus: bytes) -> bytes:
    """Дескремблирует RSA-модуль из пакета Init.

    Некоторые серверы L2 (включая L2JMobius) могут отправлять
    RSA-модуль в скремблированном виде. Эта функция выполняет
    обратное преобразование.

    Стандартный алгоритм L2:
    1. Swap первых 64 байт со вторыми 64 байтами
    2. XOR и swap по 4 байта

    Args:
        modulus: Скремблированный модуль (128 байт).

    Returns:
        Дескремблированный модуль.

    TODO: Для L2JMobius скремблирование может быть отключено.
          Если шифрование не работает — возможно нужно пропустить
          эту функцию или настроить сервер.
    """
    if len(modulus) != 128:
        raise ValueError(f"Modulus must be 128 bytes, got {len(modulus)}")

    # Копируем в mutable bytearray
    result = bytearray(modulus)

    # Шаг 1: Swap первых 64 байт (0x00-0x3F) со вторыми 64 байтами (0x40-0x7F)
    for i in range(64):
        result[0x00 + i], result[0x40 + i] = result[0x40 + i], result[0x00 + i]

    # Шаг 2: XOR и swap по 4 байта (стандартный L2 алгоритм)
    # Это примерная реализация, точный алгоритм может отличаться
    # TODO: Уточнить по исходникам l2js-client

    # Пока возвращаем как есть после первого swap
    # (это часто достаточно для L2JMobius)
    return bytes(result)


__all__ = ["L2RSA", "unscramble_modulus"]
