# models.py

"""
Database Models Module.

This module contains the SQLAlchemy models for the database tables.
"""

from src.db.database import Base
from sqlalchemy import Column, Integer, String, Date, func, Boolean
from sqlalchemy.orm import relationship
from sqlalchemy.sql.schema import ForeignKey
from sqlalchemy.sql.sqltypes import DateTime

# Database model
class ContactDB(Base):
    """
    ContactDB model class.

    This class represents the 'contacts' table in the database. It contains the following columns:

    - id: The primary key for the contact.
    - first_name: The first name of the contact.
    - last_name: The last name of the contact.
    - email: The email of the contact.
    - phone_number: The phone number of the contact.
    - birthday: The birthday of the contact.
    - additional_data: Additional data about the contact.
    - user_id: The foreign key linking the contact to a user.
    - user: The relationship to the UserDB model.
    """
    __tablename__ = "contacts"
    id = Column(Integer, primary_key=True, index=True)
    first_name = Column(String)
    last_name = Column(String)
    email = Column(String, unique=True, index=True)
    phone_number = Column(String)
    birthday = Column(Date)
    additional_data = Column(String, nullable=True)
    user_id = Column('user_id', ForeignKey('users.id', ondelete='CASCADE'), default=None)
    user = relationship('UserDB', backref="contacts")


class UserDB(Base):
    """
    UserDB model class.

    This class represents the 'users' table in the database. It contains the following columns:

    - id: The primary key for the user.
    - username: The username of the user.
    - email: The email of the user.
    - created_at: The date and time the user was created.
    - password: The hashed password of the user.
    - avatar: The URL of the user's avatar.
    - refresh_token: The refresh token for the user.
    - confirmed: A boolean indicating whether the user's email has been confirmed.
    """
    __tablename__ = "users"
    id = Column(Integer, primary_key=True)
    username = Column(String(50))
    email = Column(String(250), nullable=False, unique=True)
    created_at = Column('crated_at', DateTime, default=func.now())
    password = Column(String(255), nullable=False)
    avatar = Column(String(255), nullable=True)
    refresh_token = Column(String(255), nullable=True)
    confirmed = Column(Boolean, default=False)
    # hashed_password = Column(String)


