# src/repository/user.py
from src.models.models import UserDB
from sqlalchemy.orm import Session
from src.schemas.schemas import UserCreate
from passlib.context import CryptContext
from src.auth.auth import Hash



pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
hash_handler = Hash()

async def create_user(user: UserCreate, db: Session):
    hashed_password = pwd_context.hash(user.password)
    db_user = UserDB(email=user.email, password=hashed_password)
    # db_user = UserDB(email=user.email, hashed_password=hash_handler.get_password_hash(user.password))
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user

async def authenticate_user(email: str, password: str, db: Session):
    user = db.query(UserDB).filter(UserDB.email == email).first()
    if not user:
        return False
    if not pwd_context.verify(password, user.password):
        return False
    return user