# src/repository/user.py
from src.models.models import UserDB
from sqlalchemy.orm import Session
from src.schemas.schemas import UserModel
from libgravatar import Gravatar 



async def get_user_by_email(email: str, db: Session) -> UserDB:
    return db.query(UserDB).filter(UserDB.email == email).first()


async def create_user(body: UserModel, db: Session) -> UserDB:
    avatar = None
    try:
        g = Gravatar(body.email)
        avatar = g.get_image()
    except Exception as e:
        print(e)
    new_user = UserDB(**body.dict(), avatar=avatar)
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    return new_user


async def update_token(user: UserDB, token: str | None, db: Session) -> None:
    user.refresh_token = token
    db.commit()