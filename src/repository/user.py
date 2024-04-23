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

async def confirmed_email(email: str, db: Session) -> None:
    user = await get_user_by_email(email, db)
    user.confirmed = True
    db.commit()

async def update_avatar(email: str, avatar_path: str, db: Session) -> UserDB:
    print(email)
    user = db.query(UserDB).filter(UserDB.email == email).first()
    print(user)
    user.avatar = avatar_path
    db.commit()
    db.refresh(user)
    return user

async def update_avatar(email, url: str, db: Session) -> UserDB:
    user = await get_user_by_email(email, db)
    user.avatar = url
    db.commit()
    return user