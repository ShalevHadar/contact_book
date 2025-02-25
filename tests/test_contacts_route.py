import pytest
import pytest_mock
import pytest_asyncio
from unittest.mock import AsyncMock
from httpx import AsyncClient
from httpx import ASGITransport
from src.contacts.routes import contact_router
from src.contacts.schemas import ContactCreateModel, ContactUpdateModel
from fastapi import FastAPI

# Common test data
CONTACT_DATA = {
    "id": 1,
    "first_name": "John",
    "last_name": "Doe",
    "phone_number": "1234567890",
    "address": "123 Street",
}


# Define a manual mock class for ContactService
class MockContactService:
    async def get_contacts_paginated(self, page: int):
        if not isinstance(page, int) or page < 1:
            return None  # Simulating invalid page number error
        if not isinstance(page, int) or page < 1:
            raise ValueError("Invalid page number")
        return [CONTACT_DATA]

    async def get_contact(self, contact_id: int):
        if contact_id != 1:
            return None  # Simulating a 404 response for non-existent contact
        if contact_id != 1:
            return None  # Simulating a non-existent contact
        return CONTACT_DATA

    async def create_contact(self, contact_data: ContactCreateModel):
        return CONTACT_DATA

    async def update_contact(self, contact_id: int, update_data: ContactUpdateModel):
        return CONTACT_DATA

    async def delete_contact(self, contact_id: int):
        if contact_id != 1:
            return None  # Simulating a failed deletion, FastAPI should return 404
        if contact_id != 1:
            raise ValueError("Contact not found")  # Simulating a failed deletion
        return None  # FastAPI expects a 204 response with no content


@pytest.fixture
def app():
    app = FastAPI()
    app.include_router(contact_router, prefix="/contacts")
    return app


@pytest_asyncio.fixture
async def client(app):
    async with AsyncClient(base_url="http://test", transport=ASGITransport(app)) as ac:
        yield ac


@pytest.fixture
def mock_service(mocker: pytest_mock.MockFixture):
    mock_service = MockContactService()

    # Patch each async method explicitly
    mocker.patch.object(
        mock_service, "get_contacts_paginated", AsyncMock(return_value=[CONTACT_DATA])
    )
    mocker.patch.object(
        mock_service, "get_contact", AsyncMock(return_value=CONTACT_DATA)
    )
    mocker.patch.object(
        mock_service, "create_contact", AsyncMock(return_value=CONTACT_DATA)
    )
    mocker.patch.object(
        mock_service, "update_contact", AsyncMock(return_value=CONTACT_DATA)
    )
    mocker.patch.object(mock_service, "delete_contact", AsyncMock(return_value=None))

    # Patch the actual service import
    mocker.patch("src.contacts.routes.contact_service", mock_service)

    return mock_service


@pytest.mark.asyncio(scope="function")
async def test_get_page_contacts(client, mock_service):
    response = await client.get("/contacts/?page=1")
    assert response.status_code == 200
    assert response.json() == [CONTACT_DATA]


@pytest.mark.asyncio(scope="function")
async def test_get_page_contacts_invalid_page(client, mock_service):
    response = await client.get("/contacts/?page=abc")
    assert response.status_code == 422


@pytest.mark.asyncio(scope="function")
async def test_get_page_contacts_invalid_page_string(client, mock_service):
    response = await client.get("/contacts/?page=abc")
    assert (
        response.status_code == 422
    )  # FastAPI should return 422 for invalid query parameters


@pytest.mark.asyncio(scope="function")
async def test_get_contact(client, mock_service):
    response = await client.get("/contacts/1")
    assert response.status_code == 200
    assert response.json() == CONTACT_DATA


@pytest.mark.asyncio(scope="function")
async def test_get_invalid_contact(client, mock_service):
    response = await client.get("/contacts/abc")
    assert response.status_code == 405


@pytest.mark.asyncio(scope="function")
async def test_get_invalid_contact_string(client, mock_service):
    response = await client.get("/contacts/abc")
    assert response.status_code == 405


@pytest.mark.asyncio(scope="function")
async def test_create_contact_invalid(client, mock_service):
    response = await client.post("/contacts/", json={})
    assert response.status_code == 422  # Missing required fields


@pytest.mark.asyncio(scope="function")
async def test_create_contact(client, mock_service):
    response = await client.post("/contacts/", json=CONTACT_DATA)
    assert response.status_code == 201
    assert response.json() == CONTACT_DATA


@pytest.mark.asyncio(scope="function")
async def test_update_contact_invalid(client, mock_service):
    response = await client.put("/contacts/1", json={})
    assert response.status_code == 422  # Missing required fields


@pytest.mark.asyncio(scope="function")
async def test_update_contact(client, mock_service):
    response = await client.put("/contacts/1", json=CONTACT_DATA)
    assert response.status_code == 200
    assert response.json() == CONTACT_DATA


@pytest.mark.asyncio(scope="function")
async def test_delete_contact_invalid(client, mock_service):
    response = await client.delete("/contacts/abc")
    assert response.status_code == 422


@pytest.mark.asyncio(scope="function")
async def test_delete_contact(client, mock_service):
    response = await client.delete("/contacts/1")
    assert response.status_code == 204
