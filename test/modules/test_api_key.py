import pytest
from httpx import AsyncClient


@pytest.mark.asyncio(scope="class")
class TestApiKey:
    intermediates = {}

    async def test_create(self, async_client: AsyncClient) -> None:
        response = await async_client.post("/v1/api-keys")
        assert response.status_code == 200
        self.intermediates["api_key"] = response.json()

    async def test_get(self, async_client: AsyncClient) -> None:
        response = await async_client.get("/v1/api-keys")
        assert response.status_code == 200
        assert len(response.json()) == 1
        assert response.json()[0]["id"] == self.intermediates["api_key"]["id"]

    async def test_delete(self, async_client: AsyncClient) -> None:
        response = await async_client.delete(
            f"/v1/api-keys/{self.intermediates['api_key']['id']}"
        )
        assert response.status_code == 200
        assert (
            response.json()["message"]
            == f"Api key {self.intermediates['api_key']['api_key']} deleted"
        )
