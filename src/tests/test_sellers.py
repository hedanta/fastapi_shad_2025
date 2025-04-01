import pytest
from fastapi import status
from icecream import ic

from src.models.sellers import Seller


@pytest.mark.asyncio
async def test_create_seller(async_client, db_session):
    seller_data = {
        "first_name": "John",
        "last_name": "Doe",
        "e_mail": "john.doe@example.com",
        "password": "Password123",
    }
    response = await async_client.post("/api/v1/sellers/", json=seller_data)
    assert response.status_code == status.HTTP_201_CREATED

    seller = response.json()

    assert seller["first_name"] == "John"
    assert seller["last_name"] == "Doe"
    assert seller["e_mail"] == "john.doe@example.com"


@pytest.mark.asyncio
async def test_get_sellers(db_session, async_client):
    seller_1 = Seller(
        first_name="John",
        last_name="Doe",
        e_mail="john.doe@example.com",
        password="Password123",
    )
    seller_2 = Seller(
        first_name="Jane",
        last_name="Doe",
        e_mail="jane.doe@example.com",
        password="Password456",
    )

    db_session.add_all([seller_1, seller_2])
    await db_session.flush()

    response = await async_client.get("/api/v1/sellers/")
    assert response.status_code == status.HTTP_200_OK

    sellers = response.json()

    assert sellers[0]["first_name"] == "John"
    assert sellers[1]["first_name"] == "Jane"
    assert "books" in sellers[0]
    assert sellers[0]["books"] == []


@pytest.mark.asyncio
async def test_get_single_seller(db_session, async_client):
    seller = Seller(
        first_name="John",
        last_name="Doe",
        e_mail="john.doe@example.com",
        password="Password123",
    )
    db_session.add(seller)
    await db_session.flush()

    response = await async_client.get(f"/api/v1/sellers/{seller.id}")
    assert response.status_code == status.HTTP_200_OK
    seller_data = response.json()

    assert seller_data["first_name"] == "John"
    assert seller_data["last_name"] == "Doe"
    assert seller_data["e_mail"] == "john.doe@example.com"
    assert "books" in seller_data
    assert seller_data["books"] == []


@pytest.mark.asyncio
async def test_update_seller(db_session, async_client):
    seller = Seller(
        first_name="John",
        last_name="Doe",
        e_mail="john.doe@example.com",
        password="Password123",
    )
    db_session.add(seller)
    await db_session.flush()

    response = await async_client.put(
        f"/api/v1/sellers/{seller.id}",
        json={
            "first_name": "Jane",
            "last_name": "Doe",
            "e_mail": "jane.doe@example.com",
            "id": seller.id,
        },
    )
    assert response.status_code == status.HTTP_200_OK

    updated_seller = await db_session.get(Seller, seller.id)

    assert updated_seller.first_name == "Jane"
    assert updated_seller.last_name == "Doe"
    assert updated_seller.e_mail == "jane.doe@example.com"
    assert updated_seller.id == seller.id
    assert updated_seller.books == []


@pytest.mark.asyncio
async def test_delete_seller(db_session, async_client):
    seller = Seller(
        first_name="John",
        last_name="Doe",
        e_mail="john.doe@example.com",
        password="Password123",
    )
    db_session.add(seller)
    await db_session.flush()
    ic(seller.id)

    response = await async_client.delete(f"/api/v1/sellers/{seller.id}")
    assert response.status_code == status.HTTP_204_NO_CONTENT
