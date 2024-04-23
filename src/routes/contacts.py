#src.routes.contact.py

"""
Contact routes module.

This module contains the FastAPI routes for the contact-related operations.
It includes routes for creating, reading, updating, deleting, and searching contacts,
as well as retrieving upcoming birthdays.
"""

from src.repository import contacts as repository_contacts
from fastapi import APIRouter, Depends, HTTPException, status
from ..schemas.schemas import ContactResponse, ContactCreate
from  src.db.database import get_db
from sqlalchemy.orm import Session
from ..models.models import UserDB
from src.auth.auth import auth_service
from fastapi_limiter.depends import RateLimiter


# Initialize the router with a prefix and tags for grouping related routes
router = APIRouter(prefix="/contacts", tags=["contacts"])

@router.post("/contacts/", response_model=ContactResponse, status_code=status.HTTP_201_CREATED,
             dependencies=[Depends(RateLimiter(times=2, seconds=5))])
async def create_contact(contact: ContactCreate, db: Session = Depends(get_db), 
                    current_user: UserDB = Depends(auth_service.get_current_user)):
    """
    Create a new contact for the current user.

    :param contact: The data for the contact to create.
    :type contact: ContactCreate
    :param db: The database session.
    :type db: Session
    :param current_user: The currently authenticated user.
    :type current_user: UserDB
    :return: The newly created contact.
    :rtype: ContactResponse
    """
    db_contact = await repository_contacts.create_contact(contact, db, current_user)
    return db_contact

@router.get("/contacts/", response_model=list[ContactResponse], 
            description='No more than 10 requests per minute',
            dependencies=[Depends(RateLimiter(times=10, seconds=60))])
async def read_contacts(db: Session = Depends(get_db),
                    current_user: UserDB = Depends(auth_service.get_current_user)):
    """
    Retrieve a list of contacts for the current user.

    :param db: The database session.
    :type db: Session
    :param current_user: The currently authenticated user.
    :type current_user: UserDB
    :return: A list of contacts.
    :rtype: list[ContactResponse]
    """
    contacts = await repository_contacts.get_contacts(db, current_user)
    return contacts


@router.put("/contacts/{contact_id}", response_model=ContactResponse)
async def update_contact(contact_id: int, contact: ContactCreate, db: Session = Depends(get_db), 
                    current_user: UserDB = Depends(auth_service.get_current_user)):
    """
    Update a contact with the specified ID for the current user.

    :param contact_id: The ID of the contact to update.
    :type contact_id: int
    :param contact: The updated data for the contact.
    :type contact: ContactCreate
    :param db: The database session.
    :type db: Session
    :param current_user: The currently authenticated user.
    :type current_user: UserDB
    :return: The updated contact.
    :rtype: ContactResponse
    :raises HTTPException: If the contact is not found.
    """
    db_contact = await repository_contacts.get_contact_by_id(db, contact_id, current_user)
    if db_contact is None:
        raise HTTPException(status_code=404, detail="Contact not found")
    db_contact = await repository_contacts.update_contact(db, contact, db_contact, contact_id, current_user)
    return db_contact

@router.delete("/contacts/{contact_id}")
async def delete_contact(contact_id: int, db: Session = Depends(get_db), 
                    current_user: UserDB = Depends(auth_service.get_current_user)):
    """
    Delete a contact with the specified ID for the current user.

    :param contact_id: The ID of the contact to delete.
    :type contact_id: int
    :param db: The database session.
    :type db: Session
    :param current_user: The currently authenticated user.
    :type current_user: UserDB
    :return: A success message.
    :rtype: dict
    :raises HTTPException: If the contact is not found.
    """
    db_contact = await repository_contacts.get_contact_by_id(db, contact_id, current_user)
    if db_contact is None:
        raise HTTPException(status_code=404, detail="Contact not found")
    await repository_contacts.delete_contact(db, db_contact, contact_id, current_user)
    return {"ok": True}

@router.get("/contacts/search/", response_model=list[ContactResponse], 
            description='No more than 10 requests per minute',
            dependencies=[Depends(RateLimiter(times=10, seconds=60))])
async def search_contacts(query: str, db: Session = Depends(get_db), 
                    current_user: UserDB = Depends(auth_service.get_current_user)):
    """
    Search for contacts by a query for the current user.

    :param query: The search query.
    :type query: str
    :param db: The database session.
    :type db: Session
    :param current_user: The currently authenticated user.
    :type current_user: UserDB
    :return: A list of contacts matching the query.
    :rtype: list[ContactResponse]
    """
    contacts = await repository_contacts.search_contacts(query, db, current_user)
    return contacts

@router.get("/contacts/birthdays/", response_model=list[ContactResponse])
async def get_upcoming_birthdays(db: Session = Depends(get_db), 
                    current_user: UserDB = Depends(auth_service.get_current_user)):
    """
    Retrieve a list of upcoming birthdays for contacts of the current user.

    :param db: The database session.
    :type db: Session
    :param current_user: The currently authenticated user.
    :type current_user: UserDB
    :return: A list of contacts whose birthday is within the next 7 days.
    :rtype: list[ContactResponse]
    """
    contacts = await repository_contacts.get_upcoming_birthdays(db, current_user)

    return contacts