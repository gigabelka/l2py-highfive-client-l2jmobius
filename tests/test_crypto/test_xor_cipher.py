
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

        first = crypt.encrypt(plaintext)
        assert first == plaintext

        encrypted = crypt.encrypt(plaintext)
        assert encrypted != plaintext

        decrypted = crypt.decrypt(encrypted)
        assert decrypted == plaintext

    def test_encrypt_changes_data(self):
        """Тест что шифрование изменяет данные (со второго пакета)."""
        crypt = GameCrypt()
        crypt.set_key(b"\x01\x02\x03\x04\x05\x06\x07\x08")

        plaintext = b"TestData1234"

        first = crypt.encrypt(plaintext)
        assert first == plaintext

        encrypted = crypt.encrypt(plaintext)
        assert encrypted != plaintext

    def test_key_changes_after_operation(self):
        """Тест что ключ изменяется после операции (со второго пакета)."""
        crypt = GameCrypt()
        crypt.set_key(b"\x01\x02\x03\x04\x05\x06\x07\x08")


        key_before = list(crypt._encrypt_key)


        crypt.encrypt(b"test")
        assert list(crypt._encrypt_key) == key_before


        crypt.encrypt(b"test")
        assert list(crypt._encrypt_key) != key_before

    def test_key_increments_after_bytes(self):
        """Тест что байты 8-11 ключа инкрементируются (со второго пакета)."""
        crypt = GameCrypt()
        crypt.set_key(b"\x00" * 8)


        initial_counter = int.from_bytes(crypt._encrypt_key[8:12], "little")


        crypt.encrypt(b"abcd")
        assert int.from_bytes(crypt._encrypt_key[8:12], "little") == initial_counter


        crypt.encrypt(b"abcd")
        new_counter = int.from_bytes(crypt._encrypt_key[8:12], "little")
        assert new_counter == initial_counter + 4

    def test_encrypt_decrypt_keys_independent(self):
        """Тест что encrypt и decrypt используют независимые ключи."""
        crypt = GameCrypt()
        crypt.set_key(b"\x01\x02\x03\x04\x05\x06\x07\x08")


        encrypt_key_before = list(crypt._encrypt_key)
        decrypt_key_before = list(crypt._decrypt_key)


        crypt.encrypt(b"test")
        assert list(crypt._encrypt_key) == encrypt_key_before


        crypt.encrypt(b"test")
        assert list(crypt._encrypt_key) != encrypt_key_before


        assert list(crypt._decrypt_key) == decrypt_key_before

    def test_multiple_encrypt_calls(self):
        """Тест нескольких вызовов encrypt (первый не шифруется)."""
        crypt = GameCrypt()
        crypt.set_key(b"\x01\x02\x03\x04\x05\x06\x07\x08")


        plaintext1 = b"Packet1"
        plaintext2 = b"Packet2Data"
        plaintext3 = b"P3"

        encrypted1 = crypt.encrypt(plaintext1)
        encrypted2 = crypt.encrypt(plaintext2)
        encrypted3 = crypt.encrypt(plaintext3)


        assert encrypted1 == plaintext1

        assert encrypted2 != plaintext2
        assert encrypted3 != plaintext3


        assert encrypted2 != encrypted3

    def test_long_data(self):
        """Тест обработки длинных данных (больше ключа)."""
        crypt = GameCrypt()
        crypt.set_key(b"\x01\x02\x03\x04\x05\x06\x07\x08")


        plaintext = b"A" * 100

        first = crypt.encrypt(plaintext)
        assert first == plaintext

        encrypted = crypt.encrypt(plaintext)
        assert len(encrypted) == 100
        assert encrypted != plaintext

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
