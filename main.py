import asyncio
from l2py import L2Client

async def main():
    client = L2Client()
    session = await client.enter(
        username="qwerty",
        password="qwerty",
        host="192.168.0.33",
        port=2106,
        server_id=2,
        char_slot=0,
    )
    print(f"Вошёл в игру: {session.character.name}")
    print(f"Уровень: {session.character.level}")
    print(f"Координаты: ({session.character.x}, {session.character.y}, {session.character.z})")

if __name__ == "__main__":
    asyncio.run(main())