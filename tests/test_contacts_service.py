import pytest
import pytest_mock
from unittest.mock import AsyncMock
from src.contacts.service import ContactService
from src.contacts.schemas import ContactCreateModel, ContactUpdateModel
from src.errors import ContactNotFound, ContactAlreadyExists, InvalidPageNumber

# Common test data
CONTACT_DATA = {
    "id": 1,
    "first_name": "John",
    "last_name": "Doe",
    "phone_number": "1234567890",
    "address": "123 Street",
}


@pytest.fixture
def contact_service():
    return ContactService()


@pytest.fixture
def mock_contact_db_layer(mocker: pytest_mock.MockFixture):
    mocker.patch("src.contacts.service.is_valid_israeli_phone", return_value=True)
    mock_layer = mocker.patch("src.contacts.service.contact_db_layer")

    mock_layer.get_contact = AsyncMock(return_value=CONTACT_DATA)
    mock_layer.create_contact = AsyncMock(return_value=CONTACT_DATA)
    mock_layer.update_contact = AsyncMock(return_value=CONTACT_DATA)
    mock_layer.delete_contact = AsyncMock(return_value=True)
    mock_layer.get_contacts_paginated = AsyncMock(return_value=[CONTACT_DATA])

    return mock_layer


@pytest.mark.asyncio
async def test_create_contact(contact_service, mock_contact_db_layer):
    contact = ContactCreateModel(**CONTACT_DATA)
    result = await contact_service.create_contact(contact)
    assert result == CONTACT_DATA


@pytest.mark.asyncio
async def test_create_contact_already_exists(contact_service, mock_contact_db_layer):
    mock_contact_db_layer.create_contact = AsyncMock(return_value=None)
    contact = ContactCreateModel(**CONTACT_DATA)
    with pytest.raises(ContactAlreadyExists):
        await contact_service.create_contact(contact)


@pytest.mark.asyncio
async def test_get_contact(contact_service, mock_contact_db_layer):
    result = await contact_service.get_contact(1)
    assert result == CONTACT_DATA


@pytest.mark.asyncio
async def test_get_contact_not_found(contact_service, mock_contact_db_layer):
    mock_contact_db_layer.get_contact = AsyncMock(return_value=None)
    with pytest.raises(ContactNotFound):
        await contact_service.get_contact(9999)


@pytest.mark.asyncio
async def test_get_contacts_paginated(contact_service, mock_contact_db_layer):
    result = await contact_service.get_contacts_paginated(1)
    assert result == [CONTACT_DATA]


@pytest.mark.asyncio
async def test_get_contacts_paginated_invalid_page(contact_service):
    with pytest.raises(InvalidPageNumber):
        await contact_service.get_contacts_paginated(-1)


@pytest.mark.asyncio
async def test_update_contact(contact_service, mock_contact_db_layer):
    update_data = ContactUpdateModel(**CONTACT_DATA)
    result = await contact_service.update_contact(1, update_data)
    assert result == CONTACT_DATA


@pytest.mark.asyncio
async def test_update_contact_not_found(contact_service, mock_contact_db_layer):
    mock_contact_db_layer.get_contact = AsyncMock(return_value=None)
    update_data = ContactUpdateModel(**CONTACT_DATA)
    with pytest.raises(ContactNotFound):
        await contact_service.update_contact(9999, update_data)


@pytest.mark.asyncio
async def test_delete_contact(contact_service, mock_contact_db_layer):
    result = await contact_service.delete_contact(1)
    assert result == {"message": "Contact deleted successfully"}


@pytest.mark.asyncio
async def test_delete_contact_not_found(contact_service, mock_contact_db_layer):
    mock_contact_db_layer.delete_contact = AsyncMock(return_value=False)
    with pytest.raises(ContactNotFound) as exc_info:
        await contact_service.delete_contact(9999)
    assert str(exc_info.value) == ""
