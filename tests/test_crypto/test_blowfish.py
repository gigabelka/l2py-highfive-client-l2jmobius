
"""Тесты для Blowfish шифрования."""

import pytest

from l2py.crypto.blowfish import L2Blowfish


class TestL2Blowfish:
    """Тесты для L2Blowfish."""

    def test_encrypt_decrypt_roundtrip(self):
        """Тест encrypt/decrypt roundtrip."""
        key = b"test_key_12345"
        cipher = L2Blowfish(key)


        plaintext = b"abcdefgh"
        encrypted = cipher.encrypt(plaintext)
        decrypted = cipher.decrypt(encrypted)

        assert len(encrypted) == 8
        assert decrypted == plaintext

    def test_encrypt_decrypt_with_padding(self):
        """Тест encrypt с автоматическим padding'ом."""
        key = b"test_key_12345"
        cipher = L2Blowfish(key)


        plaintext = b"hello"
        encrypted = cipher.encrypt(plaintext)
        decrypted = cipher.decrypt(encrypted)

        assert len(encrypted) == 8
        assert decrypted[:5] == plaintext
        assert decrypted[5:] == b"\x00" * 3

    def test_different_keys_produce_different_ciphertexts(self):
        """Тест что разные ключи дают разный результат."""
        plaintext = b"testdata"

        cipher1 = L2Blowfish(b"key_one_123456")
        cipher2 = L2Blowfish(b"key_two_123456")

        encrypted1 = cipher1.encrypt(plaintext)
        encrypted2 = cipher2.encrypt(plaintext)

        assert encrypted1 != encrypted2

    def test_static_key(self):
        """Тест со статическим ключом L2."""
        from l2py.crypto.login_crypt import STATIC_BLOWFISH_KEY

        cipher = L2Blowfish(STATIC_BLOWFISH_KEY)

        plaintext = b"\x00" * 8
        encrypted = cipher.encrypt(plaintext)
        decrypted = cipher.decrypt(encrypted)

        assert len(encrypted) == 8
        assert decrypted == plaintext

    def test_multi_block_encryption(self):
        """Тест шифрования данных размером несколько блоков."""
        key = b"test_key_12345"
        cipher = L2Blowfish(key)


        plaintext = b"0123456789ABCDEFGHIJKLMN"
        encrypted = cipher.encrypt(plaintext)
        decrypted = cipher.decrypt(encrypted)

        assert len(encrypted) == 24
        assert decrypted == plaintext
