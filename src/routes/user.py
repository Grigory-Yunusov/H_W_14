# src/routes/user.py
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from src.db.database import get_db
from src.repository.user import create_user, authenticate_user
from src.schemas.schemas import UserCreate, TokenModel
from src.auth.auth import create_access_token
from datetime import timedelta
from sqlalchemy.exc import IntegrityError

router = APIRouter(prefix="/users", tags=["users"])

@router.post("/signup", response_model=TokenModel, status_code=status.HTTP_201_CREATED)
async def signup(user: UserCreate, db: Session = Depends(get_db)):
    try:
        db_user = await create_user(user, db)
        access_token_expires = timedelta(minutes=15)
        access_token = await create_access_token(data={"sub": db_user.email}, expires_delta=access_token_expires)
        return {"access_token": access_token, "token_type": "bearer"}
    except IntegrityError as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="User with this email already exists"
        )
    

@router.post("/login", response_model=TokenModel)
async def login(email: str, password: str, db: Session = Depends(get_db)):
    user = await authenticate_user(email, password, db)
    if not user:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Incorrect email or password")
    access_token_expires = timedelta(minutes=15)
    access_token = await create_access_token(data={"sub": user.email}, expires_delta=access_token_expires)
    return {"access_token": access_token, "token_type": "bearer"}