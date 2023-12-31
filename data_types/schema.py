from datetime import datetime
from typing import Optional, List

from pydantic import EmailStr
from sqlmodel import SQLModel

from data_types.models import Skill, User


class Token(SQLModel):
    access_token: str
    token_type: str


class TokenData(SQLModel):
    email: Optional[str] = None


class DisplayUser(SQLModel):
    username: str
    email: EmailStr
    permissions: Optional[List[str]]


class DisplayPost(SQLModel):
    title: str
    content: str
    created_at: datetime
    updated_at: datetime
    user: DisplayUser


class DisplaySkills(SQLModel):
    skill: Skill
    user: User
