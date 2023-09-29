from typing import List

from bcrypt import hashpw, gensalt, checkpw
from fastapi import Depends, APIRouter
from sqlalchemy.ext.asyncio import AsyncSession
from sqlmodel import select
from starlette import status
from starlette.exceptions import HTTPException

from db import get_session
from user.models import User

router = APIRouter(tags=["Users"], prefix="/api/v1")


@router.post("/users/", response_model=User)
async def create_user(user: User, db: AsyncSession = Depends(get_session)):
    is_user_exists = await db.execute(select(User).where(User.email == user.email))
    if is_user_exists.scalars().first():
        raise HTTPException(status_code=400, detail="User already exists!")

    hashed_password = hashpw(user.password.encode('utf-8'), gensalt())
    new_user = User(username=user.username, email=user.email, password=hashed_password.decode('utf-8'))

    db.add(new_user)
    await db.commit()
    await db.refresh(new_user)
    return new_user


@router.get("/users/", response_model=List[User])
async def read_users(skip: int = 0, limit: int = 10, db: AsyncSession = Depends(get_session)):
    users_result = await db.execute(select(User).offset(skip).limit(limit))
    users = users_result.scalars().all()
    return users


@router.post("/users/login")
async def login(username: str, password: str, db: AsyncSession = Depends(get_session)):
    result = await db.execute(select(User).where(User.email == username))
    user = result.fetchone()[0]
    if user is None:
        raise HTTPException(status_code=401, detail="Invalid credentials")

    # Check if the entered password matches the stored hashed password
    if not checkpw(password.encode('utf-8'), user.password.encode('utf-8')):
        raise HTTPException(status_code=401, detail="Invalid credentials")

    # Passwords match, the user is authenticated
    return {"message": "Login successful"}
