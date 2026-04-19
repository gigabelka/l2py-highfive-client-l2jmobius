"""HTTP/WebSocket сервер на базе FastAPI + uvicorn.

`ApiServer` оборачивает `uvicorn.Server` и рассчитан на запуск в одном
event-loop с `GameSession.run_keepalive()`. Обязательно используется
`install_signal_handlers=False`, иначе uvicorn перехватит Ctrl+C и `main()`
не получит `KeyboardInterrupt`.
"""

from __future__ import annotations

import logging

import uvicorn
from fastapi import FastAPI, Response

from l2py.api import ws as ws_module
from l2py.api.routes import router as http_router
from l2py.api.state import ApiState
from l2py.api.ws import router as ws_router

logger = logging.getLogger(__name__)


def create_app(state: ApiState) -> FastAPI:
    """Собирает FastAPI-приложение и привязывает к нему shared state."""
    app = FastAPI(
        title="l2py external API",
        version="0.1.0",
        description=(
            "HTTP API для управления l2py-клиентом и WebSocket-стрим входящих "
            "игровых пакетов. Swagger: /docs, WebSocket: /ws/packets."
        ),
    )
    app.state.api_state = state
    app.include_router(http_router)
    app.include_router(ws_router)
    ws_module.register_subscribers(state)

    @app.get("/.well-known/appspecific/com.chrome.devtools.json", include_in_schema=False)
    async def _chrome_devtools_probe() -> Response:
        return Response(status_code=204)

    return app


class ApiServer:
    """Программная обёртка над uvicorn.Server."""

    __slots__ = ("_state", "_host", "_port", "_server")

    def __init__(self, state: ApiState, host: str = "127.0.0.1", port: int = 8000) -> None:
        self._state = state
        self._host = host
        self._port = port
        app = create_app(state)
        config = uvicorn.Config(
            app,
            host=host,
            port=port,
            log_level="info",
            lifespan="on",
        )
        self._server = uvicorn.Server(config)
        # Uvicorn would otherwise swallow Ctrl+C before main() sees it.
        self._server.install_signal_handlers = lambda: None  # type: ignore[method-assign]

    @property
    def url(self) -> str:
        return f"http://{self._host}:{self._port}"

    async def serve(self) -> None:
        logger.info("Starting API server on %s", self.url)
        await self._server.serve()

    async def shutdown(self) -> None:
        logger.info("Shutting down API server")
        self._server.should_exit = True


__all__ = ["ApiServer", "create_app"]
