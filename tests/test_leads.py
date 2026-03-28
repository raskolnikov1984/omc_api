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
    for i in range(15):
        lead_with_unique_email = {**lead, "email": f"test{i}@example.com"}
        await async_client.post("/leads", json=lead_with_unique_email)

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


@pytest.mark.anyio
async def test_update_lead(async_client: AsyncClient, lead: dict):
    create_response = await async_client.post("/leads", json=lead)
    lead_id = create_response.json()["id"]

    update_data = {"name": "Updated Name", "budget": 5000}
    response = await async_client.patch(f"/leads/{lead_id}", json=update_data)

    assert response.status_code == 200
    data = response.json()
    assert data["name"] == "Updated Name"
    assert data["budget"] == 5000
    assert data["email"] == lead["email"]


@pytest.mark.anyio
async def test_update_lead_partial(async_client: AsyncClient, lead: dict):
    create_response = await async_client.post("/leads", json=lead)
    lead_id = create_response.json()["id"]

    update_data = {"phone": "+123456789"}
    response = await async_client.patch(f"/leads/{lead_id}", json=update_data)

    assert response.status_code == 200
    data = response.json()
    assert data["phone"] == "+123456789"
    assert data["name"] == lead["name"]


@pytest.mark.anyio
async def test_update_lead_not_found(async_client: AsyncClient):
    update_data = {"name": "Test"}
    response = await async_client.patch("/leads/999", json=update_data)

    assert response.status_code == 404


@pytest.mark.anyio
async def test_update_lead_updates_timestamp(async_client: AsyncClient, lead: dict):
    import time

    create_response = await async_client.post("/leads", json=lead)
    lead_id = create_response.json()["id"]

    time.sleep(0.1)

    update_data = {"name": "Updated Name"}
    response = await async_client.patch(f"/leads/{lead_id}", json=update_data)

    assert response.status_code == 200
    data = response.json()
    assert data["updated_at"] is not None


@pytest.mark.anyio
async def test_delete_lead_success(async_client: AsyncClient, lead: dict):
    create_response = await async_client.post("/leads", json=lead)
    lead_id = create_response.json()["id"]

    response = await async_client.delete(f"/leads/{lead_id}")

    assert response.status_code == 204

    get_response = await async_client.get(f"/leads/{lead_id}")
    assert get_response.status_code == 404


@pytest.mark.anyio
async def test_delete_lead_not_found(async_client: AsyncClient):
    response = await async_client.delete("/leads/999")

    assert response.status_code == 404


@pytest.mark.anyio
async def test_get_leads_stats(async_client: AsyncClient, lead: dict):
    lead_facebook = {**lead, "source": "facebook", "budget": 1000}
    lead_instagram = {
        **lead,
        "source": "instagram",
        "email": "test2@example.com",
        "budget": 2000,
    }
    lead_landing = {
        **lead,
        "source": "landing_page",
        "email": "test3@example.com",
        "budget": 1500,
    }

    await async_client.post("/leads", json=lead_facebook)
    await async_client.post("/leads", json=lead_instagram)
    await async_client.post("/leads", json=lead_landing)

    response = await async_client.get("/leads/stats")

    assert response.status_code == 200
    data = response.json()
    assert data["total_leads"] == 3
    assert data["leads_by_source"]["facebook"] == 1
    assert data["leads_by_source"]["instagram"] == 1
    assert data["leads_by_source"]["landing_page"] == 1
    assert data["average_budget"] == 1500.0
    assert data["leads_last_7_days"] == 3


@pytest.mark.anyio
async def test_create_lead_duplicate_email(async_client: AsyncClient, lead: dict):
    await async_client.post("/leads", json=lead)

    response = await async_client.post("/leads", json=lead)

    assert response.status_code == 400
    assert "Email already exists" in response.json()["detail"]


@pytest.mark.anyio
async def test_create_lead_short_name(async_client: AsyncClient, lead: dict):
    lead_short_name = {**lead, "name": "A"}

    response = await async_client.post("/leads", json=lead_short_name)

    assert response.status_code == 422


@pytest.mark.anyio
async def test_create_lead_invalid_source(async_client: AsyncClient, lead: dict):
    lead_invalid_source = {**lead, "source": "invalid_source"}

    response = await async_client.post("/leads", json=lead_invalid_source)

    assert response.status_code == 422
