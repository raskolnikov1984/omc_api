import pytest
from httpx import ASGITransport, AsyncClient
from sqlalchemy.ext.asyncio import (
    create_async_engine, async_sessionmaker, AsyncSession
)
from sqlalchemy.pool import StaticPool
from app.database.models import Base

from app.main import app
from app.api.v1.endpoints.leads.leads import leads

TEST_DATABASE_URL = "sqlite+aiosqlite:///:memory:"


@pytest.fixture(scope="function")
def engine():
    """
    Create the engine async for each test
    """

    return create_async_engine(
        TEST_DATABASE_URL,
        echo=True,
        poolclass=StaticPool
    )


@pytest.fixture(scope="function")
def async_session_maker(engine):
    """Factory de sesiones async"""
    return async_sessionmaker(
        bind=engine,
        class_=AsyncSession,
        expire_on_commit=False,
    )

@pytest.fixture(autouse=True, scope="function")
async def setup_database(engine):
    """Setup y teardown automatic for database in each test"""

    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)

    yield

    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.drop_all)


@pytest.fixture(scope="function")
async def async_client():
    leads.clear()
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
