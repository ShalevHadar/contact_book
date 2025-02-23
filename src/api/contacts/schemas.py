from pydantic import BaseModel

class ContactBase(BaseModel):
    first_name: str
    last_name: str
    phone_number: str
    address: str

class ContactUpdate(BaseModel):
    first_name: str | None = None
    last_name: str | None = None
    phone_number: str | None = None
    address: str | None = None

class Contact(ContactBase):
    id: int

    class Config:
        from_attributes = True
