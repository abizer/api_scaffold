#!/usr/bin/env python3
import pytest
from httpx import AsyncClient


@pytest.mark.asyncio
async def test_status(async_client: AsyncClient):
    response = await async_client.get("/status")
    assert response is not None
    assert response.status_code == 200
    data = response.json()
    assert "status" in data
    assert data["status"] == "ok"
