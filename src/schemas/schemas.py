#src.schemas.schemas.py
from pydantic import BaseModel, EmailStr, Field
from datetime import date, datetime

class ContactBase(BaseModel):
    first_name: str
    last_name: str
    email: str
    phone_number: str
    birthday: date
    additional_data: str | None

class ContactCreate(ContactBase):
    pass

class ContactResponse(ContactBase):
    id: int

    class Config:
        from_attributes = True


class UserBase(BaseModel): 
    email: EmailStr

class UserCreate(UserBase):
    password: str = Field(min_length=6, max_length=10)
    username: str = Field(min_length=5, max_length=16)

class User(UserBase):
    id: int
    username: str
    email: str
    created_at: datetime
    avatar: str
    class Config:
        orm_mode = True

class TokenModel(BaseModel):
    access_token: str
    refresh_token: str
    token_type: str = "bearer"