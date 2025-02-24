from typing import List

from fastapi import APIRouter, Depends, status
from sqlmodel.ext.asyncio.session import AsyncSession
from starlette.status import HTTP_200_OK

from src.contacts.service import ContactService
from src.db.main import get_session

from .schemas import Contact, ContactCreateModel, ContactUpdateModel

contact_router = APIRouter()
contact_service = ContactService()


# Create Route
@contact_router.post("/", status_code=status.HTTP_201_CREATED, response_model=Contact)
async def create_a_contact(
    contact_data: ContactCreateModel,
    session: AsyncSession = Depends(get_session),
) -> dict:
    new_contact = await contact_service.create_contact(
        contact_data=contact_data, session=session
    )
    return new_contact


# Get Route
@contact_router.get(
    "/{contact_id}", status_code=status.HTTP_200_OK, response_model=Contact
)
async def get_contact(
    contact_id: int,
    session: AsyncSession = Depends(get_session),
) -> dict:
    contact = await contact_service.get_contact(contact_id=contact_id, session=session)

    return contact

# Delete Route
@contact_router.delete(
    "/{contact_id}", status_code=status.HTTP_204_NO_CONTENT, dependencies=[]
)
async def delete_contact(
    contact_id: int,
    session: AsyncSession = Depends(get_session),
):
    contact_to_delete = await contact_service.delete_contact(contact_id=contact_id, session=session)

    return {"contact_to_delete": contact_id}

# Pagination Route
@contact_router.get("/pagination/{page}", status_code=HTTP_200_OK, response_model=list[Contact])
async def get_contacts_paginated(
    page: int,
    session: AsyncSession = Depends(get_session),
):
    contacts = await contact_service.get_contacts_paginated(page, session)
    return contacts

#
# @contact_router.patch("/{book_uid}", response_model=Contact, dependencies=[])
# async def update_book(
#     book_uid: str,
#     book_update_data: ContactUpdateModel,
#     session: AsyncSession = Depends(get_session),
# ) -> dict:
#     updated_book = await contact_service.update_book(
#         book_uid, book_update_data, session
#     )
#
#     if updated_book is None:
#         raise BookNotFound()
#     else:
#         return updated_book
#
#
