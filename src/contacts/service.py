from sqlalchemy.exc import IntegrityError

from sqlmodel import desc, select
from sqlmodel.ext.asyncio.session import AsyncSession

from src.db.models import Contact

from .schemas import ContactCreateModel, ContactUpdateModel
from ..errors import ContactNotFound, ContactAlreadyExists, InvalidPageNumber


# Create Service
class ContactService:

    # Create contact
    async def create_contact(
            self, contact_data: ContactCreateModel, session: AsyncSession
    ):
        contact_data_dict = contact_data.model_dump()
        new_contact = Contact(**contact_data_dict)

        session.add(new_contact)

        try:
            await session.commit()
            return new_contact
        except IntegrityError as e:
            await session.rollback()  # Rollback transaction to prevent issues
            if "unique constraint" in str(e.orig).lower():
                raise ContactAlreadyExists()

    # Get contact
    async def get_contact(self, contact_id: int, session: AsyncSession):
        statement = select(Contact).where(Contact.id == contact_id)

        result = await session.exec(statement)
        contact = result.first()

        if contact:
            return contact
        else:
            raise ContactNotFound()

    # Pagination
    async def get_contacts_paginated(self, page: int, session: AsyncSession):
        if page < 1:
            raise InvalidPageNumber()

        page_size = 10
        offset = (page - 1) * page_size  # Calculate offset

        statement = select(Contact).offset(offset).limit(page_size)
        result = await session.execute(statement)
        contacts = result.scalars().all()

        return contacts

    # Delete contact
    async def delete_contact(self, contact_id: int, session: AsyncSession):
        contact_to_delete = await self.get_contact(contact_id=contact_id, session=session)

        if contact_to_delete is not None:
            await session.delete(contact_to_delete)

            await session.commit()

            return contact_to_delete

        else:
            return None

    async def update_book(
        self, book_uid: str, update_data: ContactUpdateModel, session: AsyncSession
    ):
        book_to_update = await self.get_contact(book_uid, session)

        if book_to_update is not None:
            update_data_dict = update_data.model_dump()

            for k, v in update_data_dict.items():
                setattr(book_to_update, k, v)

            await session.commit()

            return book_to_update
        else:
            return None

