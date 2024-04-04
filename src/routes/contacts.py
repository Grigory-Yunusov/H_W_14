from src.repository import contacts as repository_contacts
from fastapi import APIRouter, Depends, HTTPException
from ..schemas.schemas import ContactResponse, ContactCreate
from  src.db.database import get_db
from sqlalchemy.orm import Session




router = APIRouter(prefix="/contacts", tags=["contacts"])

@router.post("/contacts/", response_model=ContactResponse)
async def create_contact(contact: ContactCreate, db: Session = Depends(get_db)):
    db_contact = await repository_contacts.create_contact(contact, db)
    return db_contact

@router.get("/contacts/", response_model=list[ContactResponse])
async def read_contacts(db: Session = Depends(get_db)):
    contacts = await repository_contacts.get_contacts(db)
    return contacts


@router.put("/contacts/{contact_id}", response_model=ContactResponse)
async def update_contact(contact_id: int, contact: ContactCreate, db: Session = Depends(get_db)):
    db_contact = await repository_contacts.get_contact_by_id(db, contact_id)
    if db_contact is None:
        raise HTTPException(status_code=404, detail="Contact not found")
    db_contact = await repository_contacts.update_contact(db, contact, db_contact)
    return db_contact

@router.delete("/contacts/{contact_id}")
async def delete_contact(contact_id: int, db: Session = Depends(get_db)):
    db_contact = await repository_contacts.get_contact_by_id(db, contact_id)
    if db_contact is None:
        raise HTTPException(status_code=404, detail="Contact not found")
    await repository_contacts.delete_contact(db, db_contact)
    return {"ok": True}

@router.get("/contacts/search/", response_model=list[ContactResponse])
async def search_contacts(query: str, db: Session = Depends(get_db)):
    contacts = await repository_contacts.search_contacts(query, db)
    return contacts

@router.get("/contacts/birthdays/", response_model=list[ContactResponse])
async def get_upcoming_birthdays(db: Session = Depends(get_db)):
    contacts = await repository_contacts.get_upcoming_birthdays(db)

    return contacts