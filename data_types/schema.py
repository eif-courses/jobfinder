from typing import Optional

from pydantic import EmailStr
from sqlmodel import SQLModel


class Token(SQLModel):
    access_token: str
    token_type: str


class TokenData(SQLModel):
    email: Optional[str] = None


class DisplayUser(SQLModel):
    username: str
    email: EmailStr
    permissions: str


class DisplayPost(SQLModel):
    title: str
    content: str
    created_at: str
    updated_at: str
    user: DisplayUser
