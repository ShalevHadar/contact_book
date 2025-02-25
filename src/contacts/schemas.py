from pydantic import BaseModel
from typing import Optional


class Contact(BaseModel):
    id: int
    first_name: str
    last_name: str
    phone_number: str
    address: str


class ContactCreateModel(BaseModel):
    first_name: str
    last_name: str
    phone_number: str
    address: str


class ContactUpdateModel(BaseModel):
    first_name: str
    last_name: str
    phone_number: str
    address: str


class ContactSearchModel(BaseModel):
    phone_number: Optional[str] = None
    first_name: Optional[str] = None
    last_name: Optional[str] = None
