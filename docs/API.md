# Внешний API l2py (HTTP + WebSocket)

При запуске `python main.py` вместе с игровой сессией поднимается FastAPI-сервер.
При `Ctrl+C` / выходе сервер корректно гасится вместе с клиентом.

- Хост/порт по умолчанию: `127.0.0.1:8000` (переопределяется `L2PY_API_HOST` / `L2PY_API_PORT`).
- **Swagger UI**: http://127.0.0.1:8000/docs — все методы описаны и доступны для ручного вызова.
- **WebSocket стрим входящих пакетов**: `ws://127.0.0.1:8000/ws/packets`. Каждое сообщение — JSON вида
  `{"opcode": "0xNN", "hex": "...", "len": N, "source": "game"}`.

## Эндпоинты

| Метод  | Путь                      | Тело                                                                    | Что делает                                                                                                                       |
| ------ | ------------------------- | ----------------------------------------------------------------------- | -------------------------------------------------------------------------------------------------------------------------------- |
| `GET`  | `/api/status`             | —                                                                       | Возвращает состояние: имя, objectId, координаты, последнюю выбранную цель                                                        |
| `GET`  | `/api/action/sit-stand`   | —                                                                       | `RequestActionUse 0x56` с `action_id=0` — сесть/встать                                                                           |
| `GET`  | `/api/action/attack/{id}` | —                                                                       | `AttackRequest 0x32` по `id` (origin берётся из трекнутой позиции персонажа)                                                     |
| `GET`  | `/api/action/pick-up/{id}`| —                                                                       | `Action 0x1F` на предмет на земле с objectId `id`                                                                                |
| `GET`  | `/api/action/next-target` | —                                                                       | Выбирает ближайшего attackable NPC из кэша `NpcInfo 0x16`, шлёт `Action 0x1F`, ждёт `MyTargetSelected 0xA6` (таймаут 1.5с) и возвращает `{id: int}`. `409` — кэш пуст, `504` — сервер не подтвердил |
| `GET`  | `/api/key/f{N}` (N=1..12) | —                                                                       | Резолвит слот `N-1` action-bar (page 0) по `ShortCutInit 0x45` / `ShortCutRegister 0x44` и шлёт соответствующий пакет: ACTION→`0x56`, SKILL→`0x39`, ITEM→`0x19`. `404`, если слот пуст |
| `WS`   | `/ws/packets`             | —                                                                       | Стрим входящих игровых пакетов                                                                                                   |

## Примеры

См. [EXAMPLES.md](EXAMPLES.md).

## Ограничения MVP

- `Next Target`: выбирает ближайшего attackable NPC из кэша видимых `NpcInfo 0x16` (фильтр по флагу attackable, self-id исключён), отправляет `Action 0x1F` и синхронно ждёт `MyTargetSelected 0xA6` с таймаутом 1.5с. Round-robin не делает — повторный вызов на том же моб-е вернёт тот же id; после `DeleteObject 0x08` моб выпадает из кэша.
- `F1–F12`: раскладка action-bar читается из серверных `ShortCutInit 0x45` / `ShortCutRegister 0x44` (page 0, slot = N−1). Поддерживаются типы ACTION/SKILL/ITEM; MACRO/RECIPE/BOOKMARK возвращают `409`.
- `Attack` / `Pick Up` требуют, чтобы клиент уже получил хотя бы один `UserInfo` (позиция персонажа закэширована) — иначе вернётся `409`.
