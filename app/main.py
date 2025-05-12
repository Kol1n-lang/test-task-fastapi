from fastapi import FastAPI
from app.api.v1.controllers import auth_router, bank_router
from dishka.integrations.fastapi import setup_dishka
from app.dependencies.container import container

from app.middleware import JWTAccessMiddleware


def init_routers(app: FastAPI, prefix: str) -> None:
    app.include_router(auth_router, prefix=prefix)
    app.include_router(bank_router, prefix=prefix)


def init_middlewares(app: FastAPI) -> None:
    app.add_middleware(JWTAccessMiddleware)


def init_app() -> FastAPI:
    app = FastAPI(
        title="Bank Imitation",
        description="Bank Imitation",
        version="1.0.0",
    )

    init_routers(app, prefix="/api/v1")
    init_middlewares(app)
    setup_dishka(app=app, container=container)

    return app
