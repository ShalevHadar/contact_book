from contextlib import asynccontextmanager
import pytest
from fastapi import FastAPI
from httpx import AsyncClient
from unittest.mock import AsyncMock
from src.contacts.routes import contact_router
from src.contacts.service import ContactService
from src.contacts.schemas import Contact


@asynccontextmanager
async def lifespan(app: FastAPI):
    yield


@pytest.mark.asyncio
async def test_contact_routes():
    app = FastAPI(lifespan=lifespan)
    app.include_router(contact_router)

    mock_service = AsyncMock(spec=ContactService)
    app.dependency_overrides[ContactService] = lambda: mock_service

    async with AsyncClient(app=app, base_url="http://127.0.0.1:8000") as client:
        # Test create contact
        mock_service.create_contact.return_value = Contact(
            id=1,
            first_name="John",
            last_name="Doe",
            phone_number="0501234567",
            address="123 Street",
        )
        response = await client.post(
            "/",
            json={
                "first_name": "John",
                "last_name": "Doe",
                "phone_number": "0501234567",
                "address": "123 Street",
            },
        )
        assert response.status_code == 201
        assert response.json()["first_name"] == "John"

        # Test get contact
        mock_service.get_contact.return_value = Contact(
            id=1,
            first_name="John",
            last_name="Doe",
            phone_number="0501234567",
            address="123 Street",
        )
        response = await client.get("/1")
        assert response.status_code == 200
        assert response.json()["id"] == 1

        # Test delete contact
        mock_service.delete_contact.return_value = None
        response = await client.delete("/1")
        assert response.status_code == 204

        # Test pagination
        mock_service.get_contacts_paginated.return_value = []
        response = await client.get("/?page=1")
        assert response.status_code == 200
        assert isinstance(response.json(), list)

        # Test update contact
        mock_service.update_contact.return_value = Contact(
            id=1,
            first_name="Jane",
            last_name="Doe",
            phone_number="0501234567",
            address="456 Avenue",
        )
        response = await client.put(
            "/1",
            json={
                "first_name": "Jane",
                "last_name": "Doe",
                "phone_number": "0501234567",
                "address": "456 Avenue",
            },
        )
        assert response.status_code == 200
        assert response.json()["first_name"] == "Jane"

        # Test search contact
        mock_service.search_contact.return_value = [
            Contact(
                id=1,
                first_name="John",
                last_name="Doe",
                phone_number="0501234567",
                address="123 Street",
            )
        ]
        response = await client.get("/search?phone_number=0501234567")
        assert response.status_code == 200
        assert len(response.json()) > 0
