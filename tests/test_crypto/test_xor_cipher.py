# -*- coding: utf-8 -*-
"""Тесты для XOR-шифрования Game Server."""

import pytest

from l2py.crypto.game_crypt import STATIC_KEY, GameCrypt


class TestGameCrypt:
    """Тесты для GameCrypt."""

    def test_init_disabled(self):
        """Тест что по умолчанию шифрование выключено."""
        crypt = GameCrypt()
        assert crypt.enabled is False

    def test_set_key_enables_encryption(self):
        """Тест что set_key включает шифрование."""
        crypt = GameCrypt()
        crypt.set_key(b"\x01\x02\x03\x04\x05\x06\x07\x08")
        assert crypt.enabled is True

    def test_set_key_invalid_length(self):
        """Тест что неверная длина ключа вызывает ошибку."""
        crypt = GameCrypt()

        with pytest.raises(ValueError, match="Dynamic key must be 8 bytes"):
            crypt.set_key(b"\x00" * 7)

        with pytest.raises(ValueError, match="Dynamic key must be 8 bytes"):
            crypt.set_key(b"\x00" * 9)

    def test_decrypt_disabled_passthrough(self):
        """Тест что decrypt без set_key возвращает как есть."""
        crypt = GameCrypt()
        data = b"hello world"

        result = crypt.decrypt(data)
        assert result == data

    def test_encrypt_disabled_passthrough(self):
        """Тест что encrypt без set_key возвращает как есть."""
        crypt = GameCrypt()
        data = b"hello world"

        result = crypt.encrypt(data)
        assert result == data

    def test_encrypt_decrypt_roundtrip(self):
        """Тест encrypt → decrypt roundtrip (со второго пакета)."""
        crypt = GameCrypt()
        crypt.set_key(b"\x01\x02\x03\x04\x05\x06\x07\x08")

        plaintext = b"Hello World!"
        # Первый encrypt не шифрует (возвращает как есть)
        first = crypt.encrypt(plaintext)
        assert first == plaintext
        # Второй encrypt шифрует
        encrypted = crypt.encrypt(plaintext)
        assert encrypted != plaintext
        # decrypt всегда расшифровывает
        decrypted = crypt.decrypt(encrypted)
        assert decrypted == plaintext

    def test_encrypt_changes_data(self):
        """Тест что шифрование изменяет данные (со второго пакета)."""
        crypt = GameCrypt()
        crypt.set_key(b"\x01\x02\x03\x04\x05\x06\x07\x08")

        plaintext = b"TestData1234"
        # Первый пакет не шифруется (как в L2JMobius)
        first = crypt.encrypt(plaintext)
        assert first == plaintext
        # Второй пакет шифруется
        encrypted = crypt.encrypt(plaintext)
        assert encrypted != plaintext

    def test_key_changes_after_operation(self):
        """Тест что ключ изменяется после операции (со второго пакета)."""
        crypt = GameCrypt()
        crypt.set_key(b"\x01\x02\x03\x04\x05\x06\x07\x08")

        # Сохраняем состояние ключа
        key_before = list(crypt._encrypt_key)

        # Первый пакет не меняет ключ
        crypt.encrypt(b"test")
        assert list(crypt._encrypt_key) == key_before

        # Второй пакет меняет ключ
        crypt.encrypt(b"test")
        assert list(crypt._encrypt_key) != key_before

    def test_key_increments_after_bytes(self):
        """Тест что байты 8-11 ключа инкрементируются (со второго пакета)."""
        crypt = GameCrypt()
        crypt.set_key(b"\x00" * 8)

        # Начальное значение байт 8-11
        initial_counter = int.from_bytes(crypt._encrypt_key[8:12], "little")

        # Первый пакет не меняет ключ
        crypt.encrypt(b"abcd")  # 4 байта
        assert int.from_bytes(crypt._encrypt_key[8:12], "little") == initial_counter

        # Счётчик должен увеличиться на 4 со второго пакета
        crypt.encrypt(b"abcd")  # 4 байта
        new_counter = int.from_bytes(crypt._encrypt_key[8:12], "little")
        assert new_counter == initial_counter + 4

    def test_encrypt_decrypt_keys_independent(self):
        """Тест что encrypt и decrypt используют независимые ключи."""
        crypt = GameCrypt()
        crypt.set_key(b"\x01\x02\x03\x04\x05\x06\x07\x08")

        # Сохраняем начальные состояния
        encrypt_key_before = list(crypt._encrypt_key)
        decrypt_key_before = list(crypt._decrypt_key)

        # Первый encrypt не меняет ключ (как в L2JMobius)
        crypt.encrypt(b"test")
        assert list(crypt._encrypt_key) == encrypt_key_before

        # Второй encrypt меняет ключ
        crypt.encrypt(b"test")
        assert list(crypt._encrypt_key) != encrypt_key_before

        # Decrypt ключ не изменился
        assert list(crypt._decrypt_key) == decrypt_key_before

    def test_multiple_encrypt_calls(self):
        """Тест нескольких вызовов encrypt (первый не шифруется)."""
        crypt = GameCrypt()
        crypt.set_key(b"\x01\x02\x03\x04\x05\x06\x07\x08")

        # Несколько пакетов
        plaintext1 = b"Packet1"
        plaintext2 = b"Packet2Data"
        plaintext3 = b"P3"

        encrypted1 = crypt.encrypt(plaintext1)
        encrypted2 = crypt.encrypt(plaintext2)
        encrypted3 = crypt.encrypt(plaintext3)

        # Первый пакет не шифруется (как в L2JMobius)
        assert encrypted1 == plaintext1
        # Остальные шифруются
        assert encrypted2 != plaintext2
        assert encrypted3 != plaintext3

        # Зашифрованные данные должны отличаться друг от друга
        assert encrypted2 != encrypted3

    def test_long_data(self):
        """Тест обработки длинных данных (больше ключа)."""
        crypt = GameCrypt()
        crypt.set_key(b"\x01\x02\x03\x04\x05\x06\x07\x08")

        # Данные длиннее 16 байт (длина ключа)
        plaintext = b"A" * 100
        # Первый encrypt не шифрует
        first = crypt.encrypt(plaintext)
        assert first == plaintext
        # Второй encrypt шифрует
        encrypted = crypt.encrypt(plaintext)
        assert len(encrypted) == 100
        assert encrypted != plaintext
        # decrypt всегда расшифровывает
        decrypted = crypt.decrypt(encrypted)
        assert decrypted == plaintext

    def test_empty_data(self):
        """Тест обработки пустых данных."""
        crypt = GameCrypt()
        crypt.set_key(b"\x01\x02\x03\x04\x05\x06\x07\x08")

        encrypted = crypt.encrypt(b"")
        decrypted = crypt.decrypt(b"")

        assert encrypted == b""
        assert decrypted == b""


class TestStaticKey:
    """Тесты для статического ключа."""

    def test_static_key_length(self):
        """Тест что статический ключ имеет правильную длину."""
        assert len(STATIC_KEY) == 8

    def test_static_key_values(self):
        """Тест значений статического ключа."""
        expected = bytes([0xC8, 0x27, 0x93, 0x01, 0xA1, 0x6C, 0x31, 0x97])
        assert STATIC_KEY == expected
