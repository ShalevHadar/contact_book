from fastapi import APIRouter, Query, status
from starlette.status import HTTP_200_OK

from src.contacts.service import ContactService

from .schemas import Contact, ContactCreateModel, ContactUpdateModel

contact_router = APIRouter()
contact_service = ContactService()


# Create Route
@contact_router.post("/", status_code=status.HTTP_201_CREATED, response_model=Contact)
async def create_contact(contact_data: ContactCreateModel) -> Contact:
    return await contact_service.create_contact(contact_data=contact_data)


# Get Route
@contact_router.get(
    "/{contact_id:int}", status_code=status.HTTP_200_OK, response_model=Contact
)
async def get_contact(contact_id: int) -> Contact:
    return await contact_service.get_contact(contact_id=contact_id)


# Delete Route
@contact_router.delete("/{contact_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_contact(contact_id: int):
    return await contact_service.delete_contact(contact_id=contact_id)


# Pagination Route
@contact_router.get("/", status_code=HTTP_200_OK, response_model=list[Contact])
async def get_contacts_paginated(page: int = 1):
    return await contact_service.get_contacts_paginated(page=page)


# Update Route
@contact_router.put("/{contact_id}", response_model=Contact)
async def update_contact(contact_id: int, update_data: ContactUpdateModel):
    return await contact_service.update_contact(
        contact_id=contact_id, update_data=update_data
    )


@contact_router.get("/search", status_code=HTTP_200_OK, response_model=list[Contact])
async def search_contact(
    phone_number: str = Query(None),
    first_name: str = Query(None),
    last_name: str = Query(None),
):
    return await contact_service.search_contact(
        phone_number=phone_number, first_name=first_name, last_name=last_name
    )
