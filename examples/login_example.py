# -*- coding: utf-8 -*-
"""Пример использования l2py для входа в игру.

Этот скрипт демонстрирует базовое использование клиента
для подключения к L2 серверу.
"""

import asyncio
import logging

# Настройка логирования для отладки
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
)

from l2py import L2Client


async def main():
    """Главная функция примера."""
    client = L2Client()

    try:
        # Выполняем вход в игру
        session = await client.enter(
            username="qwerty",
            password="qwerty",
            host="192.168.0.33",
            port=2106,
            server_id=1,
            char_slot=0,
        )

        # Выводим информацию о персонаже
        char = session.character
        print("=" * 50)
        print(f"Вошёл в игру!")
        print(f"  Имя: {char.name}")
        print(f"  Уровень: {char.level}")
        print(f"  Раса: {char.race}")
        print(f"  Класс: {char.class_id}")
        print(f"  Координаты: ({char.x}, {char.y}, {char.z})")
        print("=" * 50)

        # Соединение остаётся активным
        # В реальном приложении здесь бы запускался игровой цикл
        print("\nНажмите Ctrl+C для выхода...")
        while True:
            await asyncio.sleep(1)

    except KeyboardInterrupt:
        print("\nОтключение...")
    except Exception as e:
        print(f"Ошибка: {e}")
        raise


if __name__ == "__main__":
    asyncio.run(main())
