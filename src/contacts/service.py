from .database import ContactDBLayer

from .schemas import ContactCreateModel, ContactUpdateModel
from .utils import is_valid_israeli_phone
from ..database.main import get_session
from ..errors import (
    ContactNotFound,
    InvalidPageNumber,
    ContactAlreadyExists,
    InvalidPhoneNumber,
    InvalidSearch,
)
from src.logger import app_log

contact_db_layer = ContactDBLayer()


# Create Service
class ContactService:
    # Create contact
    async def create_contact(self, contact_data: ContactCreateModel):
        app_log.info("Creating a new contact")
        async with get_session() as session:
            if is_valid_israeli_phone(contact_data.phone_number) is False:
                app_log.warning("Invalid phone number provided")
                raise InvalidPhoneNumber
            contact = await contact_db_layer.create_contact(
                contact_data=contact_data, session=session
            )
            if contact is None:
                app_log.warning("Attempt to create a contact that already exists")
                raise ContactAlreadyExists()
            app_log.info(f"Contact created: {contact}")
            return contact

    # Get contact
    async def get_contact(self, contact_id: int):
        app_log.info(f"Fetching contact with ID: {contact_id}")
        async with get_session() as session:
            contact = await contact_db_layer.get_contact(
                contact_id=contact_id, session=session
            )
            if contact is None:
                app_log.warning(f"Contact with ID {contact_id} not found")
                raise ContactNotFound()
            return contact

    # Pagination
    async def get_contacts_paginated(self, page: int):
        if page < 1:
            app_log.warning("Invalid page number requested")
            raise InvalidPageNumber()

        page_size = 10
        offset = (page - 1) * page_size
        async with get_session() as session:
            app_log.info(f"Fetching contacts for page {page}")
            return await contact_db_layer.get_contacts_paginated(
                offset=offset, page_size=page_size, session=session
            )

    # Delete contact
    async def delete_contact(self, contact_id: int):
        app_log.info(f"Deleting contact with ID: {contact_id}")
        async with get_session() as session:
            deleted = await contact_db_layer.delete_contact(
                contact_id=contact_id, session=session
            )
            if not deleted:
                app_log.warning(
                    f"Attempted to delete non-existent contact ID: {contact_id}"
                )
                raise ContactNotFound()
            app_log.info(f"Contact ID {contact_id} deleted successfully")
            return {"message": "Contact deleted successfully"}

    async def update_contact(self, contact_id: int, update_data: ContactUpdateModel):
        app_log.info(f"Updating contact ID: {contact_id}")
        async with get_session() as session:
            contact_to_update = await contact_db_layer.get_contact(contact_id, session)

            if contact_to_update is None:
                app_log.warning(f"Contact ID {contact_id} not found for update")
                raise ContactNotFound()

            updated_contact = await contact_db_layer.update_contact(
                contact_to_update, update_data, session
            )
            app_log.info(f"Contact ID {contact_id} updated successfully")
            return updated_contact

    async def search_contact(
        self, phone_number: str = None, first_name: str = None, last_name: str = None
    ):
        app_log.info("Searching for contacts")
        async with get_session() as session:
            if not phone_number and not (first_name and last_name):
                raise InvalidSearch()
            contacts = await contact_db_layer.search_contact(
                phone_number=phone_number,
                first_name=first_name,
                last_name=last_name,
                session=session,
            )
            app_log.info(f"Found {len(contacts)} contacts matching criteria")
            return contacts if contacts else []
