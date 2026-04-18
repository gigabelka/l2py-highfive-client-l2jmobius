
"""Packet inspection and debugging utilities for L2py client.

Provides comprehensive packet analysis tools including hex dumps,
cryptographic validation, and protocol verification.
"""

import logging
from dataclasses import dataclass
from typing import Any, Optional

logger = logging.getLogger(__name__)


@dataclass
class PacketAnalysis:
    """Analysis results for a packet."""
    raw_data: bytes
    decrypted_data: Optional[bytes]
    opcode: Optional[int]
    expected_opcode: Optional[int]
    is_valid: bool
    error_message: Optional[str]
    packet_type: Optional[str]


class PacketInspector:
    """Comprehensive packet inspection and debugging utility."""


    LOGIN_SERVER_OPCODES = {
        0x00: "InitPacket",
        0x01: "LoginFailPacket",
        0x03: "LoginOkPacket",
        0x04: "ServerListPacket",
        0x07: "PlayOkPacket",
        0x0B: "GGAuthPacket",
    }

    GAME_SERVER_OPCODES = {
        0x13: "CharSelectionInfoPacket",
        0x15: "CharSelectedPacket",
        0x2E: "KeyPacket",
        0x32: "UserInfoPacket",
    }

    def __init__(self, enable_detailed_logging: bool = True):
        """Initialize packet inspector.

        Args:
            enable_detailed_logging: Whether to enable detailed packet logging.
        """
        self.enable_detailed_logging = enable_detailed_logging

    def hex_dump(self, data: bytes, title: str = "Packet Data", line_length: int = 16) -> str:
        """Create a formatted hex dump of packet data.

        Args:
            data: Raw packet data to dump.
            title: Title for the hex dump.
            line_length: Number of bytes per line in the dump.

        Returns:
            Formatted hex dump string.
        """
        if not data:
            return f"{title}: <empty>\n"

        lines = [f"{title} ({len(data)} bytes):"]

        for i in range(0, len(data), line_length):
            chunk = data[i:i + line_length]
            hex_part = ' '.join(f'{b:02x}' for b in chunk)
            ascii_part = ''.join(chr(b) if 32 <= b <= 126 else '.' for b in chunk)
            lines.append(f"  {i:04x}: {hex_part:<48} |{ascii_part}|")

        return '\n'.join(lines)

    def analyze_packet(self,
                      raw_data: bytes,
                      decrypted_data: Optional[bytes] = None,
                      expected_opcode: Optional[int] = None,
                      packet_source: str = "unknown") -> PacketAnalysis:
        """Analyze a packet for debugging purposes.

        Args:
            raw_data: Raw packet bytes from network.
            decrypted_data: Decrypted packet data (if available).
            expected_opcode: Expected packet opcode.
            packet_source: Source of packet (login/game server).

        Returns:
            PacketAnalysis with detailed information.
        """
        analysis = PacketAnalysis(
            raw_data=raw_data,
            decrypted_data=decrypted_data,
            opcode=None,
            expected_opcode=expected_opcode,
            is_valid=False,
            error_message=None,
            packet_type=None
        )


        if decrypted_data and len(decrypted_data) > 0:
            analysis.opcode = decrypted_data[0]


            if packet_source.lower() == "login":
                analysis.packet_type = self.LOGIN_SERVER_OPCODES.get(
                    analysis.opcode, f"Unknown Login Packet (0x{analysis.opcode:02X})"
                )
            elif packet_source.lower() == "game":
                analysis.packet_type = self.GAME_SERVER_OPCODES.get(
                    analysis.opcode, f"Unknown Game Packet (0x{analysis.opcode:02X})"
                )
            else:
                analysis.packet_type = f"Unknown Packet (0x{analysis.opcode:02X})"


            if expected_opcode is not None:
                if analysis.opcode == expected_opcode:
                    analysis.is_valid = True
                else:
                    analysis.is_valid = False
                    expected_name = self.LOGIN_SERVER_OPCODES.get(expected_opcode, f"0x{expected_opcode:02X}")
                    analysis.error_message = (
                        f"Opcode mismatch: expected {expected_name} (0x{expected_opcode:02X}), "
                        f"got {analysis.packet_type} (0x{analysis.opcode:02X})"
                    )
        else:
            analysis.error_message = "No decrypted data available for analysis"

        return analysis

    def log_packet_analysis(self, analysis: PacketAnalysis, context: str = ""):
        """Log detailed packet analysis information.

        Args:
            analysis: PacketAnalysis to log.
            context: Additional context for logging.
        """
        if not self.enable_detailed_logging:
            return

        log_lines = []

        if context:
            log_lines.append(f"=== Packet Analysis: {context} ===")
        else:
            log_lines.append("=== Packet Analysis ===")


        log_lines.append(f"Raw packet size: {len(analysis.raw_data)} bytes")
        if analysis.decrypted_data:
            log_lines.append(f"Decrypted size: {len(analysis.decrypted_data)} bytes")

        if analysis.opcode is not None:
            log_lines.append(f"Opcode: 0x{analysis.opcode:02X} ({analysis.packet_type})")

        if analysis.expected_opcode is not None:
            expected_name = self.LOGIN_SERVER_OPCODES.get(analysis.expected_opcode, f"0x{analysis.expected_opcode:02X}")
            log_lines.append(f"Expected: 0x{analysis.expected_opcode:02X} ({expected_name})")

        log_lines.append(f"Valid: {analysis.is_valid}")
        if analysis.error_message:
            log_lines.append(f"Error: {analysis.error_message}")


        log_lines.append("")
        log_lines.append(self.hex_dump(analysis.raw_data, "Raw Data"))

        if analysis.decrypted_data:
            log_lines.append("")
            log_lines.append(self.hex_dump(analysis.decrypted_data, "Decrypted Data"))

        log_lines.append("=" * 50)


        for line in log_lines:
            logger.debug(line)

    def validate_init_packet_structure(self, data: bytes) -> tuple[bool, str]:
        """Validate InitPacket structure for debugging.

        Args:
            data: Decrypted InitPacket data.

        Returns:
            Tuple of (is_valid, error_message).
        """
        if len(data) < 160:
            return False, f"InitPacket too short: {len(data)} bytes, expected ~160"

        try:

            if data[0] != 0x00:
                return False, f"Invalid opcode: 0x{data[0]:02X}, expected 0x00"


            session_id = int.from_bytes(data[1:5], "little")


            protocol_version = int.from_bytes(data[5:9], "little")


            rsa_key = data[9:137]


            blowfish_key = data[144:160]


            if len(rsa_key) != 128:
                return False, f"Invalid RSA key length: {len(rsa_key)}, expected 128"

            if len(blowfish_key) != 16:
                return False, f"Invalid Blowfish key length: {len(blowfish_key)}, expected 16"

            logger.debug(f"InitPacket validation successful:")
            logger.debug(f"  Session ID: 0x{session_id:08X}")
            logger.debug(f"  Protocol Version: {protocol_version} (0x{protocol_version:X})")
            logger.debug(f"  RSA key: {rsa_key[:8].hex()}... (128 bytes)")
            logger.debug(f"  Blowfish key: {blowfish_key.hex()}")

            return True, "InitPacket structure is valid"

        except Exception as e:
            return False, f"InitPacket parsing error: {e}"

    def detect_potential_issues(self, analysis: PacketAnalysis) -> list[str]:
        """Detect potential issues with packet data.

        Args:
            analysis: PacketAnalysis to examine.

        Returns:
            List of potential issues detected.
        """
        issues = []


        if analysis.raw_data and len(analysis.raw_data) < 4:
            issues.append("Packet too short (< 4 bytes)")

        if analysis.decrypted_data is None and analysis.raw_data:
            issues.append("Decryption failed - no decrypted data available")

        if analysis.opcode is not None:

            if analysis.opcode in self.GAME_SERVER_OPCODES and analysis.expected_opcode in self.LOGIN_SERVER_OPCODES:
                issues.append(f"Received Game Server packet (0x{analysis.opcode:02X}) when expecting Login Server packet")


            if analysis.opcode == 0x15 and analysis.expected_opcode == 0x00:
                issues.append("Received CharSelectedPacket (0x15) instead of InitPacket (0x00) - possible connection or decryption issue")


        if analysis.raw_data:

            if len(set(analysis.raw_data)) < 3 and len(analysis.raw_data) > 10:
                issues.append("Raw data shows minimal entropy - possible encryption/decryption issue")

        return issues


def create_inspector(enable_logging: bool = True) -> PacketInspector:
    """Create a packet inspector instance with debug logging configured.

    Args:
        enable_logging: Whether to enable detailed packet logging.

    Returns:
        Configured PacketInspector instance.
    """

    if enable_logging:
        logger.setLevel(logging.DEBUG)
        if not logger.handlers:
            handler = logging.StreamHandler()
            handler.setFormatter(logging.Formatter(
                '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
            ))
            logger.addHandler(handler)

    return PacketInspector(enable_logging)


__all__ = ["PacketInspector", "PacketAnalysis", "create_inspector"]