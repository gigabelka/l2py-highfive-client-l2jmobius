# -*- coding: utf-8 -*-
"""Тесты для LoginCrypt."""

import pytest

from l2py.crypto.login_crypt import STATIC_BLOWFISH_KEY, LoginCrypt
from l2py.crypto.blowfish import L2Blowfish


class TestLoginCrypt:
    """Тесты для LoginCrypt."""

    def test_init_with_default_key(self):
        """Тест инициализации со статическим ключом по умолчанию."""
        crypt = LoginCrypt()
        assert crypt._static_cipher is not None

    def test_init_with_custom_key(self):
        """Тест инициализации с пользовательским ключом."""
        custom_key = b"custom_key_for_testing"
        crypt = LoginCrypt(custom_key)
        assert crypt._static_cipher is not None

    def test_set_session_key(self):
        """Тест установки сессионного ключа."""
        crypt = LoginCrypt()
        session_key = b"session_key_16by"

        crypt.set_key(session_key)
        assert crypt._key == session_key
        assert crypt._session_cipher is not None

    def test_checksum_calculation(self):
        """Тест вычисления checksum."""
        crypt = LoginCrypt()
        crypt.set_key(b"session_key_16by")

        # Данные: 8 байт данных + 8 байт для checksum
        data = b"\x01\x02\x03\x04" + b"\x00" * 12
        checksum = crypt._checksum(data)

        # Checksum должна быть 32-битным числом
        assert isinstance(checksum, int)
        assert 0 <= checksum <= 0xFFFFFFFF

    def test_checksum_verification(self):
        """Тест проверки checksum."""
        crypt = LoginCrypt()
        crypt.set_key(b"session_key_16by")

        # Данные с правильной checksum
        data = b"\x01\x02\x03\x04\x05\x06\x07\x08"
        checksum = crypt._checksum(data + b"\x00" * 8)
        checksum_bytes = checksum.to_bytes(4, "little")
        data_with_checksum = data + checksum_bytes + b"\x00\x00\x00\x00"

        assert crypt._verify_checksum(data_with_checksum) is True

    def test_checksum_verification_fail(self):
        """Тест проверки checksum с неверными данными."""
        crypt = LoginCrypt()
        crypt.set_key(b"session_key_16by")

        # Данные с неправильной checksum
        data = b"\x01\x02\x03\x04\xFF\xFF\xFF\xFF\x00\x00\x00\x00"

        assert crypt._verify_checksum(data) is False

    def test_encrypt_decrypt_roundtrip(self):
        """Тест encrypt/decrypt roundtrip с checksum."""
        crypt = LoginCrypt()
        crypt.set_key(b"session_key_16by")

        plaintext = b"Hello World!"
        encrypted = crypt.encrypt(plaintext)
        decrypted = crypt.decrypt(encrypted)

        assert decrypted == plaintext

    def test_encrypt_without_key_raises(self):
        """Тест что encrypt без ключа вызывает ошибку."""
        crypt = LoginCrypt()

        with pytest.raises(ValueError, match="Session key not set"):
            crypt.encrypt(b"data")

    def test_decrypt_without_key_raises(self):
        """Тест что decrypt без ключа вызывает ошибку."""
        crypt = LoginCrypt()

        # Создаём фейковые зашифрованные данные
        fake_data = b"\x00" * 16

        with pytest.raises(ValueError, match="Session key not set"):
            crypt.decrypt(fake_data)

    def test_encrypt_produces_different_output(self):
        """Тест что шифрование меняет данные."""
        crypt = LoginCrypt()
        crypt.set_key(b"session_key_16by")

        plaintext = b"Test data"
        encrypted = crypt.encrypt(plaintext)

        assert encrypted != plaintext
        assert len(encrypted) % 8 == 0  # Кратно 8

    def test_decrypt_init(self):
        """Тест дешифрования Init пакета."""
        crypt = LoginCrypt()

        # Создаём тестовые данные
        # Сначала зашифруем что-то статическим ключом
        plaintext = b"\x00" * 32
        encrypted = crypt._static_cipher.encrypt(plaintext)

        # Дешифруем через decrypt_init
        decrypted = crypt.decrypt_init(encrypted)

        # Должно вернуться что-то (XOR может изменить данные)
        # decrypt_init отрезает 8 байт XOR tail, так что длина = 32 - 8 = 24
        assert isinstance(decrypted, bytes)
        assert len(decrypted) == 24  # 32 - 8 (XOR tail)
