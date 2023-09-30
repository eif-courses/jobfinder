from typing import Optional, List

from pydantic import EmailStr
from sqlmodel import Field, SQLModel, Relationship


class Profile(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    bio: str
    skills: List["Skill"] = Relationship(back_populates="profile")
    user: "User" = Relationship(back_populates="profile")
    user_id: int = Field(foreign_key="user.id")


class User(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    username: str = Field(index=True)
    email: EmailStr = Field(unique=True)
    password: str
    profile: "Profile" = Relationship(back_populates="user")
    posts: List["Post"] = Relationship(back_populates="user")
    permissions: str = Field(default="member")


class UserLogin(SQLModel):
    username: str
    email: EmailStr
    password: str
