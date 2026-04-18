
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

        data = (
            b"\x78\x56\x34\x12"
            b"\x0B\x01\x00\x00"
            + b"\x00" * 128
            + b"\x00" * 16
            + b"key1234567890123"
        )

        packet = InitPacket(data)

        assert packet.session_id == 0x12345678
        assert packet.protocol_version == 267
        assert len(packet.rsa_key) == 128
        assert packet.blowfish_key == b"key1234567890123"

    def test_gg_auth_packet_parsing(self):
        """Тест парсинга GGAuth пакета."""
        data = b"\x01\x00\x00\x00"
        packet = GGAuthPacket(data)
        assert packet.response == 1

    def test_login_ok_packet_parsing(self):
        """Тест парсинга LoginOk пакета."""
        data = (
            b"\x12\x34\x56\x78"
            b"\x87\x65\x43\x21"
        )
        packet = LoginOkPacket(data)
        assert packet.login_ok1 == 0x78563412
        assert packet.login_ok2 == 0x21436587

    def test_play_ok_packet_parsing(self):
        """Тест парсинга PlayOk пакета."""
        data = (
            b"\xAA\xBB\xCC\xDD"
            b"\x11\x22\x33\x44"
        )
        packet = PlayOkPacket(data)
        assert packet.play_ok1 == 0xDDCCBBAA
        assert packet.play_ok2 == 0x44332211

    def test_login_fail_packet_parsing(self):
        """Тест парсинга LoginFail пакета."""
        data = b"\x02"
        packet = LoginFailPacket(data)
        assert packet.reason == 2

    def test_server_list_packet_parsing(self):
        """Тест парсинга ServerList пакета."""

        data = (
            b"\x01"
            b"\x00"
            b"\x01"
            + b"\x7F\x00\x00\x01"
            + b"\x30\x75\x00\x00"
            b"\x00"
            b"\x00"
            + b"\x64\x00"
            + b"\x90\x01"
            b"\x01"
            + b"\x00" * 7
        )

        packet = ServerListPacket(data)

        assert len(packet.servers) == 1
        server = packet.servers[0]
        assert isinstance(server, GameServer)
        assert server.id == 2
        assert server.ip == "192.168.0.33"
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


        assert data[0] == 0x07
        assert data[1:5] == b"\x78\x56\x34\x12"
        assert data[5:] == b"\x00" * 16

    def test_request_auth_login_packet(self):
        """Тест RequestAuthLogin пакета."""

        modulus = b"\x00" * 128
        rsa = L2RSA(modulus)

        packet = RequestAuthLoginPacket(
            username="qwerty",
            password="qwerty",
            session_id=12345,
            rsa=rsa,
        )
        data = packet.to_bytes()


        assert data[0] == 0x00
        assert len(data) == 1 + 128 + 4 + 4 + 8

    def test_request_server_list_packet(self):
        """Тест RequestServerList пакета."""
        packet = RequestServerListPacket(
            login_ok1=0x11111111,
            login_ok2=0x22222222,
        )
        data = packet.to_bytes()


        assert data[0] == 0x05
        assert data[1:5] == b"\x11\x11\x11\x11"
        assert data[5:9] == b"\x22\x22\x22\x22"
        assert data[9] == 0x05

    def test_request_server_login_packet(self):
        """Тест RequestServerLogin пакета."""
        packet = RequestServerLoginPacket(
            login_ok1=0x11111111,
            login_ok2=0x22222222,
            server_id=2,
        )
        data = packet.to_bytes()


        assert data[0] == 0x02
        assert data[1:5] == b"\x11\x11\x11\x11"
        assert data[5:9] == b"\x22\x22\x22\x22"
        assert data[9] == 0x01
