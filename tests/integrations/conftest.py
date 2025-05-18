from typing import AsyncIterator

import pytest
from fastapi import FastAPI
from httpx import AsyncClient, ASGITransport

from app.main import init_app


@pytest.fixture(scope="function")
async def app() -> AsyncIterator[FastAPI]:
    app = init_app()
    yield app

@pytest.fixture(scope="function")
async def client(app: FastAPI) -> AsyncIterator[AsyncClient]:
    t = ASGITransport(app)
    async with AsyncClient(transport=t, base_url="http://test") as ac:
        yield ac

