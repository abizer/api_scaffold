import pytest_asyncio
from httpx import ASGITransport, AsyncClient

from app.main import app

@pytest_asyncio.fixture(scope="session")
async def async_client():
    transport = ASGITransport(app=app)
    async with AsyncClient(transport=transport, base_url="http://") as client:
        yield client
