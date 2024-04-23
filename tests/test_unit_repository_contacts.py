# test/test_unit_repository_contacts.py

import sys
import os

# Добавляем родительскую директорию в sys.path, чтобы Python мог найти модуль src
parent_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
sys.path.insert(0, parent_dir)

import unittest
from unittest.mock import MagicMock, patch
from datetime import datetime, timedelta

from sqlalchemy.orm import Session

from src.models.models import ContactDB, UserDB
from src.schemas.schemas import ContactCreate, ContactBase
from src.repository.contacts import (
    create_contact,
    get_contacts,
    get_contact_by_id,
    update_contact,
    delete_contact,
    search_contacts,
    get_upcoming_birthdays,
)

class TestContactRepository(unittest.IsolatedAsyncioTestCase):

    def setUp(self):
        self.session = MagicMock(spec=Session)
        self.user = UserDB(id=1)

    async def test_create_contact(self):
        contact_data = ContactCreate(first_name="Test", last_name="User", email="test@example.com", phone_number="123456789", birthday="2024-04-23", additional_data="2024-04-23")
        db_contact = await create_contact(contact_data, self.session, self.user)

        self.session.add.assert_called_once_with(db_contact)
        self.session.commit.assert_called_once()
        self.session.refresh.assert_called_once_with(db_contact)

    async def test_get_contacts(self):
        contacts = [ContactDB(), ContactDB(), ContactDB()]
        self.session.query().filter().all.return_value = contacts

        result = await get_contacts(self.session, self.user)

        self.assertEqual(result, contacts)

    async def test_get_contact_by_id(self):
        contact = ContactDB(id=1, user_id=self.user.id)
        self.session.query().filter().first.return_value = contact

        result = await get_contact_by_id(self.session, 1, self.user)

        self.assertEqual(result, contact)

    async def test_update_contact(self):
        contact_data = ContactCreate(first_name="Updated", last_name="User", email="updated@example.com", phone_number="000056789", birthday="2011-04-23", additional_data="2011-04-23")
        db_contact = ContactDB(id=1, user_id=self.user.id)
        self.session.query().filter().first.return_value = db_contact

        result = await update_contact(self.session, contact_data, db_contact, 1, self.user)

        self.assertEqual(result.first_name, "Updated")
        self.session.commit.assert_called_once()
        self.session.refresh.assert_called_once_with(db_contact)

    async def test_delete_contact(self):
        db_contact = ContactDB(id=1, user_id=self.user.id)
        self.session.query().filter().first.return_value = db_contact

        await delete_contact(self.session, db_contact, 1, self.user)

        self.session.delete.assert_called_once_with(db_contact)
        self.session.commit.assert_called_once()

    async def test_search_contacts(self):
        contacts = [ContactDB(first_name="Test", last_name="User", email="test@example.com")]
        self.session.query().filter().all.return_value = contacts

        result = await search_contacts("test", self.session, self.user)

        self.assertEqual(result, contacts)

    async def test_get_upcoming_birthdays(self):
        today = datetime.now().date()
        next_week = today + timedelta(days=7)
        contacts = [
            ContactDB(birthday=datetime(today.year, today.month, today.day)),
            ContactDB(birthday=datetime(next_week.year, next_week.month, next_week.day))
        ]
        self.session.query().filter().all.return_value = contacts

        result = await get_upcoming_birthdays(self.session, self.user)

        self.assertEqual(len(result), 2)
        self.assertEqual(result[0].birthday.date(), today)
if __name__ == "__main__":
    unittest.main()