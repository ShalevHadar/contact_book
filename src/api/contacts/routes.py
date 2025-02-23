from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from contact_book.shared import database
from contact_book.shared.global_strings import pagination_route_path, get_contact_route_path, contact_base_route_path, \
    update_contact_route_path, delete_contact_route_path, search_contact_route_path
from contact_book.shared.logger import app_log
from contact_book.src.api.contacts import models, schemas
from contact_book.src.api.contacts import services as contact_service

router = APIRouter(
    prefix="/contacts",
    tags=["contacts"]
)

def get_db():
    db = database.SessionLocal()
    try:
        yield db
    finally:
        db.close()

@router.get(path=pagination_route_path, response_model=list[schemas.Contact])
def list_contacts(page: int = 1, db: Session = Depends(get_db)):
    """
    List contacts with pagination
    EXAMPLE: GET /contacts/pagination?page=1
    :param page:
    :param db:
    :return:
    """
    try:
        if page == 0:
            raise HTTPException(status_code=400, detail="Page number must be greater than 0")
        skip = (page - 1) * 10
        contacts = contact_service.get_contacts(db, skip=skip, limit=10)
        app_log.info(f"Listing contacts for page {page}. Found {len(contacts)} contacts.")
        return contacts
    except HTTPException as e:
        app_log.error("HTTPException encountered in list_contacts", exc_info=True)
        raise e
    except Exception as e:
        app_log.error("Unexpected error in list_contacts", exc_info=True)
        raise HTTPException(status_code=500, detail="Internal server error") from e


@router.get(path=get_contact_route_path, response_model=schemas.Contact)
def get_contact(contact_id: int, db: Session = Depends(get_db)):
    """
    Get a contact by ID
    EXAMPLE: GET /contacts/1
    Since I define int in the path parameter, FastAPI will automatically convert the string to an integer.
    :param contact_id:
    :param db:
    :return:
    """
    try:
        contact = contact_service.get_contact(db, contact_id)
        if not contact:
            app_log.info(f"Contact with ID {contact_id} not found.")
            raise HTTPException(status_code=404, detail="Contact not found")
        app_log.info(f"Fetched contact with ID {contact_id}.")
        return contact
    except HTTPException as e:
        app_log.error("HTTPException encountered in get_contact", exc_info=True)
        raise e
    except Exception as e:
        app_log.error("Unexpected error in get_contact", exc_info=True)
        raise HTTPException(status_code=500, detail="Internal server error") from e

@router.post(path=contact_base_route_path, response_model=schemas.Contact)
def create_new_contact(contact: schemas.ContactBase, db: Session = Depends(get_db)):
    """
    Create a new contact
    EXAMPLE: POST /contacts with JSON body
    :param contact:
    :param db:
    :return:
    """
    try:
        existing = db.query(models.Contact).filter(models.Contact.phone_number == contact.phone_number).first()
        if existing:
            app_log.info(f"Attempt to create a contact with existing phone number: {contact.phone_number}")
            raise HTTPException(status_code=400, detail="Contact already exists")
        new_contact = contact_service.create_contact(db, contact)
        app_log.info(f"Created new contact with ID {new_contact.id}.")
        return new_contact
    except HTTPException as e:
        app_log.error("HTTPException encountered in create_new_contact", exc_info=True)
        raise e
    except Exception as e:
        app_log.error("Unexpected error in create_new_contact", exc_info=True)
        raise HTTPException(status_code=500, detail="Internal server error") from e


@router.put(path=update_contact_route_path, response_model=schemas.Contact)
def update_existing_contact(contact_id: int, contact: schemas.ContactUpdate, db: Session = Depends(get_db)):
    """
    Update a contact by ID
    EXAMPLE: PUT /contacts/1
    :param contact_id:
    :param contact:
    :param db:
    :return:
    """
    try:
        db_contact = contact_service.get_contact(db, contact_id)
        if not db_contact:
            app_log.info(f"Attempt to update a non-existent contact with ID {contact_id}.")
            raise HTTPException(status_code=404, detail="Contact not found")
        updated = contact_service.update_contact(db, contact_id, contact)
        app_log.info(f"Updated contact with ID {updated.id}.")
        return updated
    except HTTPException as e:
        app_log.error("HTTPException encountered in update_existing_contact", exc_info=True)
        raise e
    except Exception as e:
        app_log.error("Unexpected error in update_existing_contact", exc_info=True)
        raise HTTPException(status_code=500, detail="Internal server error") from e


@router.delete(path=delete_contact_route_path)
def delete_existing_contact(contact_id: int, db: Session = Depends(get_db)):
    """
    Delete a contact by ID
    EXAMPLE: DELETE /contacts/1
    :param contact_id:
    :param db:
    :return:
    """
    try:
        db_contact = contact_service.get_contact(db, contact_id)
        if not db_contact:
            app_log.info(f"Attempt to delete a non-existent contact with ID {contact_id}.")
            raise HTTPException(status_code=404, detail="Contact not found")
        contact_service.delete_contact(db, contact_id)
        app_log.info(f"Deleted contact with ID {contact_id}.")
        return {"detail": "Contact deleted"}
    except HTTPException as e:
        app_log.error("HTTPException encountered in delete_existing_contact", exc_info=True)
        raise e
    except Exception as e:
        app_log.error("Unexpected error in delete_existing_contact", exc_info=True)
        raise HTTPException(status_code=500, detail="Internal server error") from e

@router.get(path=search_contact_route_path, response_model=list[schemas.Contact])
def search_contact(
    first_name: str | None = None,
    last_name: str | None = None,
    phone_number: str | None = None,
    address: str | None = None,
    db: Session = Depends(get_db)
):
    """
    Search contacts by any combination of first_name, last_name, phone_number, or address.
    Example: GET /contacts/search?first_name=jane&last_name=john
    """
    try:
        app_log.info(
            f"Searching with filters: first_name={first_name}, "
            f"last_name={last_name}, phone_number={phone_number}, address={address}"
        )
        results = contact_service.search_contacts(
            db,
            first_name=first_name,
            last_name=last_name,
            phone_number=phone_number,
            address=address,
        )
        return results
    except HTTPException as e:
        app_log.error("HTTPException encountered in search_contact", exc_info=True)
        raise e
    except Exception as e:
        app_log.error("Unexpected error in search_contact", exc_info=True)
        raise HTTPException(status_code=500, detail="Internal server error") from e
