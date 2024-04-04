from ..models.models import ContactDB
from sqlalchemy.orm import Session
from ..schemas.schemas import ContactCreate
from sqlalchemy import or_
from datetime import datetime, timedelta


async def create_contact(contact: ContactCreate, db: Session):
    db_contact = ContactDB(**contact.dict())
    db.add(db_contact)
    db.commit()
    db.refresh(db_contact)
    return db_contact


async def get_contacts(db: Session):
    contacts = db.query(ContactDB).all()
    return contacts

async def get_contact_by_id(db: Session, contact_id: int):
    db_contact = db.query(ContactDB).filter(ContactDB.id == contact_id).first()
    return db_contact

async def update_contact(db: Session, contact, db_contact):
    for key, value in contact.dict().items():
        setattr(db_contact, key, value)
    db.commit()
    db.refresh(db_contact)
    return db_contact


async def delete_contact(db: Session, db_contact):
    db.delete(db_contact)
    db.commit()


async def search_contacts(query: str, db: Session):
    query = query.lower()
    contacts = db.query(ContactDB).filter(
        or_(
            ContactDB.first_name.ilike("%"+query+"%"),
            ContactDB.last_name.ilike("%"+query+"%"),
            ContactDB.email.ilike("%"+query+"%")
        )
    ).all()
    return contacts

async def get_upcoming_birthdays(db: Session):
    today = datetime.now().date()
    next_week = today + timedelta(days=7)
    contacts = db.query(ContactDB).all()
    contacts_list = []
    for contact in contacts:
        contact_birthday = contact.birthday.replace(year=today.year)
        if today <= contact_birthday <= next_week:
            contacts_list.append(contact)
    return contacts_list