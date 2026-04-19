

"""Пример входа в игру Lineage 2 с поднятием внешнего HTTP/WS API."""

import asyncio
import os
import sys

from l2py import L2Client
from l2py.api import ApiServer, ApiState
from l2py.network.game_flow import GameError
from l2py.network.login_flow import LoginError


def _api_bind() -> tuple[str, int]:
    host = os.environ.get("L2PY_API_HOST", "127.0.0.1")
    port = int(os.environ.get("L2PY_API_PORT", "8000"))
    return host, port


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
            server_id=2,
            char_slot=0,
        )
        print("[OK] Successfully entered the game!")
        print(f"   Character: {session.character.name}")
        print(f"   Level: {session.character.level}")
        print(f"   Coordinates: ({session.character.x}, {session.character.y}, {session.character.z})")

        state = ApiState(session=session)
        state.self_object_id = session.character.object_id
        state.self_x = session.character.x
        state.self_y = session.character.y
        state.self_z = session.character.z
        session.emitter = state.emitter

        api_host, api_port = _api_bind()
        api = ApiServer(state, host=api_host, port=api_port)

        print(f"   External API: http://{api_host}:{api_port}  (Swagger: /docs, WS: /ws/packets)")
        print("   Holding session alive (Ctrl+C to exit)...")

        try:
            async with asyncio.TaskGroup() as tg:
                tg.create_task(session.run_keepalive(), name="keepalive")
                tg.create_task(api.serve(), name="api")
        except* KeyboardInterrupt:
            print("\n[OK] Interrupted, closing session.")
        except* asyncio.CancelledError:
            print("\n[OK] Cancelled, closing session.")
        finally:
            await api.shutdown()
            await session.connection.close()
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
    try:
        sys.exit(asyncio.run(main()))
    except KeyboardInterrupt:
        sys.exit(0)
