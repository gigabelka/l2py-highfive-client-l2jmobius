# Рекомендуемые исправления для входа в игру

## Проблема
После отправки AuthLogin пакета на Game Server, сервер сразу закрывает соединение.

## Возможные решения

### 1. Проверить коммуникацию Game Server <-> Login Server

Проверить логи Game Server на наличие ошибок подключения к Login Server.

**Конфигурация Game Server** (`dist/game/config/Server.ini`):
```ini
LoginHost = 127.0.0.1  # Должен указывать на Login Server
LoginPort = 9014
RequestServerID = 1    # ID который запрашивает Game Server
```

**Конфигурация Login Server** (`dist/login/config/Server.ini`):
```ini
AcceptNewGameServer = True
```

### 2. Исправить формат AuthLogin пакета

В файле `src/l2py/protocol/game/client_packets.py` метод `_write()` класса `AuthLoginPacket`:

```python
def _write(self) -> None:
    """Записывает поля пакета."""
    # TODO: Проверить кодировку строки
    # Возможно нужен одинарный null-terminator (UTF-8) вместо двойного (UTF-16LE)
    # Или строка должна быть фиксированной длины (16 байт)
    self._writer.write_string(self.login)
    self._writer.write_uint32(self.play_ok2)
    self._writer.write_uint32(self.play_ok1)
    self._writer.write_uint32(self.login_ok1)
    self._writer.write_uint32(self.login_ok2)
```

### 3. Проверить XOR шифрование

Убедиться что первый пакет после включения шифрования (AuthLogin) 
правильно шифруется/дешифруется.

В файле `src/l2py/crypto/game_crypt.py`:
- Проверить алгоритм encrypt/decrypt
- Проверить обновление ключа после каждой операции

### 4. Проверить Protocol Version

Убедиться что используется правильная версия протокола (267 или 273).

В файле `src/l2py/protocol/game/client_packets.py`:
```python
HIGH_FIVE_PROTOCOL = 273  # или 267
```

## Текущие исправления

Уже применены:
1. ✅ Protocol Version изменена на 273
2. ✅ Server ID изменён на 2 (соответствует списку серверов)
3. ✅ Строка в AuthLogin отправляется с дополнительным padding до 16 байт

## Для проверки

Запустить тест:
```bash
python main.py
```

Ожидаемый результат:
```
[OK] Successfully entered the game!
   Character: <имя_персонажа>
   Level: <уровень>
```
