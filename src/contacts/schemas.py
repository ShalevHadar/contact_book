from pydantic import BaseModel


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
