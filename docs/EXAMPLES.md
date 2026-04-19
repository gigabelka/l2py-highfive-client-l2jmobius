# Примеры использования l2py

## Быстрый старт

```python
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
```

## Примеры HTTP / WebSocket API

```bash
# Сесть / встать
curl http://127.0.0.1:8000/api/action/sit-stand

# Атака по objectId 268440938
curl http://127.0.0.1:8000/api/action/attack/268440938

# F1 — шлёт пакет, соответствующий слоту 0 action-bar (page 0), как в клиенте
curl http://127.0.0.1:8000/api/key/f1

# Подписка на стрим пакетов
websocat ws://127.0.0.1:8000/ws/packets
```
