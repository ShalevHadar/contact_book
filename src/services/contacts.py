from sqlalchemy.orm import Session
from server.src import models, schemas

def get_contacts(db: Session, skip: int = 0, limit: int = 10):
    """
    Get a list of contacts
    :param db:
    :param skip:
    :param limit:
    :return:
    """
    return db.query(models.Contact).offset(skip).limit(limit).all()

def get_contact(db: Session, contact_id: int):
    """
    Get a contact by id
    :param db:
    :param contact_id:
    :return:
    """
    return db.query(models.Contact).filter(models.Contact.id == contact_id).first()

def create_contact(db: Session, contact: schemas.ContactBase):
    """
    Create a new contact
    :param db:
    :param contact:
    :return:
    """
    db_contact = models.Contact(**contact.dict())
    db.add(db_contact)
    db.commit()
    db.refresh(db_contact)
    return db_contact

def update_contact(db: Session, contact_id: int, contact: schemas.ContactUpdate):
    """
    Update a contact by id
    if contact not found, return None
    :param db:
    :param contact_id:
    :param contact:
    :return:
    """
    db_contact = get_contact(db, contact_id)
    if not db_contact:
        return None
    for field, value in contact.dict(exclude_unset=True).items():
        setattr(db_contact, field, value)
    db.commit()
    db.refresh(db_contact)
    return db_contact

def delete_contact(db: Session, contact_id: int):
    """
    delete a contact by id
    if contact not found, return None
    :param db:
    :param contact_id:
    :return:
    """
    db_contact = get_contact(db, contact_id)
    if not db_contact:
        return None
    db.delete(db_contact)
    db.commit()
    return db_contact

def search_contacts(
    db: Session,
    first_name: str | None = None,
    last_name: str | None = None,
    phone_number: str | None = None,
    address: str | None = None
):
    """
    Search by any combination of first_name, last_name, phone_number, address.
    Only filters that are not None will be applied.
    """
    query = db.query(models.Contact)

    if first_name:
        query = query.filter(models.Contact.first_name.ilike(f"%{first_name}%"))
    if last_name:
        query = query.filter(models.Contact.last_name.ilike(f"%{last_name}%"))
    if phone_number:
        query = query.filter(models.Contact.phone_number.ilike(f"%{phone_number}%"))
    if address:
        query = query.filter(models.Contact.address.ilike(f"%{address}%"))

    return query.all()