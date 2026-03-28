#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Пример входа в игру Lineage 2."""

import asyncio
import sys

from l2py import L2Client
from l2py.network.login_flow import LoginError
from l2py.network.game_flow import GameError


async def main() -> int:
    """Основная функция.
    
    Returns:
        0 при успехе, 1 при ошибке.
    """
    client = L2Client()
    
    try:
        session = await client.enter(
            username="qwerty",
            password="qwerty",
            host="192.168.0.33",
            port=2106,
            2,
            char_slot=0,
        )
        print("[OK] Successfully entered the game!")
        print(f"   Character: {session.character.name}")
        print(f"   Level: {session.character.level}")
        print(f"   Coordinates: ({session.character.x}, {session.character.y}, {session.character.z})")
        return 0
        
    except LoginError as e:
        print(f"[ERROR] {e}")
        if "already in use" in str(e).lower():
            print("   [HINT] Wait a few seconds and try again.")
        return 1
        
    except GameError as e:
        print(f"[ERROR] {e}")
        return 1
        
    except asyncio.TimeoutError:
        print("[ERROR] Connection timeout. Server is not responding.")
        print("   [HINT] Check that the server is running and accessible.")
        return 1
        
    except ConnectionError as e:
        print(f"[ERROR] Connection error: {e}")
        print("   [HINT] Check server address and port.")
        return 1
        
    except Exception as e:
        print(f"[ERROR] {e}")
        print("   [HINT] Enable debug mode for diagnostics.")
        import traceback
        traceback.print_exc()
        return 1


if __name__ == "__main__":
    sys.exit(asyncio.run(main()))
