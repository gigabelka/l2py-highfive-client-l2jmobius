# -*- coding: utf-8 -*-
"""Главный фасад для подключения к L2 серверу.

Предоставляет простой API для входа в игру.
"""

import logging

from l2py.config import ConnectionConfig, Credentials, LoginConfig
from l2py.network.game_flow import GameFlow, GameSession
from l2py.network.login_flow import LoginFlow

logger = logging.getLogger(__name__)


class L2Client:
    """Главный фасад для работы с L2 сервером.

    Пример использования:
        client = L2Client()
        session = await client.enter(
            username="qwerty",
            password="qwerty",
            host="192.168.0.33",
            server_id=2,
        )
    """

    __slots__ = ()

    def __init__(self) -> None:
        """Инициализация клиента."""
        pass

    async def enter(
        self,
        username: str,
        password: str,
        host: str = "192.168.0.33",
        port: int = 2106,
        server_id: int = 2,
        char_slot: int = 0,
    ) -> GameSession:
        """Выполняет полный login flow: авторизация → выбор сервера → вход в мир.

        Args:
            username: Логин аккаунта.
            password: Пароль аккаунта.
            host: Адрес Login Server (по умолчанию 192.168.0.33).
            port: Порт Login Server (по умолчанию 2106).
            server_id: ID игрового сервера (по умолчанию 1).
            char_slot: Индекс слота персонажа (по умолчанию 0).

        Returns:
            Игровая сессия с активным соединением.

        Raises:
            LoginError: Если авторизация не удалась.
            GameError: Если вход в мир не удался.
            ConnectionError: Если проблемы с соединением.
        """
        logger.info(
            f"Starting login: user={username}, host={host}:{port}, "
            f"server_id={server_id}, char_slot={char_slot}"
        )

        # Создаём конфигурации
        login_config = LoginConfig(host=host, port=port)
        credentials = Credentials(username=username, password=password)

        # Фаза 1: Авторизация на Login Server
        logger.debug("Phase 1: Login Server authentication")
        login_result = await LoginFlow(login_config, credentials, server_id).execute()

        # Фаза 2: Вход в игровой мир
        logger.debug("Phase 2: Game Server connection")
        session = await GameFlow(login_result, char_slot).execute()

        logger.info(f"Successfully logged in as {session.character.name}")
        return session


__all__ = ["L2Client"]
