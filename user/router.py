from typing import List

from bcrypt import hashpw, gensalt, checkpw
from fastapi import Depends, APIRouter
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.ext.asyncio import AsyncSession
from sqlmodel import select
from starlette.exceptions import HTTPException

from auth.jwt import create_access_token, get_current_user
from db import get_session
from user.models import User

router = APIRouter(tags=["Users"], prefix="/api/v1/users")


@router.post("/", response_model=User)
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


@router.get("/", response_model=List[User])
async def read_users(skip: int = 0, limit: int = 10, db: AsyncSession = Depends(get_session)):
    users_result = await db.execute(select(User).offset(skip).limit(limit))
    users = users_result.scalars().all()
    return users


@router.post("/login")
async def login(request: OAuth2PasswordRequestForm = Depends(), db: AsyncSession = Depends(get_session)):
    result = await db.execute(select(User).where(User.email == request.username))
    user = result.fetchone()[0]
    print(user.email)
    if user is None:
        raise HTTPException(status_code=401, detail="Wrong Credentials!")

    # Check if the entered password matches the stored hashed password
    if not checkpw(request.password.encode('utf-8'), user.password.encode('utf-8')):
        raise HTTPException(status_code=401, detail="Wrong Credentials!")

    access_token = create_access_token(data={"sub": user.email})
    return {"access_token": access_token, "token_type": "Bearer"}


@router.get("/me")
async def users_me(current_user: User = Depends(get_current_user)):
    return current_user
