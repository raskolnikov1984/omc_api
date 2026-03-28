import pytest
from httpx import AsyncClient


@pytest.mark.anyio
async def test_create_lead_with_successfuly(async_client: AsyncClient, lead: dict):
    response = await async_client.post("/leads", json=lead)

    assert response.status_code == 201
    data = response.json()
    
    assert "id" in data
    assert data["id"] == 1 
    assert "created_at" in data


@pytest.mark.anyio
async def test_get_leads_paginated(async_client: AsyncClient, lead: dict):
    for _ in range(15):
        await async_client.post("/leads", json=lead)

    response = await async_client.get("/leads?page=1&limit=10")

    assert response.status_code == 200
    data = response.json()
    assert len(data["items"]) == 10
    assert data["page"] == 1
    assert data["limit"] == 10
    assert data["total"] == 15
    assert data["total_pages"] == 2


@pytest.mark.anyio
async def test_get_leads_filter_by_source(async_client: AsyncClient, lead: dict):
    lead_facebook = {**lead, "source": "facebook"}
    lead_instagram = {**lead, "source": "instagram", "email": "test2@example.com"}

    await async_client.post("/leads", json=lead_facebook)
    await async_client.post("/leads", json=lead_instagram)

    response = await async_client.get("/leads?source=facebook")

    assert response.status_code == 200
    data = response.json()
    assert all(item["source"] == "facebook" for item in data["items"])


@pytest.mark.anyio
async def test_get_leads_filter_by_date_range(async_client: AsyncClient, lead: dict):
    await async_client.post("/leads", json=lead)

    from datetime import date, timedelta

    today = date.today()
    tomorrow = today + timedelta(days=1)

    response = await async_client.get(f"/leads?start_date={today}&end_date={tomorrow}")

    assert response.status_code == 200
    data = response.json()
    assert len(data["items"]) >= 1


@pytest.mark.anyio
async def test_get_leads_order_by_created_at_desc(
    async_client: AsyncClient, lead: dict
):
    lead_1 = {**lead, "email": "first@example.com"}
    lead_2 = {**lead, "email": "second@example.com"}

    await async_client.post("/leads", json=lead_1)
    await async_client.post("/leads", json=lead_2)

    response = await async_client.get("/leads?order_dir=desc")

    assert response.status_code == 200
    data = response.json()
    assert len(data["items"]) >= 2


@pytest.mark.anyio
async def test_get_lead_by_id(async_client: AsyncClient, lead: dict):
    create_response = await async_client.post("/leads", json=lead)
    lead_id = create_response.json()["id"]

    response = await async_client.get(f"/leads/{lead_id}")

    assert response.status_code == 200
    data = response.json()
    assert data["id"] == lead_id
    assert data["email"] == lead["email"]


@pytest.mark.anyio
async def test_get_lead_by_id_not_found(async_client: AsyncClient):
    response = await async_client.get("/leads/999")

    assert response.status_code == 404
