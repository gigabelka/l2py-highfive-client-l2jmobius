
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

    EXPONENT = 65537

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


        padded = data.ljust(128, b"\x00")


        plaintext_int = int.from_bytes(padded, "big")
        cipher_int = pow(plaintext_int, self._e, self._n)

        return cipher_int.to_bytes(128, "big")


def unscramble_modulus(modulus: bytes, full_descramble: bool = True) -> bytes:
    """Дескремблирует RSA-модуль из пакета Init (L2JMobius алгоритм).

    L2JMobius использует специфический алгоритм scramble:
    https://github.com/L2JMobius/L2J_Mobius/blob/master/java/org/l2jmobius/loginserver/network/ScrambledKeyPair.java

    Алгоритм descramble (обратный scramble):
    1. XOR last 0x40 bytes with first 0x40 bytes (reverse Step 4)
    2. XOR bytes 0x0d-0x10 with bytes 0x34-0x38 (reverse Step 3)
    3. XOR first 0x40 bytes with last 0x40 bytes (reverse Step 2)
    4. Swap 0x4d-0x50 <-> 0x00-0x04 (reverse Step 1)

    Args:
        modulus: Скремблированный модуль (128 байт).
        full_descramble: Не используется, сохранено для совместимости.

    Returns:
        Дескремблированный модуль.
    """
    if len(modulus) != 128:
        raise ValueError(f"Modulus must be 128 bytes, got {len(modulus)}")


    result = bytearray(modulus)


    for i in range(0x40):
        result[0x40 + i] = (result[0x40 + i] ^ result[i]) & 0xff


    for i in range(4):
        result[0x0d + i] = (result[0x0d + i] ^ result[0x34 + i]) & 0xff


    for i in range(0x40):
        result[i] = (result[i] ^ result[0x40 + i]) & 0xff


    for i in range(4):
        result[0x00 + i], result[0x4d + i] = result[0x4d + i], result[0x00 + i]

    return bytes(result)


def test_rsa_descrambling(modulus: bytes) -> dict[str, tuple[bool, bytes, str]]:
    """Тестирует различные варианты дескремблирования RSA модуля.

    Полезно для определения правильного алгоритма для конкретного сервера.

    Args:
        modulus: Исходный RSA модуль (128 байт).

    Returns:
        Словарь {method_name: (appears_valid, descrambled_data, description)}.
    """
    results = {}


    try:
        results["no_descramble"] = (
            _is_valid_rsa_modulus(modulus),
            modulus,
            "Original modulus without any descrambling"
        )
    except Exception as e:
        results["no_descramble"] = (False, modulus, f"Error: {e}")


    try:
        partial_descrambled = unscramble_modulus(modulus, full_descramble=False)
        results["block_swap_only"] = (
            _is_valid_rsa_modulus(partial_descrambled),
            partial_descrambled,
            "Only 64-byte block swap (L2JMobius compatible)"
        )
    except Exception as e:
        results["block_swap_only"] = (False, b"", f"Error: {e}")


    try:
        full_descrambled = unscramble_modulus(modulus, full_descramble=True)
        results["full_descramble"] = (
            _is_valid_rsa_modulus(full_descrambled),
            full_descrambled,
            "Full descrambling with XOR and 4-byte swaps"
        )
    except Exception as e:
        results["full_descramble"] = (False, b"", f"Error: {e}")

    return results


def _is_valid_rsa_modulus(modulus: bytes) -> bool:
    """Проверяет, выглядит ли RSA модуль валидным.

    Простые эвристики для определения корректности модуля.

    Args:
        modulus: RSA модуль для проверки.

    Returns:
        True, если модуль выглядит валидным.
    """
    if len(modulus) != 128:
        return False


    modulus_int = int.from_bytes(modulus, "big")


    if modulus_int % 2 == 0:
        return False


    if modulus_int < (1 << 1023):
        return False


    if modulus_int == 0 or modulus == b"\xff" * 128:
        return False


    unique_bytes = len(set(modulus))
    if unique_bytes < 10:
        return False

    return True


def create_l2rsa_with_auto_descramble(raw_modulus: bytes) -> "L2RSA":
    """Создает L2RSA с дескремблированием для L2JMobius.

    L2JMobius использует специфический алгоритм scramble для RSA модуля.
    Эта функция всегда применяет правильный descramble алгоритм.

    Args:
        raw_modulus: Сырой RSA модуль из Init пакета.

    Returns:
        L2RSA с дескремблированным модулем.
    """
    import logging
    logger = logging.getLogger(__name__)

    descrambled = unscramble_modulus(raw_modulus)
    logger.debug("RSA: Applied L2JMobius descrambling")
    return L2RSA(descrambled)


__all__ = ["L2RSA", "unscramble_modulus", "test_rsa_descrambling", "create_l2rsa_with_auto_descramble"]
