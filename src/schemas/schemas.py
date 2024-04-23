#src.schemas.schemas.py

"""
Pydantic Schemas Module.

This module contains the Pydantic models for data validation and serialization.
"""

from pydantic import BaseModel, EmailStr, Field
from datetime import date, datetime




class ContactBase(BaseModel):
    """
    Base Pydantic model for Contact.

    This model is used as a base for other Contact models and defines the common fields.

    - first_name: The first name of the contact.
    - last_name: The last name of the contact.
    - email: The email of the contact.
    - phone_number: The phone number of the contact.
    - birthday: The birthday of the contact.
    - additional_data: Additional data about the contact.
    """
    first_name: str
    last_name: str
    email: str
    phone_number: str
    birthday: date
    additional_data: str | None

class ContactCreate(ContactBase):
    """
    Pydantic model for creating a Contact.

    This model inherits from ContactBase and is used for creating new contacts.
    """
    pass

class ContactResponse(ContactBase):
    """
    Pydantic model for a Contact response.

    This model inherits from ContactBase and adds an id field. It is used to define the response schema for a contact.

    - id: The id of the contact.
    """
    id: int
    

    class Config:
        from_attributes = True


class UserModel(BaseModel):
    """
    Pydantic model for a User.

    This model defines the fields for a user.

    - username: The username of the user.
    - email: The email of the user.
    - password: The password of the user.
    """
    username: str = Field(min_length=5, max_length=16)
    email: str
    password: str = Field(min_length=6, max_length=10)


class UserDb(BaseModel):
    """
    Pydantic model for a User in the database.

    This model defines the fields for a user in the database.

    - id: The id of the user.
    - username: The username of the user.
    - email: The email of the user.
    - created_at: The date and time the user was created.
    - avatar: The URL of the user's avatar.
    """
    id: int
    username: str
    email: str
    created_at: datetime
    avatar: str

    class Config:
        from_attributes = True


class UserResponse(BaseModel):
    """
    Pydantic model for a User response.

    This model defines the response schema for a user.

    - user: The user object.
    - detail: A message indicating that the user was successfully created.
    """
    user: UserDb
    detail: str = "User successfully created"


class TokenModel(BaseModel):
    """
    Pydantic model for a Token.

    This model defines the fields for a token.

    - access_token: The access token.
    - refresh_token: The refresh token.
    - token_type: The type of the token.
    """
    access_token: str
    refresh_token: str
    token_type: str = "bearer"
    
    
class RequestEmail(BaseModel):
    """
    Pydantic model for an Email request.

    This model defines the fields for an email request.

    - email: The email address.
    """ 
    email: EmailStr
