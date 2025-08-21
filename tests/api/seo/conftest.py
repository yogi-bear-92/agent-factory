"""Test fixtures for SEO API tests."""

from __future__ import annotations

import pytest
import pytest_asyncio
from fastapi import FastAPI
from httpx import ASGITransport, AsyncClient

from src.api.seo.routes import router


@pytest.fixture
def app() -> FastAPI:
    """Create FastAPI test application."""
    app = FastAPI()
    app.include_router(router)
    return app


@pytest.fixture
async def client(app: FastAPI) -> AsyncClient:
    """Create test client."""
    client = AsyncClient(base_url="http://testserver", transport=ASGITransport(app=app))
    try:
        yield client
    finally:
        await client.aclose()
        yield client