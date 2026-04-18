
"""Типизированная система событий.

Позволяет подписываться на события с type-safe callbacks.
Поддерживает как синхронные, так и асинхронные обработчики.
"""

from __future__ import annotations

import inspect
from dataclasses import dataclass
from typing import Awaitable, Callable, Generic, TypeVar

from l2py.models.character import CharacterInfo
from l2py.models.server import GameServer
from l2py.network.game_flow import GameSession

T = TypeVar("T")
EventCallback = Callable[[T], Awaitable[None] | None]


@dataclass(frozen=True)
class LoggedInEvent:
    """Событие успешного входа в игру."""

    character: CharacterInfo
    session: GameSession


@dataclass(frozen=True)
class PacketReceivedEvent:
    """Событие получения пакета."""

    opcode: int
    data: bytes
    source: str


@dataclass(frozen=True)
class LoginFailedEvent:
    """Событие неудачной авторизации."""

    reason: str
    code: int


@dataclass(frozen=True)
class ServerListEvent:
    """Событие получения списка серверов."""

    servers: list[GameServer]


class EventEmitter:
    """Типизированный эмиттер событий.

    Позволяет регистрировать обработчики для различных типов событий.
    Поддерживает как sync, так и async обработчики.

    Example:
        emitter = EventEmitter()
        emitter.on(LoggedInEvent, lambda e: print(f"Logged in as {e.character.name}"))
        await emitter.emit(LoggedInEvent(character=..., session=...))
    """

    __slots__ = ("_listeners",)

    def __init__(self) -> None:
        """Инициализация эмиттера."""
        self._listeners: dict[type, list[EventCallback]] = {}

    def on(self, event_type: type[T], callback: EventCallback[T]) -> EventEmitter:
        """Регистрирует обработчик события.

        Args:
            event_type: Тип события (класс dataclass).
            callback: Функция-обработчик.

        Returns:
            self для chaining.
        """
        if event_type not in self._listeners:
            self._listeners[event_type] = []
        self._listeners[event_type].append(callback)
        return self

    def once(self, event_type: type[T], callback: EventCallback[T]) -> EventEmitter:
        """Регистрирует одноразовый обработчик события.

        Обработчик будет автоматически удалён после первого вызова.

        Args:
            event_type: Тип события.
            callback: Функция-обработчик.

        Returns:
            self для chaining.
        """
        async def wrapper(event: T) -> None:
            self.off(event_type, wrapper)
            await self._invoke_callback(callback, event)


        wrapper._original = callback
        return self.on(event_type, wrapper)

    def off(self, event_type: type[T], callback: EventCallback[T]) -> EventEmitter:
        """Удаляет обработчик события.

        Args:
            event_type: Тип события.
            callback: Функция-обработчик (или wrapper от once).

        Returns:
            self для chaining.
        """
        if event_type not in self._listeners:
            return self

        listeners = self._listeners[event_type]

        to_remove = callback
        for listener in listeners:
            if listener is callback:
                to_remove = callback
                break

            if hasattr(listener, "_original") and listener._original is callback:
                to_remove = listener
                break

        if to_remove in listeners:
            listeners.remove(to_remove)

        return self

    async def emit(self, event: T) -> None:
        """Эмиттирует событие.

        Вызывает все зарегистрированные обработчики для типа события.

        Args:
            event: Объект события.
        """
        event_type = type(event)
        if event_type not in self._listeners:
            return

        for callback in self._listeners[event_type][:]:
            await self._invoke_callback(callback, event)

    async def _invoke_callback(self, callback: EventCallback[T], event: T) -> None:
        """Вызывает callback (sync или async).

        Args:
            callback: Функция для вызова.
            event: Объект события.
        """
        result = callback(event)
        if inspect.isawaitable(result):
            await result

    def remove_all(self, event_type: type[T] | None = None) -> None:
        """Удаляет все обработчики.

        Args:
            event_type: Если указан — удаляет только для этого типа,
                       иначе удаляет все.
        """
        if event_type is None:
            self._listeners.clear()
        elif event_type in self._listeners:
            del self._listeners[event_type]


class EventMixin:
    """Mixin для добавления EventEmitter к классу.

    Example:
        class MyClass(EventMixin):
            def __init__(self):
                super().__init__()
                self.on(LoggedInEvent, self._on_login)

            def _on_login(self, event):
                print(f"Logged in: {event.character.name}")
    """

    __slots__ = ("_emitter",)

    def __init__(self) -> None:
        """Инициализация mixin."""
        self._emitter = EventEmitter()

    def on(self, event_type: type[T], callback: EventCallback[T]) -> EventMixin:
        """Регистрирует обработчик события."""
        self._emitter.on(event_type, callback)
        return self

    def once(self, event_type: type[T], callback: EventCallback[T]) -> EventMixin:
        """Регистрирует одноразовый обработчик."""
        self._emitter.once(event_type, callback)
        return self

    def off(self, event_type: type[T], callback: EventCallback[T]) -> EventMixin:
        """Удаляет обработчик события."""
        self._emitter.off(event_type, callback)
        return self

    async def emit(self, event: T) -> None:
        """Эмиттирует событие."""
        await self._emitter.emit(event)


__all__ = [

    "LoggedInEvent",
    "PacketReceivedEvent",
    "LoginFailedEvent",
    "ServerListEvent",

    "EventEmitter",
    "EventMixin",
]
