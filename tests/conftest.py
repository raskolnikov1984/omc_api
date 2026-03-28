import pytest
from httpx import ASGITransport, AsyncClient
from app.main import app


@pytest.fixture(scope="function")
async def async_client():
    async with AsyncClient(
        transport=ASGITransport(app=app), base_url="http://test/api/v1"
    ) as client:
        yield client


@pytest.fixture
def lead():
    return {
        "name": "Test Lead",
        "email": "test@example.com",
        "phone": "+1234567890",
        "source": "facebook",
        "target_product": "product_1",
        "budget": 1000,
    }
