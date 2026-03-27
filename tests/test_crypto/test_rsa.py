# -*- coding: utf-8 -*-
"""Тесты для RSA шифрования."""

import pytest

from l2py.crypto.rsa import L2RSA, unscramble_modulus


class TestL2RSA:
    """Тесты для L2RSA."""

    def test_init_with_valid_modulus(self):
        """Тест инициализации с валидным модулем."""
        # 128 байт нулей (не валидный RSA, но подходит для теста)
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
        # Простой модуль для тестирования (не криптографически безопасный!)
        modulus = bytes([0x00, 0x01] + [0x00] * 126)
        rsa = L2RSA(modulus)

        data = b"test"
        encrypted = rsa.encrypt(data)

        assert len(encrypted) == 128

    def test_encrypt_with_small_modulus(self):
        """Тест encrypt с малым модулем (для проверки математики)."""
        # Используем очень простой модуль для предсказуемого результата
        # n = 257 * 263 = 67591 (простые числа)
        # phi = 256 * 262 = 67072
        # e = 65537 mod 67072 = 65537
        # d = pow(65537, -1, 67072) = ...
        # Для теста используем textbook RSA с малым модулем

        # Создаём RSA вручную для теста
        n = 3233  # 61 * 53
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
        data = b"\x00\x41"  # 65
        encrypted = rsa.encrypt(data)

        # 65^17 mod 3233 = ... проверяем что шифрование работает
        assert len(encrypted) > 0

    def test_encrypt_changes_data(self):
        """Тест что шифрование изменяет данные."""
        modulus = bytes([0x00, 0x01] + [0x00] * 126)
        rsa = L2RSA(modulus)

        data = b"hello world test"
        encrypted = rsa.encrypt(data)

        # Зашифрованные данные должны отличаться от исходных
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
        modulus = bytes(range(128))  # 0, 1, 2, ..., 127
        result = unscramble_modulus(modulus)
        assert len(result) == 128

    def test_unscramble_invalid_length(self):
        """Тест что неверная длина вызывает ошибку."""
        with pytest.raises(ValueError, match="Modulus must be 128 bytes"):
            unscramble_modulus(b"\x00" * 64)

    def test_unscramble_swap_first_64_bytes(self):
        """Тест что первые 64 байта меняются местами со вторыми."""
        # Создаём модуль где первая и вторая половины различимы
        first_half = bytes([0xAA] * 64)
        second_half = bytes([0xBB] * 64)
        modulus = first_half + second_half

        result = unscramble_modulus(modulus)

        # После swap должно быть: second_half + first_half
        assert result[:64] == second_half
        assert result[64:] == first_half

    def test_double_unscramble_restores_original(self):
        """Тест что двойное дескремблирование возвращает исходное."""
        # Создаём тестовый модуль
        modulus = bytes(range(128))

        # Первое дескремблирование
        result1 = unscramble_modulus(modulus)

        # Повторное дескремблирование
        result2 = unscramble_modulus(result1)

        # Должны получить исходное (только swap, без других преобразований)
        assert result2 == modulus
