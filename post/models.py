from datetime import datetime
from typing import List

from sqlmodel import Field, SQLModel, Relationship


class Category(SQLModel, table=True):
    id: int = Field(default=None, primary_key=True)
    name: str
    posts: List["Post"] = Relationship(back_populates="category")


class Skill(SQLModel, table=True):
    id: int = Field(default=None, primary_key=True)
    profile_id: int = Field(foreign_key="profile.id")
    profile: "Profile" = Relationship(back_populates="skills")
    name: str


class Post(SQLModel, table=True):
    id: int = Field(default=None, primary_key=True)
    title: str
    content: str
    created_at: datetime = datetime.now()
    updated_at: datetime = datetime.now()
    user_id: int = Field(foreign_key="user.id")
    category_id: int = Field(foreign_key="category.id")
    category: "Category" = Relationship(back_populates="posts")
    user: "User" = Relationship(back_populates="posts")
