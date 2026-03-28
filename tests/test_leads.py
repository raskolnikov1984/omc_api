import pytest
from httpx import AsyncClient


@pytest.mark.anyio
async def test_create_lead_with_successfulyy(async_client: AsyncClient, lead: dict):
    response = await async_client.post("/leads", json=lead)

    assert response.status_code == 201