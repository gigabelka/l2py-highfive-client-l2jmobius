
"""Криптография для Login Server.

Содержит LoginCrypt — комбинированная система шифрования:
- Первый пакет (Init) шифруется статическим Blowfish + XOR
- Остальные пакеты — Blowfish с сессионным ключом + checksum

Основано на l2js-client: https://github.com/npetrovski/l2js-client
"""

import logging
import struct
from l2py.crypto.blowfish import L2Blowfish

logger = logging.getLogger(__name__)




STATIC_BLOWFISH_KEY = bytes([
    0x6b, 0x60, 0xcb, 0x5b, 0x82, 0xce, 0x90, 0xb1,
    0xcc, 0x2b, 0x6c, 0x55, 0x6c, 0x6c, 0x6c, 0x6c
])



L2J_CLASSIC_KEY = bytes([
    0x6b, 0x60, 0xcb, 0x5b, 0x82, 0xce, 0x90, 0xb1,
    0xcc, 0x2b, 0x6c, 0x55, 0x6c, 0x6c, 0x6c, 0x6c
])


L2JMOBIUS_KEY_V1 = bytes([
    0xC8, 0x27, 0x93, 0x01, 0xA1, 0x6C, 0x31, 0x97,
    0x39, 0xDD, 0x9A, 0x26, 0x91, 0x81, 0x07, 0x9F
])


L2JMOBIUS_KEY_V2 = bytes([
    0x94, 0x35, 0x00, 0x00, 0xa1, 0x6c, 0x54, 0x87,
    0x45, 0xa1, 0x6c, 0x54, 0x87, 0x45, 0xa1, 0x6c
])


NCSOFT_ORIGINAL_KEY = bytes([
    0x94, 0x35, 0x00, 0x00, 0xa1, 0x6c, 0x54, 0x87,
    0x45, 0xa1, 0x6c, 0x54, 0x87, 0x45, 0xa1, 0x6c
])


