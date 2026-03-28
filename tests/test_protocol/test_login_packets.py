# -*- coding: utf-8 -*-
"""Тесты для пакетов Login Server."""

import pytest

from l2py.crypto.rsa import L2RSA
from l2py.models.server import GameServer
from l2py.protocol.login.client_packets import (
    AuthGameGuardPacket,
    RequestAuthLoginPacket,
    RequestServerListPacket,
    RequestServerLoginPacket,
)
from l2py.protocol.login.server_packets import (
    GGAuthPacket,
    InitPacket,
    LoginFailPacket,
    LoginOkPacket,
    PlayOkPacket,
    ServerListPacket,
)


class TestServerPackets:
    """Тесты для серверных пакетов."""

    def test_init_packet_parsing(self):
        """Тест парсинга Init пакета."""
        # Создаём мок-данные для Init пакета
        data = (
            b"\x78\x56\x34\x12"  # session_id = 0x12345678
            b"\x0B\x01\x00\x00"  # protocol_version = 267
            + b"\x00" * 128  # rsa_key (128 нулей)
            + b"\x00" * 16  # GG data
            + b"key1234567890123"  # blowfish_key (16 байт)
        )

        packet = InitPacket(data)

        assert packet.session_id == 0x12345678
        assert packet.protocol_version == 267
        assert len(packet.rsa_key) == 128
        assert packet.blowfish_key == b"key1234567890123"

    def test_gg_auth_packet_parsing(self):
        """Тест парсинга GGAuth пакета."""
        data = b"\x01\x00\x00\x00"  # response = 1
        packet = GGAuthPacket(data)
        assert packet.response == 1

    def test_login_ok_packet_parsing(self):
        """Тест парсинга LoginOk пакета."""
        data = (
            b"\x12\x34\x56\x78"  # login_ok1 = 0x78563412
            b"\x87\x65\x43\x21"  # login_ok2 = 0x21436587
        )
        packet = LoginOkPacket(data)
        assert packet.login_ok1 == 0x78563412
        assert packet.login_ok2 == 0x21436587

    def test_play_ok_packet_parsing(self):
        """Тест парсинга PlayOk пакета."""
        data = (
            b"\xAA\xBB\xCC\xDD"  # play_ok1 = 0xDDCCBBAA
            b"\x11\x22\x33\x44"  # play_ok2 = 0x44332211
        )
        packet = PlayOkPacket(data)
        assert packet.play_ok1 == 0xDDCCBBAA
        assert packet.play_ok2 == 0x44332211

    def test_login_fail_packet_parsing(self):
        """Тест парсинга LoginFail пакета."""
        data = b"\x02"  # reason = 2
        packet = LoginFailPacket(data)
        assert packet.reason == 2

    def test_server_list_packet_parsing(self):
        """Тест парсинга ServerList пакета."""
        # Создаём мок-данные для ServerList (1 сервер)
        data = (
            b"\x01"  # count = 1
            b"\x00"  # last_server = 0
            b"\x01"  # server_id = 1
            + b"\x7F\x00\x00\x01"  # IP = 127.0.0.1
            + b"\x30\x75\x00\x00"  # port = 30000
            b"\x00"  # age_limit = 0
            b"\x00"  # is_pvp = 0
            + b"\x64\x00"  # online = 100
            + b"\x90\x01"  # max_online = 400
            b"\x01"  # status = 1
            + b"\x00" * 7  # дополнительные поля
        )

        packet = ServerListPacket(data)

        assert len(packet.servers) == 1
        server = packet.servers[0]
        assert isinstance(server, GameServer)
        assert server.id == 1
        assert server.ip == "127.0.0.1"
        assert server.port == 30000
        assert server.online == 100
        assert server.max_online == 400
        assert server.status is True


class TestClientPackets:
    """Тесты для клиентских пакетов."""

    def test_auth_game_guard_packet(self):
        """Тест AuthGameGuard пакета."""
        packet = AuthGameGuardPacket(session_id=0x12345678)
        data = packet.to_bytes()

        # Опкод + session_id (4) + 16 нулей = 21 байт
        assert data[0] == 0x07  # opcode
        assert data[1:5] == b"\x78\x56\x34\x12"  # session_id LE
        assert data[5:] == b"\x00" * 16  # GG data

    def test_request_auth_login_packet(self):
        """Тест RequestAuthLogin пакета."""
        # Создаём мок RSA
        modulus = b"\x00" * 128
        rsa = L2RSA(modulus)

        packet = RequestAuthLoginPacket(
            username="qwerty",
            password="qwerty",
            session_id=12345,
            rsa=rsa,
        )
        data = packet.to_bytes()

        # Опкод + 128 байт RSA + 4 + 4 + 8 = 145 байт
        assert data[0] == 0x00  # opcode
        assert len(data) == 1 + 128 + 4 + 4 + 8

    def test_request_server_list_packet(self):
        """Тест RequestServerList пакета."""
        packet = RequestServerListPacket(
            login_ok1=0x11111111,
            login_ok2=0x22222222,
        )
        data = packet.to_bytes()

        # Опкод + login_ok1 + login_ok2 + 1 байт = 10 байт
        assert data[0] == 0x05  # opcode
        assert data[1:5] == b"\x11\x11\x11\x11"  # login_ok1
        assert data[5:9] == b"\x22\x22\x22\x22"  # login_ok2
        assert data[9] == 0x05  # unknown byte

    def test_request_server_login_packet(self):
        """Тест RequestServerLogin пакета."""
        packet = RequestServerLoginPacket(
            login_ok1=0x11111111,
            login_ok2=0x22222222,
            server_id=2,
        )
        data = packet.to_bytes()

        # Опкод + login_ok1 + login_ok2 + server_id = 10 байт
        assert data[0] == 0x02  # opcode
        assert data[1:5] == b"\x11\x11\x11\x11"  # login_ok1
        assert data[5:9] == b"\x22\x22\x22\x22"  # login_ok2
        assert data[9] == 0x01  # server_id
