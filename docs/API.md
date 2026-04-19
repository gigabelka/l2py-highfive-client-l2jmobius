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
| `POST` | `/api/action/sit-stand`   | `{ctrl?: bool, shift?: bool}`                                           | `RequestActionUse 0x56` с `action_id=0` — сесть/встать                                                                           |
| `POST` | `/api/action/attack`      | `{object_id: int, shift?: bool}`                                        | `AttackRequest 0x32` по цели (origin берётся из трекнутой позиции персонажа)                                                     |
| `POST` | `/api/action/pick-up`     | `{object_id: int}`                                                      | `Action 0x1F` на предмет на земле                                                                                                |
| `POST` | `/api/action/next-target` | `{object_id: int}`                                                      | `Action 0x1F` на заданный objectId. Выбор «следующей» цели — клиентская логика, вызывающий сам определяет её                     |
| `POST` | `/api/key/f{N}` (N=1..12) | `{type: "ACTION"\|"SKILL"\|"ITEM", id: int, ctrl?: bool, shift?: bool}` | MVP: вызывающий задаёт биндинг F-клавиши. ACTION→`RequestActionUse 0x56`, SKILL→`RequestMagicSkillUse 0x39`, ITEM→`UseItem 0x19` |
| `WS`   | `/ws/packets`             | —                                                                       | Стрим входящих игровых пакетов                                                                                                   |

## Примеры

См. [EXAMPLES.md](EXAMPLES.md).

## Ограничения MVP

- `Next Target`: логика перебора целей на стороне вызывающего — эндпоинт принимает готовый `object_id`.
- `F1–F12`: автоматическое разрешение shortcut bar (серверные `ShortcutInit`/`ShortcutRegister`) ещё не реализовано; биндинг передаётся в теле запроса.
- `Attack` / `Pick Up` требуют, чтобы клиент уже получил хотя бы один `UserInfo` (позиция персонажа закэширована) — иначе вернётся `409`.