AVAILABLE_KEYS = {
    "l2js-client": STATIC_BLOWFISH_KEY,
    "l2j-classic": L2J_CLASSIC_KEY,
    "l2jmobius-v1": L2JMOBIUS_KEY_V1,
    "l2jmobius-v2": L2JMOBIUS_KEY_V2,
    "ncsoft-original": NCSOFT_ORIGINAL_KEY,
}


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

        key_name = self.get_current_key_name()
        logger.debug(f"Initialized LoginCrypt with static key: {key_name}")

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

        while pos >= stop:

            edx = data[pos] & 0xff
            edx |= (data[pos + 1] & 0xff) << 8
            edx |= (data[pos + 2] & 0xff) << 16
            edx |= (data[pos + 3] & 0xff) << 24


            edx ^= ecx

            ecx -= edx


            data[pos] = edx & 0xff
            data[pos + 1] = (edx >> 8) & 0xff
            data[pos + 2] = (edx >> 16) & 0xff
            data[pos + 3] = (edx >> 24) & 0xff

            pos -= 4

    def encrypt_init(self, data: bytes) -> bytes:
        """Шифрует Init пакет для имитации сервера.

        Использует XOR + статический Blowfish.

        Args:
            data: Данные для шифрования (без опкода, но с XOR tail).
                  Если XOR tail не передан, он будет добавлен автоматически.

        Returns:
            Зашифрованные байты.
        """

        if len(data) % 8 != 0:

            pass


        encrypted = bytearray(data)


        rnd_xor = struct.unpack("<I", encrypted[-8:-4])[0]



        self._dec_xor_pass(encrypted, 0, len(encrypted), rnd_xor)


        return self._static_cipher.encrypt(bytes(encrypted))

    def decrypt_init(self, data: bytes) -> bytes:
        """Дешифрует Init пакет (первый пакет от сервера).

        Использует статический Blowfish + XOR.
        Алгоритм из l2js-client.

        Args:
            data: Зашифрованные данные.

        Returns:
            Дешифрованные данные (без trailing 8-byte XOR блока).
        """

        decrypted = bytearray(self._static_cipher.decrypt(data))



        rnd_xor = decrypted[-8] & 0xff
        rnd_xor |= (decrypted[-7] << 8) & 0xff00
        rnd_xor |= (decrypted[-6] << 16) & 0xff0000
        rnd_xor |= (decrypted[-5] << 24) & 0xff000000

        self._dec_xor_pass(decrypted, 0, len(decrypted), rnd_xor)


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


        decrypted = bytearray(self._session_cipher.decrypt(data))


        if not self._verify_checksum(decrypted):
            raise RuntimeError("Checksum verification failed")


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



        total_len_with_checksum = len(data) + 4
        padding_needed = (8 - (total_len_with_checksum % 8)) % 8


        padded = bytearray(data)
        padded.extend(b"\x00" * padding_needed)
        padded.extend(b"\x00" * 4)


        checksum = self._checksum(bytes(padded))
        padded[-4:] = struct.pack("<I", checksum)


        return self._session_cipher.encrypt(bytes(padded))

    @classmethod
    def create_with_key(cls, key_name: str) -> "LoginCrypt":
        """Создает LoginCrypt с определенным ключом по имени.

        Args:
            key_name: Имя ключа из AVAILABLE_KEYS.

        Returns:
            LoginCrypt с указанным статическим ключом.

        Raises:
            ValueError: Если ключ не найден.
        """
        if key_name not in AVAILABLE_KEYS:
            available = ", ".join(AVAILABLE_KEYS.keys())
            raise ValueError(f"Unknown key '{key_name}'. Available: {available}")

        return cls(static_key=AVAILABLE_KEYS[key_name])

    def update_static_key(self, key_bytes: bytes) -> None:
        """Обновляет статический Blowfish-ключ.

        Args:
            key_bytes: Новые байты статического ключа.
        """
        self._static_cipher = L2Blowfish(key_bytes)
        key_name = self.get_current_key_name()
        logger.debug(f"Updated LoginCrypt static key to: {key_name}")

    def test_decrypt_with_all_keys(self, encrypted_data: bytes) -> dict[str, tuple[bool, bytes | None, str]]:
        """Тестирует дешифрование с различными статическими ключами.

        Полезно для отладки при неизвестном типе сервера.

        Args:
            encrypted_data: Зашифрованные данные для тестирования.

        Returns:
            Словарь {key_name: (success, decrypted_data, error_msg)}.
        """
        results = {}

        for key_name, key_bytes in AVAILABLE_KEYS.items():
            try:

                temp_cipher = L2Blowfish(key_bytes)
                decrypted = temp_cipher.decrypt(encrypted_data)


                try:
                    decrypted_copy = bytearray(decrypted)


                    rnd_xor = 0
                    rnd_xor |= (decrypted_copy[-8] & 0xff)
                    rnd_xor |= ((decrypted_copy[-7] & 0xff) << 8)
                    rnd_xor |= ((decrypted_copy[-6] & 0xff) << 16)
                    rnd_xor |= (decrypted_copy[-5] << 24) & 0xff000000

                    self._dec_xor_pass(decrypted_copy, 0, len(decrypted_copy), rnd_xor)
                    final_data = bytes(decrypted_copy[:-8])


                    if len(final_data) > 0 and final_data[0] in [0x00, 0x01, 0x03, 0x04, 0x07, 0x0B]:
                        results[key_name] = (True, final_data, "Success with XOR pass")
                    else:
                        results[key_name] = (False, final_data, f"Invalid opcode: 0x{final_data[0]:02X}")
                except Exception as xor_error:
                    results[key_name] = (False, decrypted, f"XOR pass failed: {xor_error}")

            except Exception as decrypt_error:
                results[key_name] = (False, None, f"Decryption failed: {decrypt_error}")

        return results

    def get_current_key_name(self) -> str:
        """Возвращает имя текущего статического ключа (если известно).

        Returns:
            Имя ключа или "unknown".
        """
        current_key = self._static_cipher._key if hasattr(self._static_cipher, '_key') else None

        for name, key_bytes in AVAILABLE_KEYS.items():
            if current_key == key_bytes:
                return name

        return "unknown"


def create_login_crypt_for_l2jmobius(
    key_name: str | None = None, fallback_to_default: bool = True
) -> "LoginCrypt":
    """Создает LoginCrypt оптимизированный для L2JMobius.

    Пробует L2JMobius-специфичные ключи перед стандартным или использует указанный.

    Args:
        key_name: Конкретное имя ключа (опционально).
        fallback_to_default: Использовать стандартный ключ при неудаче.

    Returns:
        LoginCrypt с подходящим ключом для L2JMobius.
    """
    if key_name:
        logger.info(f"Creating LoginCrypt with specific Mobius key: {key_name}")
        return LoginCrypt.create_with_key(key_name)



    preferred_keys = ["l2js-client", "l2j-classic", "l2jmobius-v1", "l2jmobius-v2"]
    logger.debug(f"Attempting to find best static key for L2JMobius among: {preferred_keys}")

    for name in preferred_keys:
        try:
            crypt = LoginCrypt.create_with_key(name)
            logger.info(f"Selected L2JMobius compatible key: {name}")
            return crypt
        except ValueError:
            continue

    if fallback_to_default:
        logger.warning("No suitable Mobius key found, falling back to default static key")
        return LoginCrypt()
    else:
        raise ValueError("No suitable key found for L2JMobius")


__all__ = ["LoginCrypt", "STATIC_BLOWFISH_KEY", "AVAILABLE_KEYS", "create_login_crypt_for_l2jmobius"]
