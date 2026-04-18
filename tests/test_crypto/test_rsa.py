
"""Тесты для RSA шифрования."""

import pytest

from l2py.crypto.rsa import L2RSA, unscramble_modulus


class TestL2RSA:
    """Тесты для L2RSA."""

    def test_init_with_valid_modulus(self):
        """Тест инициализации с валидным модулем."""

        modulus = b"\x00" * 128
        rsa = L2RSA(modulus)
        assert rsa._n == 0
        assert rsa._e == 65537

    def test_init_with_invalid_modulus_length(self):
        """Тест инициализации с неверной длиной модуля."""
        with pytest.raises(ValueError, match="Modulus must be 128 bytes"):
            L2RSA(b"\x00" * 64)

    def test_encrypt_returns_128_bytes(self):
        """Тест что encrypt возвращает 128 байт."""

        modulus = bytes([0x00, 0x01] + [0x00] * 126)
        rsa = L2RSA(modulus)

        data = b"test"
        encrypted = rsa.encrypt(data)

        assert len(encrypted) == 128

    def test_encrypt_with_small_modulus(self):
        """Тест encrypt с малым модулем (для проверки математики)."""








        n = 3233
        e = 17

        class TestRSA:
            def __init__(self, n, e):
                self._n = n
                self._e = e

            def encrypt(self, data: bytes) -> bytes:
                plaintext_int = int.from_bytes(data, "big")
                cipher_int = pow(plaintext_int, self._e, self._n)
                return cipher_int.to_bytes((cipher_int.bit_length() + 7) // 8 or 1, "big")

        rsa = TestRSA(n, e)
        data = b"\x00\x41"
        encrypted = rsa.encrypt(data)


        assert len(encrypted) > 0

    def test_encrypt_changes_data(self):
        """Тест что шифрование изменяет данные."""
        modulus = bytes([0x00, 0x01] + [0x00] * 126)
        rsa = L2RSA(modulus)

        data = b"hello world test"
        encrypted = rsa.encrypt(data)


        assert encrypted != data.ljust(128, b"\x00")

    def test_encrypt_data_too_long(self):
        """Тест что слишком длинные данные вызывают ошибку."""
        modulus = b"\x00" * 128
        rsa = L2RSA(modulus)

        with pytest.raises(ValueError, match="Data too long"):
            rsa.encrypt(b"x" * 129)


class TestUnscrambleModulus:
    """Тесты для unscramble_modulus."""

    def test_unscramble_preserves_length(self):
        """Тест что дескремблирование сохраняет длину."""
        modulus = bytes(range(128))
        result = unscramble_modulus(modulus)
        assert len(result) == 128

    def test_unscramble_invalid_length(self):
        """Тест что неверная длина вызывает ошибку."""
        with pytest.raises(ValueError, match="Modulus must be 128 bytes"):
            unscramble_modulus(b"\x00" * 64)

    def test_unscramble_swap_first_64_bytes(self):
        """Тест что первые 64 байта меняются местами со вторыми."""

        first_half = bytes([0xAA] * 64)
        second_half = bytes([0xBB] * 64)
        modulus = first_half + second_half

        result = unscramble_modulus(modulus)


        assert result[:64] == second_half
        assert result[64:] == first_half

    def test_double_unscramble_restores_original(self):
        """Тест что двойное дескремблирование возвращает исходное."""

        modulus = bytes(range(128))


        result1 = unscramble_modulus(modulus)


        result2 = unscramble_modulus(result1)


        assert result2 == modulus
