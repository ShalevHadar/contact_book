from sqlalchemy.exc import IntegrityError
from typing import Any
from sqlmodel import select

from sqlalchemy.ext.asyncio import AsyncSession

from src.database.models import Contact


class ContactDBLayer:
    async def create_contact(self, contact_data: Any, session: AsyncSession):
        contact_data_dict = contact_data.model_dump()
        new_contact = Contact(**contact_data_dict)
        session.add(new_contact)

        try:
            await session.commit()
            return new_contact
        except IntegrityError as e:
            await session.rollback()
            if "unique constraint" in str(e.orig).lower():
                return None
            raise e

    async def get_contact(self, contact_id: int, session: AsyncSession):
        statement = select(Contact).where(Contact.id == contact_id)
        result = await session.execute(statement)
        return result.scalars().first()  # ✅ Returns None if not found, no exception

    async def get_contacts_paginated(
        self, offset: int, page_size: int, session: AsyncSession
    ):
        statement = select(Contact).offset(offset).limit(page_size)
        result = await session.execute(statement)
        contacts = result.scalars().all()

        return contacts

    async def delete_contact(self, contact_id: int, session: AsyncSession):
        contact = await self.get_contact(contact_id=contact_id, session=session)

        if contact is None:
            return False

        await session.delete(contact)
        await session.commit()
        return True

    async def update_contact(
        self, contact_to_update, update_data: Any, session: AsyncSession
    ):
        update_data_dict = update_data.model_dump(exclude_unset=True)

        for key, value in update_data_dict.items():
            setattr(contact_to_update, key, value)

        await session.commit()
        return contact_to_update

    async def search_contact(
        self,
        phone_number: str = None,
        first_name: str = None,
        last_name: str = None,
        session: AsyncSession = None,
    ):
        if phone_number:
            statement = select(Contact).where(Contact.phone_number == phone_number)
        elif first_name and last_name:
            statement = select(Contact).where(
                Contact.first_name == first_name, Contact.last_name == last_name
            )

        result = await session.execute(statement)
        contacts = result.scalars().all()

        return contacts
