#src.repository.contacts.py
from ..models.models import ContactDB, UserDB
from sqlalchemy.orm import Session
from src.schemas.schemas import ContactCreate
from sqlalchemy import or_, and_
from datetime import datetime, timedelta, date


async def create_contact(contact: ContactCreate, db: Session, user: UserDB):
    """
    Creates a new contact for a specific user.

    :param contact: The data for the contact to create.
    :type contact: ContactCreate
    :param db: The database session.
    :type db: Session
    :param user: The user to create the contact for.
    :type user: UserDB
    :return: The newly created contact.
    :rtype: ContactDB
    """
    db_contact = ContactDB(**contact.model_dump(), user_id=user.id)
    db.add(db_contact)
    db.commit()
    db.refresh(db_contact)
    return db_contact


async def get_contacts(db: Session, user: UserDB):
    """
    Retrieves a list of contacts for a specific user.

    :param db: The database session.
    :type db: Session
    :param user: The user to retrieve contacts for.
    :type user: UserDB
    :return: A list of contacts.
    :rtype: List[ContactDB]
    """
    contacts = db.query(ContactDB).filter(ContactDB.user_id == user.id).all()
    return contacts

async def get_contact_by_id(db: Session, contact_id: int, user: UserDB):
    """
    Retrieves a single contact with the specified ID for a specific user.

    :param db: The database session.
    :type db: Session
    :param contact_id: The ID of the contact to retrieve.
    :type contact_id: int
    :param user: The user to retrieve the contact for.
    :type user: UserDB
    :return: The contact with the specified ID, or None if it does not exist.
    :rtype: ContactDB | None
    """
    db_contact = db.query(ContactDB).filter(and_(ContactDB.id == contact_id, ContactDB.user_id == user.id)).first()
    return db_contact

async def update_contact(db: Session, contact, db_contact, contact_id: int, user: UserDB):
    """
    Updates a single contact with the specified ID for a specific user.

    :param db: The database session.
    :type db: Session
    :param contact: The updated data for the contact.
    :type contact: ContactUpdate
    :param db_contact: The contact to update.
    :type db_contact: ContactDB
    :param contact_id: The ID of the contact to update.
    :type contact_id: int
    :param user: The user to update the contact for.
    :type user: UserDB
    :return: The updated contact, or None if it does not exist.
    :rtype: ContactDB | None
    """
    db_contact = db.query(ContactDB).filter(and_(ContactDB.id == contact_id, ContactDB.user_id == user.id)).first()
    if db_contact:
        for key, value in contact.model_dump().items():
            setattr(db_contact, key, value)
        db.commit()
        db.refresh(db_contact)
        return db_contact


async def delete_contact(db: Session, db_contact, contact_id: int, user: UserDB):
    """
    Deletes a single contact with the specified ID for a specific user.

    :param db: The database session.
    :type db: Session
    :param db_contact: The contact to delete.
    :type db_contact: ContactDB
    :param contact_id: The ID of the contact to delete.
    :type contact_id: int
    :param user: The user to delete the contact for.
    :type user: UserDB
    """
    db_contact = db.query(ContactDB).filter(and_(ContactDB.id == contact_id, ContactDB.user_id == user.id)).first()
    if db_contact:
        db.delete(db_contact)
        db.commit()


async def search_contacts(query: str, db: Session, user: UserDB):
    """
    Searches for contacts by a query for a specific user.

    :param query: The search query.
    :type query: str
    :param db: The database session.
    :type db: Session
    :param user: The user to search contacts for.
    :type user: UserDB
    :return: A list of contacts matching the query.
    :rtype: List[ContactDB]
    """
    query = query.lower()
    contacts = db.query(ContactDB).filter(
        and_(
            ContactDB.user_id == user.id,
            or_(
                ContactDB.first_name.ilike("%"+query+"%"),
                ContactDB.last_name.ilike("%"+query+"%"),
                ContactDB.email.ilike("%"+query+"%")
            )
        )
    ).all()
    return contacts

async def get_upcoming_birthdays(db: Session, user: UserDB):
    """
    Retrieves a list of upcoming birthdays for contacts of a specific user.

    :param db: The database session.
    :type db: Session
    :param user: The user to retrieve upcoming birthdays for.
    :type user: UserDB
    :return: A list of contacts whose birthday is within the next 7 days.
    :rtype: List[ContactDB]
    """
    today = datetime.now().date()
    next_week = today + timedelta(days=7)
    contacts = db.query(ContactDB).filter(ContactDB.user_id == user.id).all()
    contacts_list = []
    for contact in contacts:
        contact_birthday = contact.birthday.replace(year=today.year)
        if today <= contact_birthday.date() <= next_week:
            contacts_list.append(contact)
    return contacts_list